import os
import time
import socket
from subprocess import Popen, PIPE

print("Compilation...")
os.system("mkdir obj")
os.system("mkdir bin")
os.system("make")
print("Démarrage du programme")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

print("Fichier à parser \n")
fileName = str(input())
print("Port serveur \n")
port = int(input())
verboseChoise = input("Mode verbeux ? (y/n) \n")
if verboseChoise == "y":
    verbose = 1
else:
    verbose = 0
print("Nombre de run \n")
run = int(input())

f = open("Files/"+fileName, "r")
nbNode = 0
for x in f:
  if x.startswith("p"):
        nbNode = int(x.split(" ")[2])
        break

print("Besoin de",nbNode , "clients")

for i in range(run):
  file = '"' + fileName + '"'
  #print("[Runner] Démarrage du serveur sur " + str(port))
  call = "./bin/serverMultiplex " + str(port+i*1000) + " " + file + " " + str(verbose) + " &"
  os.system(call)    

time.sleep(1)
for i in range(run):
  for x in range(0,nbNode) :
    #time.sleep(0.005)
    tmpPort = port+x+1+(i*1000)
    #print("[Runner] Démarrage du client" , x , "sur" , str(s.getsockname()[0]) + ":" + str(tmpPort) ,"au serveur")
    call = "./bin/client "+ str(s.getsockname()[0]) + " " + str(port+i*1000) + " " + str(s.getsockname()[0]) + " " + str(tmpPort) + " " + str(verbose) + " &"
    os.system(call)

