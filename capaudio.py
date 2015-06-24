###############################
#  Modulo captura de audio    #
#  Proyecto de Modulo 4       #
#	 		      #
#      nmorales               #
#      varteaga               #
#      mvasquez               #
###############################

#!/usr/bin/python
import os
import datetime
import sys

x = datetime.datetime.now()
x = x.isoformat()
if len(sys.argv) >= 2:
	y = sys.argv[1]
	comando = "arecord -d " + y +" -f cd -t wav "+ x + ".wav"
	#print(comando)
else:
        print "Este programa necesita un parametro"

os.system(comando)

