//Requeimientos:
$ sudo apt-get install sshpass

//Instalación Atacante
$ ssh-keygen -q -b 4096 -t rsa -N '' -f /home/sysadmin/.ssh/id_rsa
$ sshpass -p 'hola123,' ssh-copy-id manavi@192.168.222.9

//Conexión Atacante
$ ssh manavi@192.168.222.9
$ scp origen destino
