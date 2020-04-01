#!/usr/bin/env python
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import Filename,TextNode
import os,sys
sys.path.append('././')
from CSoundManager import SoundMng

CSound = SoundMng()

# Get the location of the 'py' file I'm running:
mydir = os.path.abspath(sys.path[0])
 
# Convert that to panda's unix-style notation.
mydir = Filename.fromOsSpecific(mydir).getFullpath()

font = loader.loadFont(mydir+"/fonts/bo.ttf")

def addText():
    return OnscreenText( style=2, fg=(1,1,1,1), font = font,
       align=TextNode.ALeft, scale = .027)
    
    
#**********************************************************************************************************    
    

#Wieviele Gegner abhauen oder zerstoert werden um zu gewinnen
MAX_ENEMYS = 25

#Nur die Daten veraendern - erste Zahl: Welle, zweite Zahl: Zeit wann die Welle kommt
nextwave = {
0:8,
1:25,
}

#Nicht loeschen!
wave = []
for i in range(len(nextwave)):
    wave.append(0)
    

txtline1 = "MISSION 3: SEEK THE COW " #Nur den String aendern

# Nicht Loeschen
txtl1 = addText()

#Die Funktion nicht veraendern!
def getIntroduction(counter):
    
    text = ""
    for i in range(counter):
        text += txtline1[i]
    if counter < len(txtline1):
        txtl1.setPos(-0.5,0.35)
        txtl1.setText(text)
        CSound.sndTipp.play()
        return True
    else:
        return False
    
# Nicht Loeschen
def removeIntroduction():
    txtl1.destroy()
    
# Nicht Loeschen
def getSituation(time):
    for wv,t in nextwave.iteritems():
        if time > t and wave[wv]==0:
            wave[wv] = 1
            return True
    return False

# Nicht Loeschen
def getEnemies(pcount):
    enemies = []
    if wave[0] >= 1 and wave[0]<4:
        enemies=[15,800,"white"]
        wave[0] +=1
        
    elif wave[1] >= 1 and wave[1]<4:
        enemies=[10,800,"green"]    
        wave[1] +=1
        
    return enemies[pcount]    
        


    
    