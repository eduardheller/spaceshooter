#!/usr/bin/env python

#Eigene Importe
from CShip import Ship

class Enemy:
    
    def __init__(self,kindofenemy):
        
        #Private Attribute
        self.__strength = 0
        self.__agility = 0
        self.__exp = 0
        self.__amountcash = 0
        
        #Instanz: Schiff erstellen
        self.CEnemyShip = Ship()


        if kindofenemy == "white":
            self.nEnemyShip = self.CEnemyShip.getShip("models/fight")
            self.nEnemyShip.setScale(0.1,0.4,0.7)
            self.nEnemyShip.setHpr(90,0,-15)
            self.CEnemyShip.setShield(2)
            self.CEnemyShip.setSpeed(1)
            self.setStrength(1)
            self.setAgility(1)
            self.setExpDrop(50)
            self.setCashDrop(20)
            
        if kindofenemy == "green":
            self.nEnemyShip = self.CEnemyShip.getShip("models/fight")
            self.nEnemyShip.setScale(0.1,0.7,1.2)
            self.nEnemyShip.setHpr(90,0,-15)
            self.CEnemyShip.setShield(25)
            self.CEnemyShip.setSpeed(1)
            self.setStrength(2)
            self.setAgility(4)            
            self.setExpDrop(150)
            self.setCashDrop(50)
            
        if kindofenemy == "yellow":
            #self.nEnemyShip = self.CEnemyShip.getShip("models/box") 
            self.CEnemyShip.setShield(90)
            self.CEnemyShip.setSpeed(2)
            self.setStrength(3)
            self.setAgility(5)
            self.setExpDrop(500)
            self.setCashDrop(150)
            
        if kindofenemy == "blue":
            #self.nEnemyShip = self.CEnemyShip.getShip("models/box")
            self.CEnemyShip.setShield(4)
            self.CEnemyShip.setSpeed(2)
            self.setStrength(3)
            self.setAgility(3)
            self.setExpDrop(500)
            self.setCashDrop(550)
            
        if kindofenemy == "purple":
            #self.nEnemyShip = self.CEnemyShip.getShip("models/box")
            self.CEnemyShip.setShield(7)
            self.CEnemyShip.setSpeed(1)
            self.setStrength(5)
            self.setAgility(8)
            self.setExpDrop(1700)
            self.setCashDrop(1000)
            
        if kindofenemy == "black":
            self.nEnemyShip = self.CEnemyShip.getShip("models/fight")
            self.CEnemyShip.setShield(100)
            self.CEnemyShip.setSpeed(0.5)
            self.nEnemyShip.setScale(0.1,0.4,0.7)

            #self.CEnemyShip.CWeapon.setWeaponSpeed(10)
            self.setStrength(9)
            self.setAgility(9)
            self.setExpDrop(5000)
            self.setCashDrop(10000)
            
        self.CEnemyShip.setX(0)
        self.CEnemyShip.setY(150)
        
    def createEnemy(self):
        return self.CEnemyShip.getShip(self.path)
        
    def setShield(self,newShield):
        self.CEnemyShip.setShield(newShield)
        
    def setStrength(self,str):
        self.__strength = str
    
    def setAgility(self,agi):
        self.__agility = agi
        
    def setCashDrop(self,csh):
        self.__amountcash = csh
        
    def setExpDrop(self,ep):
        self.__exp = ep
        
    def getStrength(self):
        return self.__strength
    
    def getAgility(self):
        return self.__agility
    
    def getCashDrop(self):
        return self.__amountcash
    
    def getExpDrop(self):
        return self.__exp
    
    def getShield(self):
        return self.CEnemyShip.getShield()    