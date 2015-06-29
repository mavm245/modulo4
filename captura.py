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

#una captura cada tiempo
if arg == '-t':
	y = int(sys.argv[2])
	while('TRUE'):
		x = datetime.datetime.now()
		x= x.isoformat()
		comando = "convert archivo.xwd " + x + ".png"
		os.system("xwd -root -screen > archivo.xwd")
		os.system(comando)
		os.system("rm archivo.xwd")
		time.sleep(y)
#numero de capturas cada segundo
if arg == '-n':
        y = int(sys.argv[2])
        for i in range(0,y):
                x = datetime.datetime.now()
                x= x.isoformat()
                comando = "convert archivo.xwd " + x + ".png"
                os.system("xwd -root -screen > archivo.xwd")
                os.system(comando)
                os.system("rm archivo.xwd")
		time.sleep(1)
#menu ayuda
if arg == '-h':
	print "\nOpciones disponibles"
	print "-n	Numero de capturas cada segundo"
	print "Ejemplo: captura.py -n 5 >>>> 5 capturas cada segundo\n"
        print "-t 	Tomar una captura cada cierto tiempo(Segundos)"
        print "Ejemplo: captura.py -t 5 >>>> 1 captura cada 5 segundos"

