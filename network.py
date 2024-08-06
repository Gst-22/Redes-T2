import socket
import ast

class Message:
    def __init__(self, type, origem, destino, msg, recebido):
        self.type = type #A mensagem é um token?
        self.origem = origem    #quem esta enviando
        self.destino = destino  #quem recebe
        self.msg = msg
        self.recebido = recebido    #confirmacao de recebimento da carta

    def __str__(self):
        return str(self.__dict__)

def set_configs (machine_number):
    config = open("config.txt", "r")

    cnfg_txt = config.readlines()
    UDP_IP = cnfg_txt[machine_number * 4 - 4].strip()
    MDP_IP = cnfg_txt[machine_number * 4 - 3].strip()
    PORT_RCV = int(cnfg_txt[machine_number * 4 - 2]) 
    PORT_SND = int(cnfg_txt[machine_number * 4 - 1])

    return (PORT_RCV, PORT_SND, UDP_IP, MDP_IP)

def messageTo(message, UPD_IP, SND_PORT):

    send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send.sendto(str(message).encode("utf-8"), (UPD_IP, SND_PORT))

    send.close()

def ringMessage(message, machine_number, UPD_IP, SND_PORT, RCV_SKT):

    messageTo(message, UPD_IP, SND_PORT)
    #Envia mensagem inicial
    
    #Espera confimação de recebimento.
    while True:
        data, addr = RCV_SKT.recvfrom(1024)
        if data:
            message = ast.literal_eval(data.decode())
            if message["origem"] == machine_number and (message["recebido"] == 1 or message["recebido"] == 3):
                return message["msg"]