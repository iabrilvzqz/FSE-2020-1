""" Materia: Fundamentos de Sistemas Embebidos
	Semestre: 2020-1
	Alumnos: 	Arellano Yeo Nomar Alberto
				Hernández García Luis Angel
				Vázquez Sánchez Ilse Abril

Descripción: Primer examen parcial. Programa para la RPi, encargada de recibir los datos
enviados por el ESP32 en una cadena que contiene el voltaje [mV], grados [K] y grados [C] 
separados por comas y, envía estos datos en un formato más amigable a la computadora que 
muestra la información en un monitor serial
	Voltaje [mV]: 
	T [ºK]:
	T [ºC]: 
"""

import serial
from time import sleep

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

def readlineCR(port):
	rv=""
	while True:
		ch = port.read().decode("utf-8")
		rv += ch
		if ch=='\n' or ch=='':
			cadena = rv.split(",")
			return cadena
while True:
	try:
		rcv = readlineCR(port)
		if len(rcv) == 3:
			port.write(("\r\nVoltaje [mV]: " + rcv[0]).encode())
			port.write(("\r\nT [Kº]:  " + rcv[1]).encode())
			port.write(("\r\nT [Cº]:  " + rcv[2]).encode())

	except:
		print("ERROR")
		pass
