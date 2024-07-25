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

maoNumerica = []

if machine_number == 1: #Maquina 1 inicia o jogo
    
    carteado = game.sorteiaMaos(4)#Cria carteado.
    maoNumerica = carteado[0]#Minha mão
    print(maoNumerica)

    for i in range(3):#Distribui Cartas
        message = Message(2, machine_number, i+2, ' '.join(map(str, carteado[i+1])), 0)
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
        
        if message["type"] == 1: #Recebi o token, é minha vez.
            
            select = int(input("Escolha uma carta"))
            while select not in maoNumerica:
                select = int(input("Escolha uma carta"))

            my_message = Message(3, machine_number, 5, select, 0)
            
            enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)
            if enviado:
                net.passToken(UDP_IP, SND_PORT)
            else:
                print("Falha ao enviar.")
                exit
        
        elif message["destino"] == machine_number: #Essa mensagem é pra mim
            
            message["recebido"] = 1
            net.messageTo(message, UDP_IP, SND_PORT)

            match message["type"]: 
                case 2:
                    maoNumerica = [int(s) for s in str(message["msg"]).split() if s.isdigit()]
                    print(maoNumerica)
                case 3:
                    print(int(message["msg"]))
                case _:
                    print("Poop")
        
        elif message["destino"] == 5:
            
            message["recebido"] += 1
            net.messageTo(message, UDP_IP, SND_PORT)

            print(str(message["origem"]) + " jogou um " + str(message["msg"]) + " confirmado: " + str(message["recebido"]))

        else: #Mensagem para outra pessoa, passa adiante.
            net.messageTo(message, UDP_IP, SND_PORT)
