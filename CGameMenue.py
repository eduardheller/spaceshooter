#!/usr/bin/env python

import direct.directbase.DirectStart
from direct.gui.DirectGui import *


class GameMenue:
    
    def __init__(self,actor,state):
        
        self.CActor = actor
        self.CGame = state
        self.btnMissionStart = DirectButton(text = ("Next Mission", "Next Mission", "-Next Mission-", "disabled"), scale=.10, command=self.startMission)
        self.btnMissionStart['text_scale'] = 0.50
        self.btnMissionStart['frameSize'] = (-2,2,0,1)
        self.btnMissionStart['text_pos'] = (0,0.4)
        
        self.btnShipShop = DirectButton(text = ("Shop", "Shop", "-Shop-", "disabled"), scale=.10, command=self.shipMenue)
        self.btnShipShop['text_scale'] = 0.50
        self.btnShipShop['frameSize'] = (-2,2,-2,-1)
        self.btnShipShop['text_pos'] = (0,-1.6)
        
        self.btnSkill = DirectButton(text = ("Abilities", "Abilities", "-Abilities-", "disabled"), scale=.10, command=self.skillMenue)
        self.btnSkill['text_scale'] = 0.50
        self.btnSkill['frameSize'] = (-2,2,-4,-3)
        self.btnSkill['text_pos'] = (0,-3.6)        
        
        self.btnEnd = DirectButton(text = ("Menue", "Menue", "-Menue-", "disabled"), scale=.10, command=self.newGame)
        self.btnEnd['text_scale'] = 0.50
        self.btnEnd['frameSize'] = (-2,2,-6,-5)
        self.btnEnd['text_pos'] = (0,-5.6)
        
        
    def newGame(self):
        self.CGame.request("MainMenue",self.CGame)
        
    def skillMenue(self):
        self.CGame.request("SkillMenue",self.CActor,self.CGame)
        
    def shipMenue(self):
        self.CGame.request("ShipShop",self.CActor,self.CGame)
        
    def startMission(self):
        self.CGame.request("Game",self.CActor,self.CGame)
        
        