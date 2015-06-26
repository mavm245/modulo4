#!/usr/bin/python

###############################
# Modulo captura de pantalla  #
# Proyecto de Modulo 4        #
#	 		      #
#      nmorales               #
#      varteaga               #
#      mvasquez               #
#			      #
###############################

import os
import datetime
import time
import sys

arg = sys.argv[1]

if arg == '-t':
	y = int(sys.argv[2])
	while(true):
		x = datetime.datetime.now()
		x= x.isoformat()
		comando = "convert archivo.xwd " + x + ".png"
		os.system("xwd -root -screen > archivo.xwd")
		os.system(comando)
		os.system("rm archivo.xwd")
		time.sleep(y)

if arg == '-n':
        y = int(sys.argv[2])
        for i in range(1,y):
                x = datetime.datetime.now()
                x= x.isoformat()
                comando = "convert archivo.xwd " + x + ".png"
                os.system("xwd -root -screen > archivo.xwd")
                os.system(comando)
                os.system("rm archivo.xwd")
		time.sleep(1)

if arg == '-h':
	print "\nOpciones disponibles"
	print "-n	Numero de capturas cada segundo"
	print "Ejemplo: captura.py -n 5 >>>> 5 capturas cada segundo\n"
        print "-t 	Tomar una captura cada cierto tiempo(Segundos)"
        print "Ejemplo: captura.py -t 5 >>>> 1 captura cada 5 segundos"

