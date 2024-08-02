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
tamMaoAtual = 1
vidas = [4  , 4  , 4  , 4]

if machine_number == 1: #Maquina 1 começa como carteado
    souCarteador = True
else:
    souCarteador = False

while True:
    print("Iniciando jogo")
    rodando = True

    (maiorCarta, lider) = (0, 0)
    pontuacaoRodada = [0, 0, 0, 0]
    apostasDaRodada = [0, 0, 0, 0]

    if souCarteador: #Carteador inicia o jogo
        
        carteado = game.sorteiaMaos(tamMaoAtual)#Cria carteado.
        maoNumerica = carteado[machine_number - 1]#Minha mão
        print(maoNumerica)

        for i in range(4):#Distribui Cartas
            if i != machine_number - 1: #garante que eu não receba minhas próprias cartas
                message = Message(3, machine_number, i+1, ' '.join(map(str, carteado[i])), 0) #mensagem com cartas para cada jogador
                enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                if enviado:
                    print("Enviado para " + str(i+1))
                else:
                    print("Falha ao enviar.")
                    exit
        
        message = Message(2, machine_number, (machine_number % 4) +1, 0, 0)
        enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)#começam apostas

    while rodando: #espero mensagem, envio confirmação.
        data, addr = rcv_skt.recvfrom(1024)
        if data:
            message = ast.literal_eval(data.decode()) #recebi dados
            
            if message["destino"] == machine_number: #mensagem pra mim
                
                message["recebido"] = 1 #confirmo recebimento
                net.messageTo(message, UDP_IP, SND_PORT)

                match message["type"]: #que tipo de mensagem?
                    case 1: #Minha vez de jogar
                        
                        print(maoNumerica)
                        select = int(input("Escolha uma carta:\n")) #loop até escolher uma carta válida
                        while select not in maoNumerica:
                            select = int(input("Escolha uma carta:\n"))

                        maoNumerica.remove(select) #removo carta da mão
                        print(maoNumerica)#printo mão atualizada
                        
                        my_message = Message(4, machine_number, 5, select, 0) #mensagem com minha jogada para todos
                        enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt) #envio mensagem
                        
                        if not souCarteador:
                            message = Message(1, machine_number, (machine_number % 4) + 1, 0, 0)#passo a vez pro proximo
                            enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                        else:
                            if select % 10 > maiorCarta % 10: #se a carta que eu joguei é a maior, eu sou o lider
                                lider = machine_number
                                pontuacaoRodada[machine_number - 1] += 1
                            else: #se não, o lider continua o mesmo
                                pontuacaoRodada[lider - 1] += 1
                        
                            print("Campeão: " + str(lider))
                            my_message = Message(6, machine_number, 5, lider, 0)#anuncia o lider da rodadada
                            enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)

                            if len(maoNumerica) > 0:
                                (maiorCarta, lider) = (0, 0)
                                my_message = Message(1, machine_number, (machine_number % 4) + 1, 0, 0)#começa proxima rodada
                                enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                            else: #se acabaram as cartas, acabou a rodada
                                for i in range(4): #para cada jogador, verifica se a aposta foi correta, se não, perde uma vida
                                    if apostasDaRodada[i] != pontuacaoRodada[i] and i != machine_number - 1:
                                            vidasPerdidas = abs(apostasDaRodada[i] - pontuacaoRodada[i]) #calcula quantas vidas foram perdidas
                                            aviso = str(i+1) + " " + str(vidasPerdidas) #a mensagem deve indicar quantas vidas foram perdidas e quem perdeu
                                            my_message = Message(7, machine_number, 5, aviso, 0)#mensagem de perda de vida
                                            enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                                        
                                souCarteador = False
                                my_message = Message(8, machine_number, (machine_number % 4) + 1, 0, 0)#novo carteador
                                enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)

                                rodando = False
                                my_message = Message(9, machine_number, 5, 0, 0)#fim de rodada
                                enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                    
                    case 2: #Minha vez de apostar
                        
                        select = int(input("Faz quantos?\n"))#loop até escolher uma aposta válida
                        if souCarteador:
                            while apostasTotais +  select == tamMaoAtual or select < 0 or select > tamMaoAtual: #cartador deve fazer uma aposta válida e que torne impossivel empate
                                select = int(input("Faz quantos?\n"))
                        else:
                            while select > tamMaoAtual or select < 0: #jogadores devem fazer apostas válidas
                                select = int(input("Faz quantos?\n"))

                        my_message = Message(5, machine_number, 5, select, 0)#mensagem com minha aposta para todos
                        enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)#envio mensagem
                        if not souCarteador:
                            message = Message(2, machine_number, (machine_number % 4)+1, 0, 0)#se não sou carteador, passo a vez pro proximo
                            enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                        else:
                            apostasDaRodada[machine_number - 1] = select
                            message = Message(1, machine_number, (machine_number % 4) + 1, 0, 0)
                            enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)#se sou carteador, começo as jogadas

                    case 3: # Minhas cartas recebidas
                        maoNumerica = [int(s) for s in str(message["msg"]).split() if s.isdigit()]
                        print(maoNumerica)

                    case 8: #recebi o bastão
                        print("Sou o novo carteador")
                        souCarteador = True

                    case _:
                        print("Poop")
            
            elif message["destino"] == 5: #mensagem para todos.
                
                message["recebido"] += 1 #confirmo recebimento
                net.messageTo(message, UDP_IP, SND_PORT)
                
                match message["type"]: #que tipo de mensagem?
                    case 4: #anuncio de jogada
                        print(str(message["origem"]) + " jogou um " + str(message["msg"]))
                        if souCarteador: #se eu sou o carteador, armazeno quem esta vencendo a rodada
                            cartaAtual = int(message["msg"])
                            jogadorAtual = int(message["origem"])
                            if cartaAtual % 10 > maiorCarta % 10:
                                (maiorCarta, lider) = (cartaAtual, jogadorAtual)

                    case 5: #anuncio de aposta
                        print(str(message["origem"]) + " faz " + str(message["msg"]))
                        if souCarteador:
                            apostasTotais += int(message["msg"])
                            apostasDaRodada[int(message["origem"]) - 1] = int(message["msg"])
                            print("Apostas totais: " + str(apostasTotais))
                    
                    case 6: # Anuncio de Campeão
                        print("O campeao da rodada é: " + str(message["msg"]))
                    
                    case 7: #Anuncio de perda de vida.
                        
                        (perdedor, vidasPerdidas) = [int(s) for s in str(message["msg"]).split() if s.isdigit()] #separa quem perdeu e quantas vidas
                        vidas[perdedor - 1] -= vidasPerdidas #reduz as vida do perdedor
                        print(str(perdedor) + " perdeu " + str(vidasPerdidas) + " vidas")

                        if vidas[perdedor - 1] == 0: #se o perdedor ficou sem vidas, ele morre
                            print(str(perdedor) + " morreu")      
                    
                    case 9: #Fim de rodada
                        print("Fim de rodada")
                        rodando = False              
            
            else: #Mensagem para outra pessoa, passa adiante.
                net.messageTo(message, UDP_IP, SND_PORT)
