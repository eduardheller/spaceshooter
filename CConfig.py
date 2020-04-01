#!/usr/bin/env python

import direct.directbase.DirectStart
from direct.filter.CommonFilters import CommonFilters
import sys

def runConfiguration():
    
    #Grundeinstellungen
    base.setFrameRateMeter(True)
    base.setBackgroundColor(0,0,0)
    
    #Bloom Filter
    CFilters = CommonFilters(base.win, base.cam)
    filterok = CFilters.setBloom(blend=(0,0,0,1),desat=-0.1,mintrigger=0.0, intensity=6.0, size="small")
    
    if filterok == 0:
        print "Deine Grafikkarte unterstuetzt kein Bloom Filter: Shader Error"
        
        
        