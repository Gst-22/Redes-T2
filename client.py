import socket
import config as config
import ast
import gameplay as game
import network as net
from network import Message

machine_number = int(input("Numero da Maquina: "))
UDP_IP = "localhost"

RCV_PORT, SND_PORT = config.config_machine(machine_number)

print ("SEND", SND_PORT, "RECEIVE", RCV_PORT)

rcv_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcv_skt.bind((UDP_IP, RCV_PORT))

if machine_number == 1: #Maquina 1 inicia o jogo
    carteado = game.sorteiaMaos(4)
    for i in range(2):
        message = Message(0, machine_number, i+2, str(carteado[i+2]), 0)
        enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)
        if enviado:
            print("Enviado para " + str(i+2))
        else:
            print("Falha ao enviar.")
            exit
    
    net.passToken(UDP_IP, SND_PORT)

while True: #espero mensagem, envio confirmação.
    data, addr = rcv_skt.recvfrom(1024)
    if data:
        message = ast.literal_eval(data.decode())
        
        if message["token"] == 1:
            text = input("Digite Mensagem\n")
            my_message = Message(0, machine_number, int(input("Digite Destinatario:")), text, 0)
            enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)
            if enviado:
                net.passToken(UDP_IP, SND_PORT)
            else:
                print("Falha ao enviar.")
                exit
        
        elif message["destino"] == machine_number:
            print(message["msg"])
            message["recebido"] = 1
            net.messageTo(message, UDP_IP, SND_PORT)
        
        else:
            net.messageTo(message, UDP_IP, SND_PORT)
