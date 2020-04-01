#!/usr/bin/env python
from random import randint, choice, random
import math,os,sys,imp

from CShip import Ship
from CEnemy import Enemy
from CActor import Actor
from CEffects import Effects
from CSoundManager import SoundMng

from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.task.Task import Task
from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import Filename,Texture,Shader
from pandac.PandaModules import GraphicsOutput
from pandac.PandaModules import NodePath,TextNode
from pandac.PandaModules import OrthographicLens

import missions.chapter1
sys.path.append('missions/chapter1/')

# Get the location of the 'py' file I'm running:
mydir = os.path.abspath(sys.path[0])
 
# Convert that to panda's unix-style notation.
mydir = Filename.fromOsSpecific(mydir).getFullpath()

font = loader.loadFont(mydir+"/fonts/ocrb.ttf")

def addText(posx,posy, msg):
    return OnscreenText(text=msg, style=2, fg=(1,1,1,1), font = font,
      pos=(posx, posy), align=TextNode.ALeft, scale = .027)
    
class World:
    
    def __init__(self, actor, state,lvl):
        
        #Setzte die Parameter
        self.CActor = actor #Spieler erstellen
        self.CGame = state #FSM - Gamestate erstellen
        self.mission = lvl #Aktuelle Mission
        self.mMission = None
        
        #Grundeinstellen fuer die Welt
        base.disableMouse()#Mouse ausmachen
        self.slowdown = 1#Schnelligkeitsfaktor 1=Normal
        self.hud = False
        
        file, filename, description = imp.find_module("mission"+str(self.mission))
        self.mMission = imp.load_module("mission"+str(self.mission) ,file, filename,description)
        
         #SPIELER - Variablen
        self.oldactorlevel = self.CActor.getLevel()
        self.CActor.CActorShip.setX(-165)#Setze den Spieler links im Bildschirm
        self.CActor.CActorShip.setY(0)
        self.CActor.nActorShip.reparentTo(render)
        self.CActor.CActorShip.getWeapon().setWeapon("laserGun") #Standardwaffe setzen
        self.maxshield = self.CActor.CActorShip.getShield()#Schild speichern um Prozent berechnen zu koennen
        self.hitted = False #Variable um abzufragen ob man getroffen wurde
        self.dead = False #Spieler lebt
        self.lbullets = [] #Spielerbullets
        self.lbulletsspeed = []
        self.lcanon = [] #Spielercanonbullets
        self.lcanonspeed = []
        self.cameraeffectx = 0#X-Wert der Camera um eine Sinuskurve zu implementieren
        self.cameraeffectamplitude = 5#Die Amplitude der Sinuswelle - Maxima                
        self.exppercent = (self.CActor.getExperience() * 100)/self.CActor.getMaxExperience()#EXP in Prozent       
        self.oldcash = self.CActor.getMoney()
        self.secweapon = 3
        
       
        #Resultattexte, wenn die Mission zu ende ist
        self.txtresultmission = addText(-0.15,0.35,"")
        self.txtresultkills = addText(-0.15,0.25,"")
        self.txtresultleft = addText(-0.15,0.20,"")
        self.txtresultcash = addText(-0.15,0.15,"")
        self.txtresultlevel = addText(-0.15,0.10,"")
        self.txtresultmessage = addText(-0.15,0.0,"")
        
        #ALLES FUER MOTION BLUR ***********************************************************************
        #Eine Texture erstellen, welches in das Hauptfenster kopiert wird
        self.CTex = Texture()
        self.CTex.setMinfilter(Texture.FTLinear)
        base.win.addRenderTexture(self.CTex, GraphicsOutput.RTMTriggeredCopyTexture)
     
        #Eine andere 2D Kamera erstellen, welches vor der Hauptkamera gerendert wird
        self.backcam = base.makeCamera2d(base.win, sort=-10)
        self.background = NodePath("background")
        self.backcam.reparentTo(self.background)
        self.background.setDepthTest(0)
        self.background.setDepthWrite(0)
        self.backcam.node().getDisplayRegion(0).setClearDepthActive(0)

        #Zwei Texturekarten ersten. Eins bevor, eins danach
        self.bcard = base.win.getTextureCard()
        self.bcard.reparentTo(self.background)
        self.bcard.setTransparency(1)
        self.fcard = base.win.getTextureCard()
        self.fcard.reparentTo(render2d)
        self.fcard.setTransparency(1)
        #**********************************************************************************************
        
        #Drops als Liste
        self.ldrop = []
        #Explosionen - oder besser gesagt Splittereffekt als Liste
        self.lexplosions = []
        
        #Soundklasse erstellen um Zugriff auf die Sound zu haben
        self.CSound = SoundMng()
        self.CSound.sndFlyAmbience.play()
        
        #GEGNER - Variablen
        self.destroyedenemy = 0
        self.lostenemy = 0
        self.lenemys = [] #Gegnerspeicher
        self.lbulletsenemy = [] #Gegnerbullets
        
        self.newwave = False #Boolean,welches eine neue Gegnerwelle angibt
    
            
        
        #Effekte
        self.CEffects = Effects() #Effektklasse erstellen
        #self.CEffects.createSpaceStars("particle/background.ptf") #Hintergrundeffekt erstellen
       
        #Die Game-Loop Voreinstellungen
        self.gameTask = taskMgr.add(self.gameLoop,"gameLoop")
        self.gameTask.last = 0 
        self.gameTask.nextbullet = 0#Timer wann geschossen werden darf, vom Spieler
        self.gameTask.gotHit = 0
        self.gameTask.lnextenemybullet = []#Timer wann geschossen werden darf, unabhaengig von welche Gegner
        self.gameTask.resultkills = 0#Timer fuer die Kills, im Resultat
        self.gameTask.resultleft = 0#Timer fuer die geflohenen Gegner, im Resultat
        self.gameTask.introduction = 0
        self.gameTask.introdelete = 0
        self.gameTask.won = 0
        
        self.resultcounter = 0#Zeahler der die Nummern der Kills im Result aktualisiert
        self.resultcounterleft = 0#Zeahler der die Nummern der geflohenen Gegner im Result aktualisiert
    
        self.introcounter = 0
        
        self.ldata = []
        self.readytospawn = False
        
        self.musicplayed = False
        self.musicplayed2 = False
        self.resultplayed = False
        
        #2D Kamera erstellen
        lens = OrthographicLens()
        lens.setFilmSize(350, 250)  
        base.cam.node().setLens(lens)
        
    def gameLoop(self,task):
        
        #Clock fuer FPS unabhaengige Bewegung
        elapsed = globalClock.getDt()
        
        if task.time > task.introduction:
            if (self.mMission.getIntroduction(self.introcounter) == True):
                self.introcounter +=1
                task.introduction = task.time + 0.1
            else:
                task.introdelete = task.introduction + 3
                if task.time > task.introdelete:
                    if self.musicplayed == False:
                        self.CSound.sndMusic.play()
                        self.musicplayed = True
                        self.toogleHud()
                    self.mMission.removeIntroduction()
            
        
        if self.mMission.getSituation(task.time) == True:
            for i in range(3):
                self.ldata.append(self.mMission.getEnemies(i))
            self.createEnemys(self.ldata[len(self.ldata)-3],self.ldata[len(self.ldata)-1])
            self.spawnEnemys(200,self.ldata[len(self.ldata)-2])
    
        
        #Die Position der Gegner aktualisieren
        for obj in self.lenemys:
            self.updatePosEnemy(obj,elapsed)
            if obj.nEnemyShip.isEmpty()==0:        
                if obj.CEnemyShip.getX()<-180:
                    obj.nEnemyShip.removeNode()
                    self.lostenemy +=1
                if obj.CEnemyShip.getX()>170:
                   obj.nEnemyShip.detachNode()
                if obj.CEnemyShip.getX()<170 and obj.CEnemyShip.getX()>-150:
                   obj.nEnemyShip.reparentTo(render)
                
                
        if self.destroyedenemy + self.lostenemy == self.mMission.MAX_ENEMYS:
            if task.won==0:
                task.won = task.time + 3
            if task.won < task.time and self.musicplayed2 == False:
                self.CSound.sndMusic.stop()
                self.musicplayed2 = True
                task.won = task.time + 3
        
            if task.won < task.time:
                if self.resultplayed == False:
                    self.CSound.sndResult.play()
                    self.CSound.sndFlyAmbience.stop()
                    self.resultplayed = True
                for drop in self.ldrop:
                    drop.remove()           
                self.txthp.destroy()
                self.txtshield.destroy()
                self.txtlvl.destroy()
                self.imgHud.destroy()
                self.imgExp.destroy()
                self.txtresultmission.setText("Mission: "+str(self.mission)+ " Complete")
                if task.time > task.resultkills:
                    if self.resultcounter < self.destroyedenemy:
                        self.resultcounter +=1
                        self.txtresultkills.setText("Killed Enemies: "+str(self.resultcounter))
                        self.CSound.sndTipp.play()
                        task.resultkills = task.time + 0.1
                    if self.resultcounter == self.destroyedenemy:
                        if task.time >task.resultleft:
                            if self.resultcounterleft < self.lostenemy:
                                self.resultcounterleft +=1
                                self.txtresultleft.setText("Left Enemies: "+str(self.resultcounterleft))
                                task.resultleft = task.time + 0.1
                                self.CSound.sndTipp.play()
                        if self.resultcounterleft == self.lostenemy:
                            self.txtresultcash.setText("Geldstand: "+str(self.CActor.getMoney()) + "$ (+" + str(self.CActor.getMoney()-self.oldcash)+"$)")
                            self.txtresultlevel.setText("Dein Level: "+str(self.CActor.getLevel())+" (+"+str(self.CActor.getLevel()-self.oldactorlevel)+")")
                            self.txtresultmessage.setText("Druecke Enter um fortzufahren")
                            if self.CActor.keyMap["entr"]!=0:
                                self.CActor.CActorShip.setShield(self.maxshield)
                                self.CActor.setHP(self.CActor.getMaxHP())
                                taskMgr.remove('gameLoop')
                                self.CGame.request("GameMenue",self.CActor,self.CGame)  
                                        
     
            
        if self.dead == True:
            render.node().removeAllChildren() 
            taskMgr.remove("gameLoop")
            self.CGame.request("MainMenue",self.CGame)
            
            
        #Falls nextEnemyBullet-Timer NULL ist, so erstelle fuer jeden Gegner einen eigenen Timer
        if(self.newwave == True):
            for i in range(len(self.lenemys)):
                task.lnextenemybullet.append(i)
                self.newwave = False
        
        #Gegnerfeuer erstellen und mit einem Zufallsalgorythmus schiessen lassen    
        for i in range(len(self.lenemys)):
            posEnemyX = self.lenemys[i].CEnemyShip.getX()
            #Erst schiessen lassen, wenn sie im Spielbereich sind
            if posEnemyX<170 and posEnemyX>-180 and self.lenemys[i].nEnemyShip.hasParent()==True:
                if task.time > task.lnextenemybullet[i]:
                    task.lnextenemybullet[i] = task.time + choice(range(4, 7) + range(4, 7))
                    self.enemyShot(self.lenemys[i])
                    self.lenemys[i].CEnemyShip.getWeapon().sndGun.setVolume(0.5)
                    self.lenemys[i].CEnemyShip.getWeapon().sndGun.play()
                    
            
            
        #Nachdem der Spieler die Schiesstaste gedrueckt hat, wird ein Timer aktiviert der nach eine Zeit
        #immer wieder aktualisiert wird, damit der Spieler den naechsten Schuss abfeuern kann
        if(self.CActor.keyMap["arr_up"]!=0 and task.time > task.nextbullet):
            if self.dead==False:
                task.nextbullet = task.time + 1.25**(-1.5*self.CActor.getAgility())
                self.playerShot("laserGun")
                self.CActor.CActorShip.getWeapon().sndGun.play()    
  
  
        #Nachdem der Spieler die Schiesstaste gedrueckt hat, wird ein Timer aktiviert der nach eine Zeit
        #immer wieder aktualisiert wird, damit der Spieler den naechsten Schuss abfeuern kann
        if(self.CActor.keyMap["arr_right"]!=0 and task.time > task.nextbullet):
            if self.dead==False:
                task.nextbullet = task.time + 1+1.25**(-1.5*self.CActor.getAgility())
                self.playerShot("canonGun")
                self.CActor.CActorShip.getWeapon().sndGun.play()
                
                
        #Ein Array, um abgeschossen Patronen festzuhalten: vom Spieler
        lnewbullet = []
        
        #Funktion um die Bullets zu aktualsieren
        for i in range(len(self.lbullets)):
            self.updateBulletPlayer(self.lbullets[i],self.lbulletsspeed[i],elapsed)
            if self.lbullets[i].isEmpty()==0:
                if(self.lbullets[i].getX()<180):
                    lnewbullet.append(self.lbullets[i])
                else:
                    self.lbullets[i].remove()           
        self.lbullets = lnewbullet


        lnewcanon = []
        
        #Funktion um die Bullets zu aktualsieren
        for i in range(len(self.lcanon)):
            self.updateBulletPlayer(self.lcanon[i],self.lcanonspeed[i],elapsed)
            if self.lcanon[i].isEmpty()==0:
                if(self.lcanon[i].getX()<180):
                    lnewcanon.append(self.lcanon[i])
                else:
                    self.lcanon[i].remove()           
        self.lcanon = lnewcanon
        
        #Ein Array, um abgeschossen Patronen festzuhalten: vom Gegner
        lnewenemybullet = []
        
        
        #Funktion um die Bullets der Gegner zu aktualsieren
        for obj in self.lbulletsenemy:
                self.updateBulletEnemy(obj,elapsed)
                if obj.isEmpty()==0:
                    if(obj.getX()>-180):
                        lnewenemybullet.append(obj)
                    else:
                       obj.remove()
        self.lbulletsenemy = lnewenemybullet
                    
            
        #Funktion fuer die Kollision mit dem Gegner
        for obj in self.lbullets:
            self.enemyHit(obj)
        for obj in self.lcanon:
            self.enemyHit(obj)
        
        #Funktion fuer die Kollision mit dem Spieler
        if self.playerHit() == True:
            self.hitted = True                                
        
        #Funktion fuer die Kollision mit dem Schiff
        if self.getShipHit() == True:
            self.hitted = True
            
        self.dropHit()
        
        #Falls Spieler getroffen wird, so mache ein Cameraeffekt
        if self.hitted == True:
            if self.CActor.CActorShip.getShield()>0:
                self.cameraeffectamplitude = 5
                base.camera.setZ(base.camera.getZ()+ self.cameraeffectamplitude*math.sin(self.cameraeffectx))              
                self.cameraeffectx = self.cameraeffectx + 1
                if self.cameraeffectx == 20:
                    self.hitted = False
                    self.cameraeffectx = 0
                    base.camera.setZ(0)
            else:
                if(self.dead == False):
                    self.cameraeffectamplitude = 2
                    base.camera.setZ(base.camera.getZ()+ self.cameraeffectamplitude*math.sin(self.cameraeffectx))
                    self.cameraeffectx = self.cameraeffectx + 1
                else:
                    self.hitted = False
                    
        for obj in self.ldrop:
            if obj != None:
                if obj.isEmpty() == 0:
                    obj.setHpr(obj.getH()-1,0,0)
                
        for obj in self.lexplosions:
            if obj != None:
                if obj.isEmpty()==0:
                    posy = obj.getZ()
                    self.updateExplosion(obj,elapsed,-3,choice(range(-11,11) + range(-11,11)))
                    if obj.getX()<-180:
                        obj.remove()
    
        return Task.cont
    
    
    def updateExplosion(self,obj,dt,x,y):
        if obj.isEmpty()==0:
            newposx = obj.getX() + (self.slowdown*dt*35*3)*x
            newposy = obj.getZ() + (self.slowdown*dt*35*3)*y
            obj.setX(newposx)
            obj.setZ(newposy)
            
    def updateBulletPlayer(self,obj,spe,dt):
        if obj.isEmpty()==0:
            newpos = obj.getX() + (self.slowdown*dt*35*spe)
            obj.setX(newpos)
        
    def updateBulletEnemy(self,obj,dt):
        if obj.isEmpty()==0:
            newpos = obj.getX() - (self.slowdown*dt*35*self.CEnemy.CEnemyShip.getWeapon().getWeaponSpeed())
            obj.setX(newpos)
                             
    def updatePosEnemy(self,obj,dt):
        if obj.nEnemyShip.isEmpty()==0:
            obj.CEnemyShip.setX(obj.CEnemyShip.getX()-self.slowdown*dt*15*obj.CEnemyShip.getSpeed())
            obj.CEnemyShip.setY(obj.CEnemyShip.getY()+self.slowdown*dt*15*(math.sin(0.1*obj.CEnemyShip.getX())))

    def playerShot(self,gun):
        bullet = self.CActor.CActorShip.getWeapon().setWeapon(gun)
        if bullet.isEmpty() == 0:
            if self.secweapon ==3:
                bullet.setPos(self.CActor.CActorShip.getX()+10,500,self.CActor.CActorShip.getY()+self.secweapon)
                self.secweapon = -4
            else:
                bullet.setPos(self.CActor.CActorShip.getX()+10,500,self.CActor.CActorShip.getY()+self.secweapon)
                self.secweapon = 3
            print self.CActor.CActorShip.getWeapon().getWeapon()
            if self.CActor.CActorShip.getWeapon().getWeapon() == "laserGun":
                self.lbullets.append(bullet)
                self.lbulletsspeed.append(self.CActor.CActorShip.getWeapon().getWeaponSpeed())
            elif self.CActor.CActorShip.getWeapon().getWeapon() == "canonGun":
                self.lcanon.append(bullet)
                self.lcanonspeed.append(self.CActor.CActorShip.getWeapon().getWeaponSpeed())
        del bullet
        
        
    def enemyShot(self,obj):
        bullet = obj.CEnemyShip.getWeapon().setWeapon("laserGun")
        if obj.nEnemyShip.isEmpty()==0:
            bullet.setPos(obj.nEnemyShip.getPos())
            self.lbulletsenemy.append(bullet)
        del bullet
            

    def addDrop(self,pos):
        drp = self.CEffects.getDrop("models/heal",19,pos)
        if(drp == None):
            return False
        else:
            self.ldrop.append(drp)
            return True
        
    def explode(self,pos):
        expl = self.CEffects.getExplosion(pos)
        self.lexplosions.append(expl)
        
            
    def enemyHit(self,bullet): 
        for enmy in self.lenemys:
            if enmy.nEnemyShip.isEmpty()==0 and bullet.isEmpty()==0:
                #Falls Gegner getroffen wird
                if (bullet.getPos() - enmy.nEnemyShip.getPos()).lengthSquared() < 85:
                    
                    #Bullet loesche
                    bullet.remove()
                    self.explode(enmy.nEnemyShip.getPos())
                    enmy.CEnemyShip.setShield(enmy.CEnemyShip.getShield()-self.CActor.CActorShip.getWeapon().getWeaponStrength())
                    self.CSound.sndHit.play()
                    #Falls kein Schild mehr vorhanden -> Loeschen  
                    if enmy.CEnemyShip.getShield()<=0:
                        self.addDrop(enmy.nEnemyShip.getPos())
                        
                        for i in range(5):
                            self.explode(enmy.nEnemyShip.getPos())
                            
                        enmy.nEnemyShip.removeNode()
                        self.CSound.sndExplosion.play()
                        self.destroyedenemy +=1
                        self.CActor.setExperience(self.CActor.getExperience() + (enmy.getExpDrop()))
                        self.exppercent = (self.CActor.getExperience() * 100)/self.CActor.getMaxExperience()
                        if self.imgExp.isEmpty()==0:
                            self.imgExp.setScale(0.01,0.2,((2.0*self.exppercent)/100.0))
                        self.CActor.setMoney(self.CActor.getMoney()+enmy.getCashDrop())
                        
                    if self.CActor.getLevelUp()==True:
                        self.txtlvl.setText(str(self.CActor.getLevel()))
                        self.CActor.setExperience(self.CActor.getExperience() + (enmy.getExpDrop()/2))
                        self.exppercent = (self.CActor.getExperience() * 100)/self.CActor.getMaxExperience()
                        self.imgExp.setScale(0.01,0.2,0.002)
                                               
    def playerHit(self):
        for bullet in self.lbulletsenemy:
            if self.CActor.nActorShip.isEmpty()==0 and bullet.isEmpty()==0:
                #Falls Spieler getroffen wird
                if ((bullet.getPos() - self.CActor.nActorShip.getPos()).lengthSquared() < 85):
           
                    #Bullet loeschen
                    bullet.remove()

                    #Funktion aufrufen - Parameter: Schaden
                    if self.actorHurt(self.CEnemy.CEnemyShip.getWeapon().getWeaponStrength()+self.CEnemy.getStrength()) == True:
                        return True
                
    def getShipHit(self):
        for enmy in self.lenemys:
            if enmy.nEnemyShip.isEmpty()==0 and self.CActor.nActorShip.isEmpty()==0:
                #Falls das Spielerschiff einen Gegnerschiff trifft
                if ((enmy.nEnemyShip.getPos() - self.CActor.nActorShip.getPos()).lengthSquared() < 85):
                    
                    for i in range(5):
                        self.explode(enmy.nEnemyShip.getPos())
                        
                    enmy.nEnemyShip.removeNode()
                    #self.CSound.sndExplosion.play()
                    self.destroyedenemy +=1
                    self.CActor.setExperience(self.CActor.getExperience() + (enmy.getExpDrop()/2))
                    self.exppercent = (self.CActor.getExperience() * 100)/self.CActor.getMaxExperience()
                    if self.CActor.getLevelUp()==True:
                        self.txtlvl.setText(str(self.CActor.getLevel()))
                        self.CActor.setExperience(self.CActor.getExperience() + (enmy.getExpDrop()/2))
                        self.exppercent = (self.CActor.getExperience() * 100)/self.CActor.getMaxExperience()
                    #Schaden ist gleich der Staerke vom gegnerischen Schiff
                    if self.actorHurt(enmy.getStrength()) == True:
                        return True
                    
    def createEnemys(self,amount,kind):
        for i in range(amount):
            #Gegner erstellen
            self.CEnemy = Enemy(kind)
            self.lenemys.append(self.CEnemy)
    
    def spawnEnemys(self,start,width):
        for obj in self.lenemys:
            if obj.CEnemyShip.getY()>101 and obj.nEnemyShip.isEmpty()==0:
                obj.CEnemyShip.setX(choice(range(start, width) + range(start, width)))
                obj.CEnemyShip.setY(choice(range(-100, 0) + range(0, 100)))
            self.newwave = True
            
    def dropHit(self):
        for obj in self.ldrop:
            if obj.isEmpty()==0 and self.CActor.nActorShip.isEmpty()==0:
                if((obj.getPos() - self.CActor.nActorShip.getPos()).lengthSquared() < 86):
               
                    obj.remove()
                    if self.CActor.getHP()<self.CActor.getMaxHP():
                        self.CActor.setHP(self.CActor.getHP()+20)
                        self.txthp.setText(str((self.CActor.getHP()*100)/self.CActor.getMaxHP()))    

    def actorHurt(self,dmg):
        if(self.CActor.CActorShip.getShield()<=0):
            self.txtshield.setText("0")
            self.CActor.CActorShip.setShield(0)
            self.CActor.setHP(self.CActor.getHP()-dmg*20)
            self.CSound.sndCrit.play()
            if(self.CActor.getHP()<=0):
                #Der Spieler ist tot und hat verloren
                self.txthp.setText("0")
                self.dead = True
                #self.CFilters.setBloom(blend=(0,0,0,1), desat=-0.5, intensity=5.0, size="small")
                self.slowdown = 1
                self.CActor.slowdown = self.slowdown
                taskMgr.remove("takeSnapShot")
                self.clickrate = 0
                self.fcard.hide()
                for i in range(5):
                    self.explode(self.CActor.nActorShip.getPos())
                self.CActor.nActorShip.detachNode()
                
                return True

            if(self.CActor.getHP()<=50):
                
                self.CSound.sndExplosion.setPlayRate(0.5)
                self.CSound.sndMusic.setPlayRate(0.5)
                self.CSound.sndFlyAmbience.setPlayRate(0.5)
                self.CSound.sndHit.setPlayRate(0.5)
                self.CActor.CActorShip.getWeapon().sndGun.setPlayRate(0.5)
                taskMgr.add(self.takeSnapShot, "takeSnapShot")
                self.chooseEffectGhost()
                self.slowdown = 0.5
                self.CActor.setSlowDown(self.slowdown)
                #self.CFilters.delBloom()
                self.explode(self.CActor.nActorShip.getPos())

            self.txthp.setText(str((self.CActor.getHP()*100)/self.CActor.getMaxHP()))
            return True
        else:
            self.CActor.CActorShip.setShield(self.CActor.CActorShip.getShield()-dmg)
            self.txtshield.setText(str((self.CActor.CActorShip.getShield()*100)/self.maxshield))
            self.explode(self.CActor.nActorShip.getPos())
            return True
                    
    #Screenshots erstellen um MotionBlur Effekt zu erreichen            
    def takeSnapShot(self, task):
        if (task.time > self.nextclick):
            self.nextclick += 1.0 / self.clickrate
            if (self.nextclick < task.time):
                self.nextclick = task.time
            base.win.triggerCopy()
        return Task.cont

    #MotionBlur Effekt
    def chooseEffectGhost(self):
        base.setBackgroundColor(0,0,0,1)
        self.bcard.hide()
        self.fcard.show()
        self.fcard.setColor(1.0,1.0,1.0,0.99)
        self.fcard.setScale(1.00)
        self.fcard.setPos(0,0,0)
        self.fcard.setR(0)
        self.clickrate = 100
        self.nextclick = 0  
            
    def toogleHud(self):
        if self.hud == False:
            #Hudeinstellung *******************************************************************************
            self.imgHud = OnscreenImage(image = 'images/hud.png', pos = (-1.09, 0,-0.01),scale=(0.185,0.5,1) )
            self.imgHud.reparentTo(aspect2d)
            self.imgHud.setTransparency(TransparencyAttrib.MAlpha)
            #EXP Leiste
            self.imgExp = OnscreenImage(image = 'images/exp.png', pos = (-1.2645,0,-1),scale=(0.01,0.2,0.001))
            self.imgExp.reparentTo(aspect2d)
            #Texte der HUD
            self.txthp = addText(-1.03,0.966,str((self.CActor.getHP()*100)/self.CActor.getMaxHP()))
            self.txtshield = addText(-1.03,0.9151,str((self.CActor.CActorShip.getShield()*100)/self.maxshield))
            self.txtlvl = addText(-1.19,0.80,str(self.CActor.getLevel()))
            self.hud = True
