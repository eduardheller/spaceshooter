#!/usr/bin/env python

import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from CGameMenue import GameMenue
from CActor import Actor

from direct.task.Task import Task
from pandac.PandaModules import Filename,Fog
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenImage import OnscreenImage

from random import randint, choice, random
import sys,os

mydir = os.path.abspath(sys.path[0])
mydir = Filename.fromOsSpecific(mydir).getFullpath()
font = loader.loadFont(mydir+"/fonts/ocra.ttf")


class MainMenue:
    
    def __init__(self,state):
        
        
        self.imgBackground = OnscreenImage(image = 'images/background.png', pos = (0, 0,0),scale=(1.333,0,1))
        
        self.CGame = state
        self.CActor = Actor("models/whati")
        

        self.btnNewGame = DirectButton(text = ("New Game", "New Game", "New Game<", "disabled"),relief=None, scale=.10, command=self.newGame)
        self.btnNewGame['text_scale'] = 0.32
        self.btnNewGame['frameSize'] = (-2.5,1.5,0.86,1.86)
        self.btnNewGame['text_pos'] = (-0.51,1.26)
        self.btnNewGame['text_font'] = font
        self.btnNewGame['text_fg'] = (255,255,255,1)
        
        #self.btnLoadGame = DirectButton(text = ("Spiel Laden", "Spiel Laden", "Spiel Laden<", "disabled"), relief=None,scale=.10, command=self.newGame)
        #self.btnLoadGame['text_scale'] = 0.32
        #self.btnLoadGame['frameSize'] = (2.2,6.2,-0.75,0.25)
        #self.btnLoadGame['text_pos'] = (4.2,-.35)
        #self.btnLoadGame['text_fg'] = (255,255,255,1)
        #self.btnLoadGame['text_font'] = font
        
        #self.btnOption = DirectButton(text = ("Multiplayer", "Multiplayer", "Multiplayer<", "disabled"),relief=None, scale=.10, command=self.newGame)
        #self.btnOption['text_scale'] = 0.32
        #self.btnOption['frameSize'] = (2.25,6.25,-2.85,-1,85)
        #self.btnOption['text_pos'] = (4.15,-2.35)        
        #self.btnOption['text_fg'] = (255,255,255,1)
        #self.btnOption['text_font'] = font
        
        self.btnEnd = DirectButton(text = ("End Game", "End Game", "End Game<", "disabled"),relief=None, scale=.10, command=self.endGame)
        self.btnEnd['text_scale'] = 0.32
        self.btnEnd['frameSize'] = (3.15,7.15,-6.13,-5.13)
        self.btnEnd['text_pos'] = (5.15,-6.13)
        self.btnEnd['text_fg'] = (255,255,255,1)
        self.btnEnd['text_font'] = font
        
        
    def newGame(self):
        self.CGame.request("GameMenue",self.CActor,self.CGame)
        #taskMgr.remove("menueLoop")
    def endGame(self):
        sys.exit()
        
        
        