#!/usr/bin/env python

import direct.directbase.DirectStart
from CActor import Actor
from CGameMenue import GameMenue
from CShipShop import ShipShop
from CSkillMenue import SkillMenue
from CWorld import World
from CMainMenue import MainMenue
from direct.fsm import FSM


class Gamestate(FSM.FSM):
    
    def __init__(self):
        FSM.FSM.__init__(self, 'Gamestate')
        self.CMainMenue = None
        self.CGameMenue = None
        self.CWorld = None
        self.CShipShop = None
        self.CSkillMenue = None
        self.level = 1
    
    def enterMainMenue(self,state):
        self.CMainMenue = MainMenue(state)
    
    def exitMainMenue(self):
        self.CMainMenue.btnEnd.destroy()
        #self.CMainMenue.btnLoadGame.destroy()
        self.CMainMenue.btnNewGame.destroy()
        #self.CMainMenue.btnOption.destroy()
        self.CMainMenue.imgBackground.destroy()
        del self.CMainMenue
    
    def enterGameMenue(self,actor,state):
        self.CGameMenue = GameMenue(actor,state)
        
    def exitGameMenue(self):
        self.CGameMenue.btnMissionStart.destroy()
        self.CGameMenue.btnShipShop.destroy()
        self.CGameMenue.btnSkill.destroy()
        self.CGameMenue.btnEnd.destroy()
        del self.CGameMenue
     
    def enterShipShop(self,actor,state):
        self.CShipShop = ShipShop(actor,state)
    
    def exitShipShop(self):
        self.CShipShop.btnEnd.destroy()
        self.CShipShop.btnShieldPlus.destroy()
        self.CShipShop.btnSpeedPlus.destroy()
        self.CShipShop.btnWeaponPlus.destroy()
        self.CShipShop.btnWeaponSpeedPlus.destroy()
        self.CShipShop.optSelectWeapon.destroy()
        self.CShipShop.txtMoney.destroy()
        self.CShipShop.txtShield.destroy()
        self.CShipShop.txtSpeed.destroy()
        self.CShipShop.txtWeaponStr.destroy()
        self.CShipShop.txtWeaponSpeed.destroy()
        self.CShipShop.txtCostsShield.destroy()
        self.CShipShop.txtCostsSpeed.destroy()
        self.CShipShop.txtCostsWeaponSpeed.destroy()
        self.CShipShop.txtCostsWeaponStr.destroy()
        del self.CShipShop
    
    def enterSkillMenue(self,actor,state):
        self.CSkillMenue = SkillMenue(actor,state)
        
    def exitSkillMenue(self):
        self.CSkillMenue.btnStrengthPlus.destroy()
        self.CSkillMenue.btnAgilityPlus.destroy()
        self.CSkillMenue.btnStaminaPlus.destroy()
        self.CSkillMenue.btnCharismaPlus.destroy()
        self.CSkillMenue.btnEnd.destroy()
        self.CSkillMenue.txtStrength.destroy()
        self.CSkillMenue.txtAgility.destroy()
        self.CSkillMenue.txtStamina.destroy()
        self.CSkillMenue.txtCharisma.destroy()
        self.CSkillMenue.txtPoints.destroy()
        del self.CSkillMenue
    
    def enterGame(self,actor,state):
        self.CWorld = World(actor,state,self.level)
        self.level +=1
        
    def exitGame(self):
        
        for bullet in self.CWorld.lbullets:
            bullet.remove()
        for bullet in self.CWorld.lbulletsenemy:
            bullet.remove()
            
        for expl in self.CWorld.lexplosions:
            expl.remove()
        
        self.CWorld.CActor.nActorShip.detachNode()
        
        self.CWorld.CEffects.removeSpaceStars()
        del self.CWorld.CEffects
        del self.CWorld.CEnemy
    
        self.CWorld.CSound.sndMusic.stop()
        self.CWorld.CSound.sndFlyAmbience.stop()
        self.CWorld.CSound.sndResult.stop()
        del self.CWorld.CSound
        
        del self.CWorld.CTex
        
        self.CWorld.txtresultcash.destroy()
        self.CWorld.txtresultkills.destroy()
        self.CWorld.txtresultleft.destroy()
        self.CWorld.txtresultlevel.destroy()
        self.CWorld.txtresultmessage.destroy()
        self.CWorld.txtresultmission.destroy()
        del self.CWorld
