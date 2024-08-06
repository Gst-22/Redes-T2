import socket
import ast
import gameplay as game
import network as net
from network import Message
import time

machine_number = int(input("Numero da Maquina: "))
RCV_PORT, SND_PORT, SND_IP, RCV_IP = net.set_configs(machine_number)

print ("SEND", SND_PORT, "RECEIVE", RCV_PORT, "SEND_IP", SND_IP, "MY_IP", RCV_IP)

rcv_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcv_skt.bind((RCV_IP, RCV_PORT))

maoNumerica = []
tamMaoAtual = 0
vidas = [4 , 4, 4, 4]

souCarteador = False

#Maquina 1 começa como carteador
if machine_number == 1:
    souCarteador = True

Jogando = True
while Jogando: #loop principal do jogo
    
    tamMaoAtual += 1

    rodando = True

    pontuacaoRodada = [0, 0, 0, 0]
    apostasDaRodada = [0, 0, 0, 0]
    apostasTotais = 0

    if souCarteador: #Carteador inicia o jogo        
        print("Sou o Carteador")

        (vivos, x) = game.jogaresVivos(vidas)

        #Gera o carteado e o vira.
        (carteado, vira) = game.sorteiaMaos(tamMaoAtual, vivos)
        maoNumerica = carteado.pop()
        
        #Imprime a mão do carteador e o vira.
        game.imprimeMao(maoNumerica)
        print("Vira: " + game.traduzCarta(vira))

        #Distribui as mãos de cada jogadors
        for aux in range(3):
            #Não envio para mim mesmo nem para jogadores mortos
            i = (machine_number + aux) % 4
            if vidas[i] > 0:
                message = Message(3, machine_number, i+1, ' '.join(map(str, carteado.pop())), 0)
                enviado = net.ringMessage(message, machine_number, SND_IP, SND_PORT, rcv_skt)
        
        #Anuncia o vira
        message = Message(10, machine_number, 5, vira, 0)
        net.ringMessage(message, machine_number, SND_IP, SND_PORT, rcv_skt)

        #Coleta as apostas de todos os jogadores
        for aux in range(3):
            i = (machine_number + aux) % 4
            if vidas[i] > 0:    
                message = Message(2, machine_number, i+1, 0, 0)
                enviado = net.ringMessage(message, machine_number, SND_IP, SND_PORT, rcv_skt)
                print(str(i+1) + " apostou " + str(enviado))

                apostasDaRodada[i] = int(enviado)
                apostasTotais += int(enviado)

                anuncio = str(i+1) + ' ' + str(apostasDaRodada[i])
                msg_anuncio = Message(6, machine_number, 5, anuncio, 0)
                net.ringMessage(msg_anuncio, machine_number, SND_IP, SND_PORT, rcv_skt)
        
        #Carteador faz sua aposta
        select = int(input("Faz quantos?\n"))
        while apostasTotais +  select == tamMaoAtual or select < 0 or select > tamMaoAtual:
            select = int(input("Faz quantos?\n"))

        apostasDaRodada[machine_number - 1] = select #armazena a aposta do carteador

        #Anuncia aposta do carteador
        anuncio = str(machine_number) + ' ' + str(select)
        message = Message(6, machine_number, 5, anuncio, 0)
        net.ringMessage(message, machine_number, SND_IP, SND_PORT, rcv_skt)
        
        #loop de rodada
        while len(maoNumerica) > 0:
            (maiorCarta, lider) = (-1, 0)
            
            #Coleta as jogadas de todos os jogadores
            for aux in range(3):
                i = (machine_number + aux) % 4
                
                if vidas[i] > 0:
                    message = Message(1, machine_number, i+1, 0, 0)
                    enviado = net.ringMessage(message, machine_number, SND_IP, SND_PORT, rcv_skt)
                    jogada = int(enviado)

                    if game.compararCartas(jogada, maiorCarta, vira):
                        "Lider: " + str(i+1)
                        maiorCarta = jogada
                        lider = i + 1
                        
                    print(str(i+1) + " jogou " + game.traduzCarta(jogada))
                    
                    anuncio = str(i+1) + ' ' + str(jogada)
                    msg_anuncio = Message(5, machine_number, 5, anuncio, 0)
                    net.ringMessage(msg_anuncio, machine_number, SND_IP, SND_PORT, rcv_skt)

            #vez do carteador
            game.imprimeMao(maoNumerica)
            select = int(input("Escolha uma carta:\n")) 
            while select < 0 or select >= len(maoNumerica):
                select = int(input("Escolha uma carta:\n"))

            select = maoNumerica[select]
            maoNumerica.remove(select)
            
            #se o carteador jogou a maior carta, ele vira o lider
            if game.compararCartas(select, maiorCarta, vira): 
                maiorCarta = select
                lider = machine_number
            
            anuncio = str(machine_number) + ' ' + str(select)
            msg_anuncio = Message(5, machine_number, 5, anuncio, 0)
            net.ringMessage(msg_anuncio, machine_number, SND_IP, SND_PORT, rcv_skt)

            pontuacaoRodada[lider - 1] += 1 #pontua o lider

            #anuncia o campeão da rodada
            my_anuncio = Message(7, machine_number, 5, lider, 0)
            net.ringMessage(my_anuncio, machine_number, SND_IP, SND_PORT, rcv_skt)
            print("O jogador " + str(lider) + " pontuou")

        for i in range(4): #para cada jogador, verifica se a aposta foi correta, se não, perde vida
            if apostasDaRodada[i] != pontuacaoRodada[i]:
                vidasPerdidas = abs(apostasDaRodada[i] - pontuacaoRodada[i]) #calcula quantas vidas foram perdidas
                aviso = str(i+1) + " " + str(vidasPerdidas) #a mensagem deve indicar quantas vidas foram perdidas e quem perdeu
                my_message = Message(8, machine_number, 5, aviso, 0)#mensagem de perda de vida
                enviado = net.ringMessage(my_message, machine_number, SND_IP, SND_PORT, rcv_skt)
                vidas[i] -= vidasPerdidas #reduz as vidas do jogador i
                print(str(i+1) + " perdeu " + str(vidasPerdidas) + " vidas")
                if vidas[i] <= 0: #se o jogador i ficou sem vidas, ele morre
                    print(str(i+1) + " morreu")

        (num_jogadores_vivos, vencedor) = game.jogaresVivos(vidas)

        if num_jogadores_vivos <= 1:
            
            for aux in range(4):
                i = (machine_number + aux) % 4
                message = Message(9, machine_number, 5, 0, 0)
                enviado = net.messageTo(message, SND_IP, SND_PORT)
            print("Fim de rodada")
            
            if vencedor != -1:
                print("O jogador " + str(vencedor) + " ganhou")
            else:
                print("Empate")

            Jogando = False
            rodando = False
        
        else:
            #carteador passa a vez
            souCarteador = False 
            token = Message(4, machine_number, 0, 0, 0)
            net.messageTo(token, SND_IP, SND_PORT)

    while rodando: #espero mensagem, envio confirmação.
        data, addr = rcv_skt.recvfrom(1024)
        if data:
            message = ast.literal_eval(data.decode()) #recebi dados
            
            if message["destino"] == machine_number: #mensagem pra mim
                
                    message["recebido"] = 1 #confirmo recebimento
                    #Passo a mensagem adiante

                    #que tipo de mensagem?
                    if message["type"] == 1: #Minha vez de jogar
                        
                        game.imprimeMao(maoNumerica)
                        select = int(input("Escolha uma carta (de 0 a {}):\n".format(len(maoNumerica)))) #loop até escolher uma carta válida
                        while select < 0 or select >= len(maoNumerica):
                            select = int(input("Escolha uma carta (de 0 a {}):\n".format(len(maoNumerica))))

                        select = maoNumerica[select]
                        maoNumerica.remove(select) #removo carta da mão

                        message["msg"] = str(select)#adiciono minha jogada na mensagem

                    elif message["type"] == 2: #Minha vez de apostar
                        select = int(input("Faz quantos?\n"))#loop até escolher uma aposta válida
                        while select > tamMaoAtual or select < 0: #jogadores devem fazer apostas válidas
                            select = int(input("Faz quantos?\n"))
                    
                        message["msg"] = str(select)#adiciono minha aposta na mensagem

                    elif message["type"] == 3: # Minhas cartas recebidas
                        maoNumerica = [int(s) for s in str(message["msg"]).split() if s.isdigit()]
                        game.imprimeMao(maoNumerica)

                    else:
                        print("ERRO: Tipo de mensagem desconhecido\n")
                        exit(1)
            
                    net.messageTo(message, SND_IP, SND_PORT)
            
            elif message["destino"] == 5: #mensagem é para todos
                
                message["recebido"] += 1 #aumento o recebimento e passo adiante

                #que tipo de mensagem?
                if message["type"] == 5: #Anuncio de jogada
                    (jogador, jogada) = [int(s) for s in str(message["msg"]).split() if s.isdigit()]
                    
                    if jogador != machine_number:
                        print(str(jogador) + " jogou " + game.traduzCarta(jogada))
                
                elif message["type"] == 6: #Anuncio de aposta
                    (apostador, aposta) = [int(s) for s in str(message["msg"]).split() if s.isdigit()]
                    
                    if apostador != machine_number:
                        print(str(apostador) + " apostou " + str(aposta))
                    
                elif message["type"] == 7: #Alguem pontuou
                    print("O jogador " + str(message["msg"]) + " pontuou")
                
                elif message["type"] == 8: #Jogador perdeu vida
                    (perdedor, vidasPerdidas) = [int(s) for s in str(message["msg"]).split() if s.isdigit()] 
                    
                    vidas[perdedor - 1] -= vidasPerdidas 
                    print(str(perdedor) + " perdeu " + str(vidasPerdidas) + " vidas")
        
                    if vidas[perdedor - 1] <= 0: 
                        print(str(perdedor) + " morreu")      
                
                elif message["type"] == 9: # Fim de rodada
                    print("Fim de rodada")
                    
                    (num_jogadores_vivos, vencedor) = game.jogaresVivos(vidas)
                    if num_jogadores_vivos <= 1:
                        if vencedor != -1:
                            print("O jogador " + str(vencedor) + " ganhou")
                        else:
                            print("Empate")
                        Jogando = False
                    
                    rodando = False
                
                elif message["type"] == 10: #Revela o vira
                    print("Vira: " + game.traduzCarta(message["msg"]))
            
                net.messageTo(message, SND_IP, SND_PORT)
            
            elif message["type"] == 4 and vidas[machine_number - 1] > 0: #Eu sou o novo carteador
                souCarteador = True
                message = Message(9, machine_number, 5, 0, 0)#novo carteador avisa o vim de rodada
                net.ringMessage(message, machine_number, SND_IP, SND_PORT, rcv_skt)
                rodando = False
                print("Fim de rodada")
            
            else:
                net.messageTo(message, SND_IP, SND_PORT)
