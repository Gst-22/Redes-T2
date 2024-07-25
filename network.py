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
                print("Sucesso!")
                return 1

def passToken(UPD_IP, SND_PORT):
    token = Message(1, 0, 0, 0, 0)
    messageTo(token, UPD_IP, SND_PORT)