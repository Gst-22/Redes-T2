import socket 
  
UDP_IP = "localhost"
UDP_PORT = 8081

UDP_IP2 = "localhost"
UDP_PORT2 = 8082
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind((UDP_IP, UDP_PORT))
sock.listen()

sndr, addr = sock.accept()

print (f"Conectado com {addr}")
data = sndr.recv(1024)
print (f"{data!r}")

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s2.connect((UDP_IP2, UDP_PORT2))

print (f"Conectado com servidor")
s2.sendall(b"TESTE 3")