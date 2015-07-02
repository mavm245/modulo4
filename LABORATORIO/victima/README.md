#Instalador del RAT

Este script se ejecutará del lado del cliente e instalará todas las dependencias necesarias para su correcto funcionamiento.
	
- Para que funcione es instalador es necesario instalar el modulo de linux rootkit.ko (Fundamental) antes de ejecutar el script.

	* Requerimientos:
		- El paquete con los scripts pertenecientes a los modulos del RAT.
		- Conexión a internet para la descarga de las dependencias.
		- Modulo de rootkit

	* Pasos que sigue el instalador:

		* Se verifica que se cuente con el paquete necesario para la instalación (RAT-MANAVI.tar.gz), 
		en caso de que no se cuente se descargara de un servidor malicioso.

		* Se desempaqueta el archivo en el directorio especificado en el script.

		* Directorio donde se encuentran los archivos de instalación:
			- $HOME/.rat/manavi/RAT-MANAVI

		* Se crea un usuario que se utilizara como repositorio de todas las capturas realizadas por el atacante donde se podran recuperar
			- Usuario creado:
				manavi
			- Contraseña:
				manavi
	
		* Directorio creado para la recolección de informacion por parte del RAT:
			- /home/user/manavi
