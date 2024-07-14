import socket
import config as config
import ast
import network as net
from network import Message

machine_number = int(input("Numero da Maquina: "))
UDP_IP = "localhost"

RCV_PORT, SND_PORT = config.config_machine(machine_number)

print ("SEND", SND_PORT, "RECEIVE", RCV_PORT)

clA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clA.bind((UDP_IP, RCV_PORT))

if machine_number == 1:
    
    text = input("Digite Mensagem\n")
    message = Message(machine_number, int(input("Digite Destinatario:")), text, 0) 
    net.messageTo(message, UDP_IP, SND_PORT)
    
    while True:
        data, addr = clA.recvfrom(1024)
        if data:
            message = ast.literal_eval(data.decode())
            if message["origem"] == machine_number and message["recebido"] == 1:
                print("Enviado com Sucesso")
            else:
                print("Caguei no peidar")

while True:
    data, addr = clA.recvfrom(1024)
    if data:
        message = ast.literal_eval(data.decode())
        if message["destino"] == machine_number:
            print(message["msg"])
            message["recebido"] = 1
            net.messageTo(message, UDP_IP, SND_PORT)
        else:
            net.messageTo(message, UDP_IP, SND_PORT)
