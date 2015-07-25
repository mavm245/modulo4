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
#debian 7 y 8
#       comando = "streamer -t 0:0:"+ y + " -c /dev/video0 -f rgb24 -F mono16 -r 3 -o " + x + ".avi"
#debian 6
        comando = "ffmpeg -f video4linux2 -s 640x480 -r ntsc -i /dev/video0 -f oss -i /dev/dsp -t 00:00:" + y + " -qscale 3 /tmp/" + x + ".mpeg"
        os.system(comando + "> /dev/null 2>&1")
