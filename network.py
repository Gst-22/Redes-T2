import socket

class Message:
    def __init__(self, token, origem, destino, msg, recebido):
        self.token = token #A mensagem é um token?
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