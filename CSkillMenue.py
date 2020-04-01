#!/usr/bin/env python

import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import NodePath,TextNode

font = loader.loadFont("cmss12")
def addText(pos, msg):
    return OnscreenText(text=msg, style=2, fg=(1,1,1,1), font = font,
      pos=(-0.3, pos), align=TextNode.ALeft, scale = .05)
    
    
class SkillMenue:
    
    def __init__(self,actor,state):
        self.CActor = actor
        self.CGame = state
        
        self.txtPoints = addText(0.50,"Points to give: "+ str(self.CActor.getPoints()))
        self.txtStrength = addText(0.23,"Strength: "+ str(self.CActor.getStrength()))
        self.txtAgility = addText(0.03,"Agility: "+ str(self.CActor.getAgility()))
        self.txtStamina = addText(-0.17,"Stamina: "+ str(self.CActor.getStamina()))
        self.txtCharisma = addText(-0.37,"Charisma: "+ str(self.CActor.getCharisma()))
        
        self.btnStrengthPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addStrength)
        self.btnStrengthPlus['text_scale'] = 0.50
        self.btnStrengthPlus['frameSize'] = (1.5,2.5,2,3)
        self.btnStrengthPlus['text_pos'] = (2,2.4)
        
        self.btnAgilityPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addAgility)
        self.btnAgilityPlus['text_scale'] = 0.50
        self.btnAgilityPlus['frameSize'] = (1.5,2.5,0,1)
        self.btnAgilityPlus['text_pos'] = (2,0.4)
        
        self.btnStaminaPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addStamina)
        self.btnStaminaPlus['text_scale'] = 0.50
        self.btnStaminaPlus['frameSize'] = (1.5,2.5,-2,-1)
        self.btnStaminaPlus['text_pos'] = (2,-1.6)        
        
        self.btnCharismaPlus = DirectButton(text = ("+", "+", "-+-", "disabled"), scale=.10, command=self.addCharisma)
        self.btnCharismaPlus['text_scale'] = 0.50
        self.btnCharismaPlus['frameSize'] = (1.5,2.5,-4,-3)
        self.btnCharismaPlus['text_pos'] = (2,-3.6)
        
        self.btnEnd = DirectButton(text = ("Zurueck", "Zurueck", "-Zurueck-", "disabled"), scale=.10, command=self.back)
        self.btnEnd['text_scale'] = 0.50
        self.btnEnd['frameSize'] = (-2,2,-6,-5)
        self.btnEnd['text_pos'] = (0,-5.6)
        
    def back(self):
        self.CGame.request("GameMenue",self.CActor,self.CGame)
        
    def addStrength(self):
        if(self.CActor.getPoints()>0):
            self.CActor.setStrength(self.CActor.getStrength()+1)
            self.txtStrength.setText("Strength: "+ str(self.CActor.getStrength()))
            self.CActor.setPoints(self.CActor.getPoints()-1)
            self.txtPoints.setText("Punkte zu vergeben: "+ str(self.CActor.getPoints()))
        
    def addAgility(self):
        if(self.CActor.getPoints()>0):
            self.CActor.setAgility(self.CActor.getAgility()+1)
            self.txtAgility.setText("Agility: "+ str(self.CActor.getAgility()))
            self.CActor.setPoints(self.CActor.getPoints()-1)
            self.txtPoints.setText("Punkte zu vergeben: "+ str(self.CActor.getPoints()))                          
                                     
    def addStamina(self):
        if(self.CActor.getPoints()>0):
            self.CActor.setStamina(self.CActor.getStamina()+1)
            self.txtStamina.setText("Stamina: "+ str(self.CActor.getStamina()))
            self.CActor.setPoints(self.CActor.getPoints()-1)
            self.txtPoints.setText("Punkte zu vergeben: "+ str(self.CActor.getPoints()))
            
    def addCharisma(self):
        if(self.CActor.getPoints()>0):
            self.CActor.setCharisma(self.CActor.getCharisma()+1)
            self.txtCharisma.setText("Charisma: "+ str(self.CActor.getCharisma()))
            self.CActor.setPoints(self.CActor.getPoints()-1)
            self.txtPoints.setText("Punkte zu vergeben: "+ str(self.CActor.getPoints()))