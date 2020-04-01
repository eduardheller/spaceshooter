#!/usr/bin/env python

import direct.directbase.DirectStart
from direct.particles.ParticleEffect import ParticleEffect
from pandac.PandaModules import Filename
from random import randint, choice, random

class Effects:
    
    def __init__(self):
        
        #Initialisierung
        base.enableParticles()
        self.__space = ParticleEffect()
        self.__particlepath = ""
        
        #Dropvariablen
        self.__nDrop = None
        self.__dropitem = ""
        self.__chance = 0
        
        #Explosionen Attribute 
        self.__nExplosion = None
        
        #Dropattribute
        self.__heal = 0

    def createSpaceStars(self,particlefile):
        self.__particlepath = particlefile
        self.__space.loadConfig(Filename(self.__particlepath))
        
        self.__space.setPos(0,10000,-20)
        self.__space.setScale(250,200,250)
        
    def removeSpaceStars(self):
        self.__space.cleanup()
        
    def getDrop(self,drop,chnc,pos):
        self.__dropitem = drop
        self.__chance = chnc
        generate = choice(range(0, 100) + range(0, 100))
        if generate<self.__chance:
            self.__nDrop = loader.loadModel(self.__dropitem)
            self.__nDrop.setScale(1,1,1)
            self.__nDrop.reparentTo(render)
            self.__nDrop.setPos(pos)
            return self.__nDrop
        else:
            self.__nDrop = None
            
    def getExplosion(self,pos):
        self.__nExplosion = loader.loadModel("models/box")
        self.__nExplosion.reparentTo(render)
        self.__nExplosion.setScale(1,1,1)
        self.__nExplosion.setPos(pos)
        return self.__nExplosion
     

    