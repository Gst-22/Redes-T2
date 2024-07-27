import socket
import config as config
import ast
import gameplay as game
import network as net
from network import Message

machine_number = int(input("Numero da Maquina: "))
UDP_IP = "localhost"

RCV_PORT, SND_PORT = config.config_machine(machine_number)

print ("SEND", SND_PORT, "RECEIVE", RCV_PORT)

rcv_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcv_skt.bind((UDP_IP, RCV_PORT))

maoNumerica = []
apostasTotais = 0
tamMaoAtual = 4
(maiorCarta, lider) = (0, 0)
pontuacaoRodada = [0, 0, 0, 0]
apostasDaRodada = [0, 0, 0, 0]

if machine_number == 1: #Maquina 1 começa como carteado
    souCarteador = True
else:
    souCarteador = False

if souCarteador: #Carteador inicia o jogo
    
    carteado = game.sorteiaMaos(tamMaoAtual)#Cria carteado.
    maoNumerica = carteado[0]#Minha mão
    print(maoNumerica)

    for i in range(3):#Distribui Cartas
        message = Message(3, machine_number, i+2, ' '.join(map(str, carteado[i+1])), 0)
        enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)
        if enviado:
            print("Enviado para " + str(i+2))
        else:
            print("Falha ao enviar.")
            exit
    
    message = Message(2, machine_number, (machine_number % 4) +1, 0, 0)
    enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)#começam apostas


while True: #espero mensagem, envio confirmação.
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
                        enviado = net.ringMessage(message, machine_number, UDP_IP, SND_PORT, rcv_skt)#o guina é um viado
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
                            my_message = Message(1, machine_number, (machine_number % 4) + 1, 0, 0)#começa apostas
                            enviado = net.ringMessage(my_message, machine_number, UDP_IP, SND_PORT, rcv_skt)
                        else: #se acabaram as cartas, acabou a rodada
                            for i in range(4): #para cada jogador, verifica se a aposta foi correta, se não, perdeu
                                if apostasDaRodada[i] != pontuacaoRodada[i]:
                                    print(str(i+1) + " perdeu")
                                else:
                                    print(str(i+1) + " ganhou")
                
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
                
                case 6:
                    print("O campeao da rodada é: " + str(message["msg"]))
        
        else: #Mensagem para outra pessoa, passa adiante.
            net.messageTo(message, UDP_IP, SND_PORT)#obrigado copilot --> o guina é um viado
