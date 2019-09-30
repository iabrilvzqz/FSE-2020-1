# bibliotecas
import sys # manejar parametros de consola
import montajeUsb # montaje de USB

pathUSB = montajeUsb.mountUSB()

file = open(pathUSB + "/" + sys.argv[1] + ".csv", "w")

for i in range(int(sys.argv[2])):
	file.write(str(i) + ",Hola USB,data" + str(i) + "\n")

file.close()