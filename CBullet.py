#!/usr/bin/env python

#Importe von Dateien
from direct.directbase import DirectStart
from pandac.PandaModules import TransparencyAttrib
class Bullet:
    
    def __init__(self):
        self.__xpos = 0
        self.__speed = 0
        self.__ypos = 0
        self.__pos = 0
        self.__mPath = ""
        self.__nBullet = None
    
    def getBullet(self,path):
        self.__mPath = path
        self.__nBullet = loader.loadModel(self.__mPath)
        self.__nBullet.reparentTo(render)
        self.__nBullet.setScale(0.5,0.1,0.5)
        self.__nBullet.setHpr(0,0,90)
        return self.__nBullet
    
    def setSpeed(self,spe):
        self.__speed = spe
    
    def setX(self,x):
        self.__xpos = x
        self.__nBullet.setX(self.__xpos)
        
    def setY(self,y):
        self.__ypos = y
        self.__nBullet.setZ(self.__ypos)
        
    def setPos(self,posi):
        self.__pos = posi
        self.__nBullet.setPos(self.__pos)
        
    def getX(self):
        return self.__xpos
    
    def getY(self):
        return self.__ypos
    
    def getPos(self):
        return self.__pos
    
    def getModelPath(self):
        return self.__mPath
        
    def getSpeed(self):
        return self.__speed