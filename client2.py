
# importing socket module 
import socket 
  
UDP_IP1 = "localhost"
UDP_PORT1 = 8080

UDP_IP2 = "localhost"
UDP_PORT2 = 8081

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((UDP_IP1, UDP_PORT1))
s1.listen()


sndr, addr1 = s1.accept()
print (f"Conectado com {addr1}")

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s2.connect((UDP_IP2, UDP_PORT2))

print (f"Conectado com servidor")