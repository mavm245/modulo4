#!/usr/bin/python
import os
import datetime

x = datetime.datetime.now()
x = x.isoformat()
comando = "convert archivo.xwd " + x + ".png"
#print(comando)

os.system("xwd -root -screen > archivo.xwd")
os.system(comando)
os.system("rm archivo.xwd")
