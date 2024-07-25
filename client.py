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

if machine_number == 1: #Maquina 1 inicia o jogo
    
    text = input("Digite Mensagem\n")
    message = Message(0, machine_number, int(input("Digite Destinatario:")), text, 0)
    net.messageTo(message, UDP_IP, SND_PORT)
    #Envia mensagem inicial
    
    round = True
    #Espera confimação de recebimento.
    while round:
        data, addr = clA.recvfrom(1024)
        if data:
            message = ast.literal_eval(data.decode())
            if message["origem"] == machine_number and message["recebido"] == 1:
                print("Enviado com Sucesso")
                token = Message(1, 0, 0, 0, 0)
                net.messageTo(token, UDP_IP, SND_PORT)
                round = False
            else:
                print("Caguei no peidar")

while True: #espero mensagem, envio confirmação.
    data, addr = clA.recvfrom(1024)
    if data:
        message = ast.literal_eval(data.decode())
        
        if message["token"] == 1:
            text = input("Digite Mensagem\n")
            message = Message(0, machine_number, int(input("Digite Destinatario:")), text, 0)
            net.messageTo(message, UDP_IP, SND_PORT)
            round = True

            while round:
                data, addr = clA.recvfrom(1024)
                if data:
                    message = ast.literal_eval(data.decode())
                    if message["origem"] == machine_number and message["recebido"] == 1:
                        print("Enviado com Sucesso")
                        token = Message(1, 0, 0, 0, 0)
                        net.messageTo(token, UDP_IP, SND_PORT)
                        round = False
                    else:
                        print("Caguei no peidar")
        
        if message["destino"] == machine_number:
            print(message["msg"])
            message["recebido"] = 1
            net.messageTo(message, UDP_IP, SND_PORT)
        
        else:
            net.messageTo(message, UDP_IP, SND_PORT)
