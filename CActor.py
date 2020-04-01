#!/usr/bin/env python

#Importe von Dateien
from direct.showbase import DirectObject
import direct.directbase.DirectStart
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

#Eigene Importe
from CShip import Ship
from CEnemy import Enemy

#Bildbereich, in der man sich frei bewegen kann
MAX_X = 170
MIN_X = -180
MAX_Y = 126
MIN_Y = -135

class Actor(DirectObject.DirectObject):
    
    def __init__(self,modelPath):
       
        #Keymap fuer die Steuerung als Assoziativen Array
        self.keyMap = {"up":0, "down":0, "left":0, "right":0, "arr_up":0,
                       "arr_down":0,"arr_left":0,"arr_right":0,"entr":0}
       
        #Initialisierung der Klassenvariablen
        self.__maxhp = 250
        self.__hp = self.__maxhp
        self.__strength = 1
        self.__stamina = 1
        self.__agility = 1
        self.__charisma = 1
        self.__level = 1
        self.__experience = 0
        self.__maxexp = 500
        self.__points = 0
        self.__money = 1
        self.__slowdown = 1#Faktor fuer Motion Blur
        
        #Private Konstanten
        self.__POINTS_ADD = 2
        self.__EXP_FACTOR = 500
        
        #Schiff erstellen und die Anfangswerte setzen - Publicvariablen
        self.CActorShip = Ship()
        self.nActorShip = self.CActorShip.getShip(modelPath)
        self.nActorShip.setScale(0.7,0.7,0.7)
        self.nActorShip.setHpr(-90,0,30)
        self.CActorShip.setX(-165)
        self.CActorShip.setY(0)
        self.CActorShip.setShield(self.CActorShip.getShield()+5)
        self.CActorShip.setSpeed(self.CActorShip.getSpeed()+6)
        self.nActorShip.detachNode()
        
        #Keymap fuer die Steuerung, Methode - accept - von DirectObject
        self.accept("w",self.setKey,["up",1])
        self.accept("a",self.setKey,["left",1])
        self.accept("s",self.setKey,["down",1])
        self.accept("d",self.setKey,["right",1])
        self.accept("arrow_up",self.setKey,["arr_up",1])
        self.accept("arrow_down",self.setKey,["arr_down",1])
        self.accept("arrow_left",self.setKey,["arr_left",1])
        self.accept("arrow_right",self.setKey,["arr_right",1])
        self.accept("enter",self.setKey,["entr",1])
        #--------------------------------------------------------------
        self.accept("w-up",self.setKey,["up",0])
        self.accept("a-up",self.setKey,["left",0])
        self.accept("s-up",self.setKey,["down",0])
        self.accept("d-up",self.setKey,["right",0])
        self.accept("arrow_up-up",self.setKey,["arr_up",0])
        self.accept("arrow_down-up",self.setKey,["arr_down",0])
        self.accept("arrow_left-up",self.setKey,["arr_left",0])
        self.accept("arrow_right-up",self.setKey,["arr_right",0])
        self.accept("enter-up",self.setKey,["entr",0])
        
        #Der Task fuer die Bewegung mittels der Tastatureingabe
        self.moveTask = taskMgr.add(self.move,"moveTask")

    def setHP(self,hp):
        self.__hp = hp
        
    def setMaxHP(self,mhp):
        self.__maxhp = mhp
        
    def setStrength(self,str):
        self.__strength = str
    
    def setStamina(self,sta):
        self.__stamina = sta
        self.setMaxHP(self.getMaxHP()+(self.getStamina()*20))
        self.setHP(self.getMaxHP())
        
    def setAgility(self,agi):
        self.__agility = agi
        
    def setCharisma(self,cha):
        self.__charisma = cha
        
    def setLevel(self,lvl):
        self.__level = lvl
        
    def setExperience(self,exp):
        self.__experience = exp
        
    def setMaxExperience(self,mexp):
        self.__maxexp = mexp
        
    def setPoints(self,lvlp):
        self.__points = lvlp
        
    def setMoney(self,cash):
        self.__money = cash
        
    def setSlowDown(self,sd):
        self.__slowdown = sd
        
    def getHP(self):
        return self.__hp
    
    def getMaxHP(self):
        return self.__maxhp
    
    def getStrength(self):
        return self.__strength
    
    def getStamina(self):
        return self.__stamina
    
    def getAgility(self):
        return self.__agility
    
    def getCharisma(self):
        return self.__charisma
    
    def getLevel(self):
        return self.__level
    
    def getExperience(self):
        return self.__experience
    
    def getMaxExperience(self):
        return self.__maxexp
    
    def getPoints(self):
        return self.__points
    
    def getMoney(self):
        return self.__money
    
    def getSlowDown(self):
        return self.__slowdown   
    
    def setKey(self,key,value):
        self.keyMap[key] = value
        
    def move(self,task):
    
        #Clock fuer FPS unabhaengige Bewegung
        elapsed = globalClock.getDt()
         
        #Falls in dem zugaenglichen Bildbereich gespielt wird
        if self.CActorShip.getX()>MIN_X and self.CActorShip.getX()<MAX_X and self.CActorShip.getY()>MIN_Y and self.CActorShip.getY()<MAX_Y:
            if(self.keyMap["right"]!=0):
                self.CActorShip.setX(self.CActorShip.getX() + self.getSlowDown()*elapsed*10*self.CActorShip.getSpeed())
               
            if(self.keyMap["up"]!=0):
                self.CActorShip.setY(self.CActorShip.getY() + self.getSlowDown()*elapsed*10*self.CActorShip.getSpeed())
                if self.CActorShip.getP()>=20:
                    self.CActorShip.setP(self.CActorShip.getP()-40*self.getSlowDown()*elapsed)
            if(self.keyMap["up"]==0):
                if self.CActorShip.getP()<30:
                    self.CActorShip.setP(self.CActorShip.getP()+40*self.getSlowDown()*elapsed)
                
            if(self.keyMap["down"]!=0):
                self.CActorShip.setY(self.CActorShip.getY() - self.getSlowDown()*elapsed*10*self.CActorShip.getSpeed())
                if self.CActorShip.getP()<=40:
                    self.CActorShip.setP(self.CActorShip.getP()+40*self.getSlowDown()*elapsed)
            if(self.keyMap["down"]==0):
                if self.CActorShip.getP()>30:
                    self.CActorShip.setP(self.CActorShip.getP()-40*self.getSlowDown()*elapsed)        
                    
            if(self.keyMap["left"]!=0):   
                self.CActorShip.setX(self.CActorShip.getX() - self.getSlowDown()*elapsed*10*self.CActorShip.getSpeed())
        else: #Falls man gegen eine Wand kommt
            if(self.CActorShip.getX()<=MIN_X):
                self.CActorShip.setX(self.CActorShip.getX()+1)
            elif(self.CActorShip.getX()>=MAX_X):
                self.CActorShip.setX(self.CActorShip.getX()-1)
            elif(self.CActorShip.getY()>=MAX_Y):
                self.CActorShip.setY(self.CActorShip.getY()-1)
            elif(self.CActorShip.getY()<=MIN_Y):
                self.CActorShip.setY(self.CActorShip.getY()+1)     
                
        return Task.cont
            
    def getLevelUp(self):
        if self.__experience >= self.__maxexp:
            self.setLevel(self.getLevel()+1)
            self.setExperience(0)
            self.setMaxExperience(self.getMaxExperience() + self.__EXP_FACTOR *self.getLevel()*2)
            self.setPoints(self.getPoints()+self.__POINTS_ADD)
            return True
        else:
            return False

            

        