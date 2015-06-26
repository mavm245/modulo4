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

x = datetime.datetime.now()
x = x.isoformat()
if len(sys.argv) >= 2:
	y = sys.argv[1]
	comando = "streamer -t 0:0:"+ y + " -c /dev/video0 -f rgb24 -F mono16 -r 3 -o " + x + ".avi"
	#print(comando)
else:
        print "Este programa necesita un parametro que indique el tiempo (Segundos)"

os.system(comando)

