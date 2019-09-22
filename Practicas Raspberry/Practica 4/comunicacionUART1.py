import serial # biblioteca necesaria para el uso de la comunciación serrial con UART

ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1) # se abre el puerto, indicando el puerto, baudrate y un valor de tiempo de lectura

for i in range(0, 16):
	# Escritura del mensaje
	ser.write(str(i).encode(encoding='UTF-8', errors='strict'))
	ser.write(b': FSE 2020-1 Comunicacion UART Rpi-FSE\n')

ser.close() # se cierra el puerto
