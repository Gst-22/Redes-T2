import socket

class Message:
    def __init__(self, origem, destino, msg, recebido):
        self.origem = origem    #quem esta enviando
        self.destino = destino  #quem recebe
        self.msg = msg
        self.recebido = recebido    #confirmacao de recebimento da carta

    def __str__(self):
        return str(self.__dict__)

def mesageTo(data, sender_number, receiver_number , UPD_IP, SND_PORT, RCV_PORT):

    message = Message(sender_number, receiver_number, data, 0) 

    send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send.sendto(str(message).encode("utf-8"), (UPD_IP, SND_PORT))
    
    send.close()

