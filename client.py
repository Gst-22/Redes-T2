import socket
import config as config
import ast
import gameplay as game
import network as net
from network import Message
import time

machine_number = int(input("Numero da Maquina: "))
UDP_IP = "localhost"

RCV_PORT, SND_PORT = config.config_machine(machine_number)

print ("SEND", SND_PORT, "RECEIVE", RCV_PORT)

rcv_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcv_skt.bind((UDP_IP, RCV_PORT))

maoNumerica = []
apostasTotais = 0
tamMaoAtual = 0
vidas = [2  , 2 , 2, 2]

souCarteador = False
if machine_number == 1: #Maquina 1 começa como carteado
    souCarteador = True

Jogando = True
while Jogando:

    tamMaoAtual += 1

    rodando = True

    (maiorCarta, lider) = (0, 0)
    pontuacaoRodada = [0, 0, 0, 0]
    apostasDaRodada = [0, 0, 0, 0]

    if souCarteador: #Carteador inicia o jogo
        print("Sou o Carteador")
        carteado = game.sorteiaMaos(tamMaoAtual)#Cria carteado.
        maoNumerica = carteado[machine_number - 1]#Minha mão
        print(maoNumerica)
    
        for i in range(4):#Distribui Cartas
            if i != machine_number - 1 and vidas[i] > 0: #garante que eu não receba minhas próprias cartas
                message = Message(3, machine_number, i+1, ' '.join(map(str, carteado[i])), 0) #mensagem com cartas para cada jogador
                enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt) #envia
        
        for aux in range(3):#Coleta as apostas de todos os jogadores
            i = (machine_number + aux) % 4
            if vidas[i] > 0:    
                message = Message(2, machine_number, i+1, 0, 0)
                enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)#coleta a aposta do jogador i
                print(str(i+1) + " apostou " + str(enviado)) #imprime a aposta do jogador i pro carteador

                apostasDaRodada[i] = int(enviado) #armazena a aposta do jogador i
                apostasTotais += int(enviado) #adiciona a aposta do jogador i ao total

                anuncio = str(i+1) + ' ' + str(apostasDaRodada[i])
                msg_anuncio = Message(6, machine_number, 5, anuncio, 0)
                net.ringMessage(msg_anuncio, machine_number, UDP_IP, SND_PORT, rcv_skt)#anuncia a aposta do jogador i
        
        select = int(input("Faz quantos?\n"))#loop até escolher uma aposta válida
        while apostasTotais +  select == tamMaoAtual or select < 0 or select > tamMaoAtual: #jogadores devem fazer apostas válidas
            select = int(input("Faz quantos?\n"))

        apostasDaRodada[machine_number - 1] = select #armazena a aposta do carteador

        anuncio = str(machine_number) + ' ' + str(select)
        message = Message(6, machine_number, 5, anuncio, 0) #tipo 6 é anuncio de aposta
        net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt) #envia a aposta do carteador
        
        while len(maoNumerica) > 0: #enquanto houver cartas na mão
            (maiorCarta, lider) = (0, 0)
            for aux in range(3):#Coleta as jogadas de todos os jogadores
                i = (machine_number + aux) % 4
                if vidas[i] > 0:
                    message = Message(1, machine_number, i+1, 0, 0)#mensagem de coleta de jogada
                    enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                    jogada = int(enviado) #converte mensagem em jogada
                    if jogada % 10 > maiorCarta % 10: #se a jogada é maior que o melhor, i vira o lider
                        maiorCarta = jogada #melhor carta = carta de i
                        lider = i + 1 #lider = i
                    print(str(i+1) + " jogou " + str(enviado))#imprime a jogada de i pro carteador
                    anuncio = str(i+1) + ' ' + str(jogada) #anuncio de jogada
                    msg_anuncio = Message(5, machine_number, 5, anuncio, 0) #tipo 5 é anuncio de jogada
                    net.ringMessage(msg_anuncio, machine_number, UDP_IP, SND_PORT, rcv_skt)

            print(maoNumerica)
            select = int(input("Escolha uma carta:\n")) #vez do carteador
            while select not in maoNumerica:
                select = int(input("Escolha uma carta:\n"))

            maoNumerica.remove(select) #remove carta da mão
            
            if select % 10 > maiorCarta % 10: #se o carteador jogou uma carta melhor que a melhor carta, ele vira o lider
                maiorCarta = select
                lider = machine_number
            
            anuncio = str(machine_number) + ' ' + str(select) #anuncio de jogada
            msg_anuncio = Message(5, machine_number, 5, anuncio, 0) #tipo 5 é anuncio de jogada
            net.ringMessage(msg_anuncio, machine_number, UDP_IP, SND_PORT, rcv_skt)

            pontuacaoRodada[lider - 1] += 1 #pontua o lider

            my_anuncio = Message(7, machine_number, 5, lider, 0) #anuncia o campeão da rodada
            net.ringMessage(my_anuncio, machine_number, UDP_IP, SND_PORT, rcv_skt)
            print("O jogador " + str(lider) + " pontuou")

        for i in range(4): #para cada jogador, verifica se a aposta foi correta, se não, perde vida
            if apostasDaRodada[i] != pontuacaoRodada[i]:
                vidasPerdidas = abs(apostasDaRodada[i] - pontuacaoRodada[i]) #calcula quantas vidas foram perdidas
                aviso = str(i+1) + " " + str(vidasPerdidas) #a mensagem deve indicar quantas vidas foram perdidas e quem perdeu
                my_message = Message(8, machine_number, 5, aviso, 0)#mensagem de perda de vida
                enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                vidas[i] -= vidasPerdidas #reduz as vidas do jogador i
                print(str(i+1) + " perdeu " + str(vidasPerdidas) + " vidas")
                if vidas[i] <= 0: #se o jogador i ficou sem vidas, ele morre
                    print(str(i+1) + " morreu")

        vivos = 0
        for i in vidas:
            if i > 0:
                vivos += 1
        if vivos <= 1:
            for aux in range(4):
                i = (machine_number + aux) % 4
                message = Message(9, machine_number, 5, 0, 0)
                enviado = net.messageTo(message, UDP_IP, SND_PORT)
            print("Fim de rodada")
            for j in range(4):
                if vidas[j] > 0:
                    print("O jogador " + str(j+1) + " ganhou")
            Jogando = False
            rodando = False
        else:
            souCarteador = False #carteador passa a vez
            token = Message(4, machine_number, 0, 0, 0)#novo carteador
            net.messageTo(token, UDP_IP, SND_PORT)

    while rodando: #espero mensagem, envio confirmação.
        data, addr = rcv_skt.recvfrom(1024)
        if data:
            message = ast.literal_eval(data.decode()) #recebi dados
            
            if message["destino"] == machine_number: #mensagem pra mim
                
                message["recebido"] = 1 #confirmo recebimento
                #Passo a mensagem adiante

                match message["type"]: #que tipo de mensagem?
                    case 1: #Minha vez de jogar
                        
                        print(maoNumerica)
                        select = int(input("Escolha uma carta:\n")) #loop até escolher uma carta válida
                        while select not in maoNumerica:
                            select = int(input("Escolha uma carta:\n"))

                        maoNumerica.remove(select) #removo carta da mão
                        print(maoNumerica)#printo mão atualizada
                                    
                        message["msg"] = str(select)#adiciono minha jogada na mensagem

                    case 2: #Minha vez de apostar
                        select = int(input("Faz quantos?\n"))#loop até escolher uma aposta válida
                        while select > tamMaoAtual or select < 0: #jogadores devem fazer apostas válidas
                            select = int(input("Faz quantos?\n"))
                    
                        message["msg"] = str(select)#adiciono minha aposta na mensagem

                    case 3: # Minhas cartas recebidas
                        maoNumerica = [int(s) for s in str(message["msg"]).split() if s.isdigit()]
                        print(maoNumerica)

                    case _:
                        print("Poop")
            
                net.messageTo(message, UDP_IP, SND_PORT)
            
            elif message["destino"] == 5: #mensagem para todos.
                
                message["recebido"] += 1 #aumento o recebimento
                #Passo a mensagem adiante

                match message["type"]: #que tipo de mensagem?
                    case 5: #anuncio de jogada
                        (jogador, jogada) = [int(s) for s in str(message["msg"]).split() if s.isdigit()] #separa quem jogou e o que jogou
                        if jogador != machine_number:
                            print(str(jogador) + " jogou " + str(jogada)) #imprime a jogada

                    case 6: #anuncio de aposta
                        (apostador, aposta) = [int(s) for s in str(message["msg"]).split() if s.isdigit()] #separa quem apostou e quanto apostou
                        if apostador != machine_number:
                            print(str(apostador) + " apostou " + str(aposta)) #imprime a aposta
                        
                    case 7: # Anuncio de Campeão
                        print("O campeao da rodada é: " + str(message["msg"]))
                    
                    case 8: #Anuncio de perda de vida.
                        
                        (perdedor, vidasPerdidas) = [int(s) for s in str(message["msg"]).split() if s.isdigit()] #separa quem perdeu e quantas vidas
                        vidas[perdedor - 1] -= vidasPerdidas #reduz as vida do perdedor
                        print(str(perdedor) + " perdeu " + str(vidasPerdidas) + " vidas")

                        if vidas[perdedor - 1] <= 0: #se o perdedor ficou sem vidas, ele morre
                            print(str(perdedor) + " morreu")      
                    
                    case 9: #Fim de rodada
                        print("Fim de rodada")
                        
                        vivos = 0
                        for i in vidas:
                            if i > 0:
                                vivos += 1
                        if vivos <= 1:
                            for j in range(4):
                                if vidas[j] > 0:
                                    print("O jogador " + str(j+1) + " ganhou")
                            Jogando = False
                        
                        rodando = False
                
                net.messageTo(message, UDP_IP, SND_PORT)
            
            elif message["type"] == 4 and vidas[machine_number - 1] > 0: #novo carteador
                souCarteador = True
                message = Message(9, machine_number, 5, 0, 0)#novo carteador avisa o vim de rodada
                net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                rodando = False
                print("Fim de rodada")
            
            else:
                net.messageTo(message, UDP_IP, SND_PORT)
