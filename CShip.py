#!/usr/bin/env python
from direct.directbase import DirectStart
from CWeapon import Weapon
from direct.gui.OnscreenImage import OnscreenImage

class Ship:
    
    def __init__(self):
        
        #Initialisierung der Klassenvariablen
        self.__xpos = 0
        self.__ypos = 0
        self.__shield = 0
        self.__speed = 0
        self.__pitch = 0
        self.__CWeapon = Weapon()
        self.__nShip = None
        self.__mPath = ""
        
    #Funktion die ein Node des Schiffes returned        
    def getShip(self,path):
        self.__mPath = path
        self.__nShip = loader.loadModel(self.__mPath)
        self.__nShip.reparentTo(render)
        self.__nShip.setScale(10,10,10)
        self.__nShip.setPos(0,500,0)#500 Entfernt
        return self.__nShip

    
    def setX(self,x):
        self.__xpos = x
        self.__nShip.setX(self.__xpos)
        
    def setY(self,y):
        self.__ypos = y
        self.__nShip.setZ(self.__ypos)
        
    def setP(self,p):
        self.__pitch = p
        self.__nShip.setR(self.__pitch)
        
    def setSpeed(self,spe):
        self.__speed = spe
        
    def setShield(self,shie):
        self.__shield = shie
        
    def getX(self):
        return self.__xpos
    
    def getY(self):
        return self.__ypos
    
    def getP(self):
        return self.__pitch
    
    def getSpeed(self):
        return self.__speed
    
    def getShield(self):
        return self.__shield
    
    def getModelPath(self):
        return self.__mPath
    
    def getWeapon(self):
        return self.__CWeapon
        
        