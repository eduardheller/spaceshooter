#!/usr/bin/env python

import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import NodePath,TextNode

font = loader.loadFont("cmss12")
def addText(posx,posy, msg):
    return OnscreenText(text=msg, style=2, fg=(1,1,1,1), font = font,
      pos=(posx, posy), align=TextNode.ALeft, scale = .05)

class ShipShop:
    
    def __init__(self,actor,state):
        self.CActor = actor
        self.CGame = state
        
        self.txtMoney = addText(-0.3,0.50,"Money: "+ str(self.CActor.getMoney())+"$")
        self.txtShield = addText(-0.3,0.23,"Shield: "+ str(self.CActor.CActorShip.getShield()))
        self.txtSpeed = addText(-0.3,0.03,"Speed: "+ str(self.CActor.CActorShip.getSpeed()))
        self.txtWeaponStr = addText(-0.3,-0.37,"Weapon Strength: "+str(self.CActor.CActorShip.getWeapon().getWeaponStrength()))
        self.txtWeaponSpeed = addText(-0.3,-0.57,"Weapon Speed: "+str(self.CActor.CActorShip.getWeapon().getWeaponSpeed()))
        
        self.txtCostsShield = addText(0.35,0.23,"Cost: "+ str(self.CActor.CActorShip.getShield()*self.CActor.CActorShip.getShield())+"$")
        self.txtCostsSpeed = addText(0.35,0.03,"Cost: "+ str(self.CActor.CActorShip.getSpeed()*self.CActor.CActorShip.getSpeed()*self.CActor.CActorShip.getSpeed())+"$")
        self.txtCostsWeaponStr = addText(0.35,-0.37,"Cost: "+ str(self.CActor.CActorShip.getWeapon().getWeaponStrength()*self.CActor.CActorShip.getWeapon().getWeaponStrength()*self.CActor.CActorShip.getWeapon().getWeaponStrength())+"$")
        self.txtCostsWeaponSpeed = addText(0.35,-0.57,"Cost: "+ str(self.CActor.CActorShip.getWeapon().getWeaponSpeed()*self.CActor.CActorShip.getWeapon().getWeaponSpeed()*self.CActor.CActorShip.getWeapon().getWeaponSpeed())+"$")
        
        self.btnShieldPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addShield)
        self.btnShieldPlus['text_scale'] = 0.50
        self.btnShieldPlus['frameSize'] = (1.5,2.5,2,3)
        self.btnShieldPlus['text_pos'] = (2,2.4)
        
        self.btnSpeedPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addSpeed)
        self.btnSpeedPlus['text_scale'] = 0.50
        self.btnSpeedPlus['frameSize'] = (1.5,2.5,0,1)
        self.btnSpeedPlus['text_pos'] = (2,0.4)
        
        self.btnWeaponPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addWeaponStrength)
        self.btnWeaponPlus['text_scale'] = 0.50
        self.btnWeaponPlus['frameSize'] = (1.5,2.5,-4,-3)
        self.btnWeaponPlus['text_pos'] = (2,-3.6)        
        
        self.btnWeaponSpeedPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addWeaponSpeed)
        self.btnWeaponSpeedPlus['text_scale'] = 0.50
        self.btnWeaponSpeedPlus['frameSize'] = (1.5,2.5,-6,-5)
        self.btnWeaponSpeedPlus['text_pos'] = (2,-5.6)
        
        self.btnEnd = DirectButton(text = ("Back", "Back", "-Back-", "disabled"), scale=.10, command=self.back)
        self.btnEnd['text_scale'] = 0.50
        self.btnEnd['frameSize'] = (-2,2,-8,-7)
        self.btnEnd['text_pos'] = (0,-7.6)
        
        self.optSelectWeapon = DirectOptionMenu(text="Weapons", scale=0.05,items=[self.CActor.CActorShip.getWeapon().getWeapon(),"superGun"],initialitem=0,
        highlightColor=(0.65,0.65,0.65,1),command=self.buyWeapon)
        self.optSelectWeapon['text_pos'] = (-5.8,-3.3)   
        self.optSelectWeapon['frameSize'] = (-6.0,5,-4,-2)
        
        
    def back(self):
        self.CGame.request("GameMenue",self.CActor,self.CGame)
        
    def addShield(self):
        x = self.CActor.CActorShip.getShield()
        cost = x*x
        if(self.CActor.getMoney()>=cost):
            self.CActor.CActorShip.setShield(self.CActor.CActorShip.getShield()+1)
            self.txtShield.setText("Shield: "+ str(self.CActor.CActorShip.getShield()))
            self.CActor.setMoney(self.CActor.getMoney()-cost)
            self.txtMoney.setText("Geld: "+ str(self.CActor.getMoney())+"$")
            self.txtCostsShield.setText("Kosten: "+ str(self.CActor.CActorShip.getShield()*self.CActor.CActorShip.getShield())+"$")
            
    def addSpeed(self):
        x = self.CActor.CActorShip.getSpeed()
        cost = x*x*x
        if(self.CActor.getMoney()>=cost):
            self.CActor.CActorShip.setSpeed(self.CActor.CActorShip.getSpeed()+1)
            self.txtSpeed.setText("Speed: "+ str(self.CActor.CActorShip.getSpeed()))
            self.CActor.setMoney(self.CActor.getMoney()-cost)
            self.txtMoney.setText("Geld "+ str(self.CActor.getMoney())+"$")
            self.txtCostsSpeed.setText("Kosten: "+ str(self.CActor.CActorShip.getSpeed()*self.CActor.CActorShip.getSpeed()*self.CActor.CActorShip.getSpeed())+"$")
                                     
    def addWeaponStrength(self):
        x = self.CActor.CActorShip.getWeapon().getWeaponStrength()
        cost = x*x*x
        if(self.CActor.getMoney()>=cost):
            self.CActor.CActorShip.getWeapon().setWeaponStrength(self.CActor.CActorShip.getWeapon().getWeaponStrength()+1)
            self.txtWeaponStr.setText("Weapon Strength: "+ str(self.CActor.CActorShip.getWeapon().getWeaponStrength()))
            self.CActor.setMoney(self.CActor.getMoney()-cost)
            self.txtMoney.setText("Geld "+ str(self.CActor.getMoney())+"$")        
  
    def addWeaponSpeed(self):
        x = self.CActor.CActorShip.getWeapon().getWeaponSpeed()
        cost = x*x*x        
        if(self.CActor.getMoney()>cost):
            self.CActor.CActorShip.getWeapon().setWeaponSpeed(self.CActor.CActorShip.getWeapon().getWeaponSpeed()+1)
            self.txtWeaponSpeed.setText("Weapon Speed: "+ str(self.CActor.CActorShip.getWeapon().getWeaponSpeed()))
            self.CActor.setMoney(self.CActor.getMoney()-cost)
            self.txtMoney.setText("Geld: "+ str(self.CActor.getMoney())+"$")
            
    def buyWeapon(self,arg):
        self.CActor.CActorShip.getWeapon().currentWeapon = arg
        self.txtMoney.setText("Geld: "+ str(self.CActor.getMoney())+"$")
        self.txtShield.setText("Shield: "+ str(self.CActor.CActorShip.getShield()))
        self.txtSpeed.setText("Speed: "+ str(self.CActor.CActorShip.getSpeed()))
        self.txtWeaponStr.setText("Weapon Strength: "+str(self.CActor.CActorShip.getWeapon().getWeaponStrength()))
        self.txtWeaponSpeed.setText("Weapon Speed: "+ str(self.CActor.CActorShip.getWeapon().getWeaponSpeed()))