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

arg1 = sys.argv[1]
arg2 = sys.argv[2]

def tiempo(arg1,arg2):
	z=0
	#una captura cada tiempo
	if arg1 == '-t':
		y = int(arg2)
		while(z!=5):
			x = datetime.datetime.now()
			x= x.isoformat()
			comando = "convert archivo.xwd " + x + ".png"
			os.system("xwd -root -screen > archivo.xwd")
			os.system(comando)
			os.system("rm archivo.xwd")
			time.sleep(y)
			z=z+1
	#numero de capturas cada segundo
	if arg1 == '-n':
		y = int(arg2)
		for i in range(0,y):
			x = datetime.datetime.now()
			x= x.isoformat()
			comando = "convert archivo.xwd " + x + ".png"
			os.system("xwd -root -screen > archivo.xwd")
			os.system(comando)
			os.system("rm archivo.xwd")
			time.sleep(1)
	#menu ayuda
	if arg1 == '-h':
		print "\nOpciones disponibles"
		print "-n	Numero de capturas cada segundo"
		print "Ejemplo: captura.py -n 5 >>>> 5 capturas cada segundo\n"
		print "-t 	Tomar una captura cada cierto tiempo(Segundos)"
		print "Ejemplo: captura.py -t 5 >>>> 1 captura cada 5 segundos"

tiempo(arg1,arg2)
