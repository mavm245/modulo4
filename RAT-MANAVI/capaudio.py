#!/usr/bin/python

###############################
#  Modulo captura de audio    #
#  Proyecto de Modulo 4       #
#	 		      #
#      nmorales               #
#      varteaga               #
#      mvasquez               #
###############################

import os
import datetime
import sys

def audio(arg1):
	x = datetime.datetime.now()
	x = x.isoformat()
	y = arg1
	comando = "arecord -d " + y +" -f cd -t wav "+ x + ".wav"
	os.system(comando + "> /dev/null 2>&1")

#audio(sys.argv[1])
