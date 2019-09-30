import serial # biblioteca necesaria para el uso de la comunciación serrial con UART
from time import sleep

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0) # se abre el puerto, indicando el puerto, baudrate y un valor de tiempo de lectura

# función que lee una cadena, caracter por caracter de la comunicación UART
def readlineCR(port):
	rv=""
	while True:
		ch = port.read().decode("utf-8")
		rv += ch
		if ch=='\n' or ch=='':
			cadena = rv.split(",") # se separa la cadena por las comas de entrada
			return cadena
while True:
	try:
		rcv = readlineCR(port) # se lee la cadena
		if len(rcv) == 3:
			# se imprime en la PC con el formato especificado
			# usando el puerto UART
			port.write(("\r\nVoltaje: " + rcv[0]).encode())
			port.write(("\r\nT [Kº]:  " + rcv[1]).encode())
			port.write(("\r\nT [Cº]:  " + rcv[2]).encode())

	except:
		print("ERROR")
		pass
