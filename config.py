#!/usr/bin/env python

from panda3d.core import loadPrcFileData 
import direct.directbase.DirectStart
from direct.filter.CommonFilters import CommonFilters
import sys

def runConfiguration():
    
    #Grundeinstellungen

    base.setFrameRateMeter(True)
    base.setBackgroundColor(0,0,0)
    
    #Bloom Filter
    CFilters = CommonFilters(base.win, base.cam)
    filterok = CFilters.setBloom(blend=(0,0,0,1),desat=-0.6,mintrigger=0.0, intensity=6.0, size="medium")
    
    if filterok == 0:
        print "Deine Grafikkarte unterstuetzt kein Bloom Filter: Shader Error!"
        
        
        