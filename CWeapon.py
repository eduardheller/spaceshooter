#!/usr/bin/env python

#Eigene Importe
from CBullet import Bullet
import direct.directbase.DirectStart

class Weapon:
    
    def __init__(self):
        self.__laserGun = {"equip":0,"str":100,"speed":300}
        self.__canonGun = {"equip":0,"str":5,"speed":1}
        self.__superGun = {"equip":0,"str":4,"speed":4}
        self.__waterBombGun = {"equip":0,"str":8,"speed":6}
        self.__currentWeapon = "laserGun"
        self.CBullet = Bullet()

    def setWeapon(self,newWeapon):
        self.__currentWeapon = newWeapon
        if newWeapon=="laserGun":
            self.__laserGun["equip"] = 1
            self.__canonGun["equip"] = 0
            self.__superGun["equip"] = 0
            self.__waterBombGun["equip"] = 0
            self.CBullet.setSpeed(self.__laserGun["speed"])
            self.setWeaponStrength(self.__laserGun["str"])
            self.sndGun = loader.loadSfx("sounds/laser1.wav")
            return self.CBullet.getBullet("models/bullet")
            
        elif newWeapon=="canonGun":
            self.__laserGun["equip"] = 0
            self.__canonGun["equip"] = 1
            self.__superGun["equip"] = 0
            self.__waterBombGun["equip"] = 0
            self.setWeaponStrength(3)
            self.CBullet.setSpeed(self.__canonGun["speed"])
            self.setWeaponStrength(self.__canonGun["str"])
            self.sndGun = loader.loadSfx("sounds/laser2.wav")
            bull = self.CBullet.getBullet("models/canongun")
            bull.setScale(0.1,0.1,0.1)
            return bull
            
        elif newWeapon=="superGun":
            self.__laserGun["equip"] = 0
            self.__canonGun["equip"] = 0
            self.__superGun["equip"] = 1
            self.__waterBombGun["equip"] = 0
            self.setWeaponStrength(5)
            self.CBullet.setSpeed(self.superGun["speed"])
            self.setWeaponStrength(self.superGun["str"])
            return self.CBullet.getBullet("models/box")
            
        elif newWeapon=="waterBombGun":
            self.__laserGun["equip"] = 0
            self.__canonGun["equip"] = 0
            self.__superGun["equip"] = 0
            self.__waterBombGun["equip"] = 1
            self.setWeaponStrength(9)
            self.CBullet.setSpeed(self.waterBombGun["speed"])
            self.setWeaponStrength(self.waterBombGun["str"])
            return self.CBullet.getBullet("models/box")
            
        else:
            self.__laserGun["equip"] = 0
            self.__canonGun["equip"] = 0
            self.__superGun["equip"] = 0
            self.__waterBombGun["equip"] = 0
            print "ERROR: WEAPON NAME NOT FOUND"
            
    def setWeaponStrength(self,str):
        if self.getWeapon() == "laserGun" : self.__laserGun["str"] = str
        elif self.getWeapon() == "canonGun": self.__canonGun["str"] = str
        elif self.getWeapon() == "superGun": self.__superGun["str"] = str
        elif self.getWeapon() == "waterBombGun": self.__waterBombGun["str"] = str
        
    def setWeaponSpeed(self,spe):
        if self.getWeapon() == "laserGun" : self.__laserGun["speed"] = spe
        elif self.getWeapon() == "canonGun": self.__canonGun["speed"] = spe
        elif self.getWeapon() == "superGun": self.__superGun["speed"] = spe
        elif self.getWeapon() == "waterBombGun": self.__waterBombGun["speed"] = spe
        
    def getWeapon(self):
        return self.__currentWeapon
    
    def getWeaponStrength(self):
        if self.getWeapon() == "laserGun" : return self.__laserGun["str"]
        elif self.getWeapon() == "canonGun": return self.__canonGun["str"]
        elif self.getWeapon() == "superGun": return self.__superGun["str"]
        elif self.getWeapon() == "waterBombGun": return self.__waterBombGun["str"]       
        
    def getWeaponSpeed(self):
        if self.getWeapon() == "laserGun" : return self.__laserGun["speed"] 
        elif self.getWeapon() == "canonGun": return self.__canonGun["speed"]
        elif self.getWeapon() == "superGun": return self.__superGun["speed"]
        elif self.getWeapon() == "waterBombGun": return self.__waterBombGun["speed"]
        
        
        
          
            
    