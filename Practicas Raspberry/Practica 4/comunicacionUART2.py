import serial # biblioteca necesaria para el uso de la comunciación serrial con UART

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout = 3.0) # se abre el puerto, indicando el puerto, baudrate y un valor de tiempo de lectura

# función que lee una cadena, caracter por caracter de la comunicación UART
def readlineCR(port):
	rv=""
	while True:
		ch = port.read()
		rv += ch
		
		if ch=='\r' or ch=='':
			cadena = rv.split(",") # se separa la cadena por las comas de entrada
			return cadena

while True:
	try:
		rcv = readlineCR(port) # se lee la cadena 
		if len(rcv) == 4:
			# se imprime en la PC con el formato especificado
			# usando el puerto UART
			port.write("\r\nNumero entero: %s"%(str(rcv[0])))
			port.write("\r\nIniciales: %s"%(str(rcv[1])))
			port.write("\r\nBandera: %s"%(str(rcv[2])))
			port.write("\r\nVoltaje: %s"%(str(rcv[3])))
		
	except:
		pass
