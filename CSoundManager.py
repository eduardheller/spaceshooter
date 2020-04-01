#!/usr/bin/env python

import direct.directbase.DirectStart

class SoundMng:
    
    def __init__(self):
        self.sndMusic = loader.loadSfx("music/behind-the-shadows.mp3")
        self.sndMusic.setVolume(1)
        self.sndMusic.setLoop(True)
        
        self.sndResult = loader.loadSfx("music/solution.mp3")
        
        self.sndTipp = loader.loadSfx("sounds/sound56.wav")
        
        self.sndCrit = loader.loadSfx("sounds/sound3.mp3")
        
        
        self.sndFlyAmbience = loader.loadSfx("sounds/fly.wav")
        self.sndFlyAmbience.setLoop(True)

        self.sndFlyAmbience.setPlayRate(5.5)
        
        self.sndHit = loader.loadSfx("sounds/expl.wav")
        self.sndHit.setVolume(0.2)
        self.sndExplosion = loader.loadSfx("sounds/expl.wav")
        self.sndExplosion.setVolume(0.5)
        
       
                
    