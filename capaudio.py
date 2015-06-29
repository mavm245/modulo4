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
	os.system(comando)

if len(sys.argv) == 2:
	arg1 = sys.argv[1]
	audio(arg1)
else:
        print "Este programa necesita un parametro"
