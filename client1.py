import socket 
  
UDP_IP = "localhost"
UDP_PORT = 8080

UDP_IP2 = "localhost"
UDP_PORT2 = 8082

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((UDP_IP, UDP_PORT))

print (f"Conectado com servidor")

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.bind((UDP_IP2, UDP_PORT2))
sock2.listen()

sndr, addr = sock2.accept()
print (f"Conectado com {addr}")