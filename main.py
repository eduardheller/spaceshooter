#!/usr/bin/env python

from CGamestate import Gamestate
from CMainMenue import MainMenue 
import config

config.runConfiguration()

CGame = Gamestate()

CGame.request("MainMenue",CGame)

run()