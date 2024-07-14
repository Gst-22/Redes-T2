import socket
import config as config
import ast
import network as net

machine_number = int(input("Numero da Maquina: "))
UDP_IP = "localhost"

RCV_PORT, SND_PORT = config.config_machine(machine_number)

print ("SEND", SND_PORT, "RECEIVE", RCV_PORT)

clA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clA.bind((UDP_IP, RCV_PORT))

if machine_number == 1:
    message = input("Digite banana\n")
    net.mesageTo(message.encode(), machine_number, 2, UDP_IP, SND_PORT, RCV_PORT)

while True:
    data, addr = clA.recvfrom(1024)
    if data:
        message = ast.literal_eval(data.decode())
        if message["destino"] == machine_number:
            print(message["msg"].decode())
        else:
            clB.sendto(data, (UDP_IP, SND_PORT))
            