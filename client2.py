import socket
import config as config 

machine_number = int(input("Numero da Maquina: "))
UDP_IP = "localhost"

RCV_PORT, SND_PORT = config.config_machine(machine_number)

print ("SEND", SND_PORT, "RECEIVE", RCV_PORT)

clA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clA.bind((UDP_IP, RCV_PORT))

if machine_number == 1:
    message = input("Digite banana\n")
    clB.sendto(message.encode(),(UDP_IP, SND_PORT))

while True:
    data, addr = clA.recvfrom(1024)
    if data:
        print(str(data).encode("utf-8"))
        message = input()
        clB.sendto(message.encode(),(UDP_IP, SND_PORT))