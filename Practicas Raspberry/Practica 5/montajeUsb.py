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
		if len(l[i]) > 9 and l[i][:8] == '../../sd':
			return [i - 2, i]

# función que monta el dispositivo usb
def mountUSB():
	# este comando busca los discos conectados a PC
	cmd = ['ls','-l','/dev/disk/by-uuid']
	result = subprocess.run(cmd, stdout=subprocess.PIPE)
	result = result.stdout.decode('utf-8').replace("\n"," ").split(' ')

	ind = searchUUID(result)
	uuid = result[ind[0]] # se busca el uuid del dispositivo USV
	disk = result[ind[1]]

	# se verifica si el montaje ya se ha realizado previamente 
	cmd = ['ls','/media/' + uuid]
	result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = result.communicate() # output y error
	if len(e.decode("utf-8")) > 0: # si la longitud del error es mayor a cero significa que la USB no tiene una carpeta asociada
		os.system("sudo mkdir /media/" + uuid) # se crea la carpeta 
		os.system("sudo chown -R pi:pi /media/" + uuid) # se cambia de propietario y grupo 
	
	# se monta la unidad usb
	print("Montando memoria USB: " + uuid)
	cmd = ['sudo', 'mount', disk, '/media/' + uuid, '-o', 'uid=pi,gid=pi']
	result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = result.communicate()
	if len(e.decode('utf-8')) > 0: # Si la memoria USB ya está montada
		return "/media/" + uuid
	return "/media/" + uuid # se regresa el path de los archivos de la memoria flash USB

def umountUSB(path):
	os.system("sudo umount " + path)

mountUSB()