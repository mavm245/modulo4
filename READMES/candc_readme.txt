
Este programa debe ejecutarse con una tarea progreama cada cierto tiempo podría ser cada 5 min o 10 min.
comando:

echo "0,10,20,30,40,50 * * * * /candc.py" >> /tmp/tare.txt
crontab -u koala /tmp/tare.txt 
rm /tmp/tare.txt
