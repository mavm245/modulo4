#!/usr/bin/python

###############################
#  Modulo captura de video    #
#  Proyecto de Modulo 4       #
#	 		      #
#      nmorales               #
#      varteaga               #
#      mvasquez               #
###############################

import os
import datetime
import sys

def video(arg1):
	x = datetime.datetime.now()
	x = x.isoformat()
	y = arg1
	comando = "streamer -t 0:0:"+ y + " -c /dev/video0 -f rgb24 -F mono16 -r 3 -o " + x + ".avi"
	os.system(comando)

if len(sys.argv) == 2:
	arg1 = sys.argv[1]
	video(arg1)
else:
	print "Este programa necesita un parametro que indique el tiempo (Segundos)"
