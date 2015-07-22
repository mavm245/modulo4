//Requeimientos:
$ sudo apt-get install sshpass

//Instalación Atacante
$ ssh-keygen -b 4096 -t rsa -N '' -f llaves
$ sshpass -p 'hola123,' ssh-copy-id koala@192.168.222.151

//Conexión Atacante
$ ssh koala@192.168.222.151
$ scp origen destino
