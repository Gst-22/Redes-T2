import socket 

machine_number = int(input("Numero da Maquina: "))

UDP_IP = "localhost"
CLA_PORT = 8081
CLB_PORT = 8082


clA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clA.bind((UDP_IP, CLA_PORT))

if machine_number == 1:
    message = input("Digite banana\n")
    clB.sendto(message.encode(),(UDP_IP, CLB_PORT))

while True:
    data, addr = clA.recvfrom(1024)
    if data:
        print(str(data).encode("utf-8"))
        message = input()
        clB.sendto(message.encode(),(UDP_IP, CLB_PORT))
