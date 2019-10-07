"""
	Programa para montar y desmontar unidades flash USB
	Sólo funciona para un solo dispositivo, el que se encuentre asociado a sdb1
"""

# Bibliotecas para ejecutar comandos shell
import subprocess
import os

# Función que busca el uuid que se encuentra a asociado a sdb1
# recibe la cadena del resultado de ejecutar el comando 'ls -l /dev/disk/by-uuid'
# regresa el uuid
def searchUUID(l):
	for i in range(len(l)):
		if l[i] == '../../sda1':
			return i - 2

# función que monta el dispositivo usb
def mountUSB():
	# este comando busca los discos conectados a PC
	cmd = ['ls','-l','/dev/disk/by-uuid']
	result = subprocess.run(cmd, stdout=subprocess.PIPE)
	result = result.stdout.decode('utf-8').replace("\n"," ").split(' ')

	uuid = result[searchUUID(result)] # se busca el uuid del dispositivo USV

	# se verifica si el montaje ya se ha realizado previamente 
	cmd = ['ls','/media/' + uuid]
	result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = result.communicate() # output y error
	if len(e.decode("utf-8")) > 0: # si la longitud del error es mayor a cero significa que la USB no tiene una carpeta asociada
		os.system("sudo mkdir /media/" + uuid) # se crea la carpeta 
		os.system("sudo chown -R pi:pi /media/" + uuid) # se cambia de propietario y grupo 
	
	# se monta la unidad usb
	os.system("sudo mount /dev/sda1 /media/" + uuid + " -o uid=pi,gid=pi")

	return "/media/" + uuid # se regresa el path de los archivos de la memoria flash USB

def umountUSB(path):
	os.system("sudo umount " + path)