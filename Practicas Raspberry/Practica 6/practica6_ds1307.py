import subprocess
import sys # manejar parametros de consola
import montajeUSB # montaje de USB
pathUSB = montajeUSB.mountUSB()
file = open(pathUSB + "/" + sys.argv[1] + ".csv", "a")

while True:
        result = subprocess.getoutput('sudo hwclock -r')
        comando = result.split(" ")
        fecha = comando[0].split("-")#Almacena anio, mes y dia
        tiempos = comando[1].split(".") #Almacena segunda parte del primer comando
        tiempo = tiempos[0].split(":") #Almacena horas, minutos y segundos
        file.write(fecha[0]+","+fecha[1]+","+fecha[2]+","+tiempo[0]+","+tiempo[1]+","+tiempo[2]+ "\n")
        print("Imprimiendo")

file.close()
