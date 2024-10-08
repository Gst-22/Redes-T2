import random

def sorteia (tam):
    sorteio = random.sample(range(40), tam)
    return sorteio

def sorteiaMaos(tam_mao, vivos):
    todas_cartas = sorteia(tam_mao * vivos + 1)
    carteado = []
    for i in range(vivos):
        mao = []
        for j in range(tam_mao):
            mao.append(todas_cartas[i * tam_mao + j])
        carteado.append(mao)
    vira = todas_cartas[-1]
    return (carteado, vira)

def traduzCarta (carta):
    n = int(carta / 10)
    if n == 0:
        naipe = "♦"
    elif n == 1:
        naipe = "♠"
    elif n == 2:
        naipe = "♥"
    elif n == 3:
        naipe = "♣"
    
    num = carta % 10
    if num == 0:
        numero = '4'
    elif num == 1:
        numero = '5'
    elif num == 2:
        numero = '6'
    elif num == 3:
        numero = '7'
    elif num == 4:
        numero = 'Q'
    elif num == 5:
        numero = 'J'
    elif num == 6:
        numero = 'K'
    elif num == 7:
        numero = 'A'
    elif num == 8:
        numero = '2'
    elif num == 9:
        numero = '3'
    carta_traduzida = naipe + numero
    return carta_traduzida

def imprimeMao (mao):
    if len(mao) == 0:
        print("Mao Vazia")
        return 1
    
    if len(mao) == 1:
        print(traduzCarta(mao[0]))
        return 1

    impressao = traduzCarta(mao[0])
    for carta in range(1, len(mao)):
        impressao += ', ' + traduzCarta(mao[carta])
    print(impressao)

    return 1


def compararCartas (cartaA, cartaB, vira):
    
    #Se cartaB  for -1, cartaA é a unica valendo.
    if cartaB == -1:
        return 1
    
    naipeA = int(cartaA / 10)
    naipeB = int(cartaB / 10)
    numA = cartaA % 10
    numB = cartaB % 10
    manilha = (vira + 1) % 10

    if numA == manilha:
        numA = 10
    if numB == manilha:
        numB = 10
    
    if numA > numB:
        return 1
    elif numA < numB:
        return 0
    else:
        if naipeA > naipeB:
            return 1
        else:
            return 0
        
def jogaresVivos (vidas):
    jogadores_vivos = []
    for i in range(len(vidas)):
        if vidas[i] > 0:
            jogadores_vivos.append(i)
    
    if len(jogadores_vivos) > 0:
        return (len(jogadores_vivos), jogadores_vivos[0]+1)
    else:
        return (len(jogadores_vivos), -1)
    
def escolhaCarta(mao):
    
    if len(mao) == 1:
        input("Pressione Enter para Jogar")
        return mao[0]

    selecao = input("Escolha uma carta (de 0 a {}):\n".format(len(mao)-1))
    while not selecao.isdigit() or int(selecao) < 0 or int(selecao) >= len(mao):
        selecao = input("Escolha uma carta (de 0 a {}):\n".format(len(mao)-1))
    
    return mao[int(selecao)]

def escolhaAposta(sou_carteador, apostasTotais, tamMaoAtual):
    if sou_carteador:
        select = input("Faz quantos?\n")
        while not select.isnumeric() or apostasTotais +  int(select) == tamMaoAtual or int(select) < 0 or int(select) > tamMaoAtual:
            select = input("Faz quantos?\n")
        
        return int(select)
    else:
        select = input("Faz quantos?\n")
        while not select.isnumeric() or int(select) < 0 or int(select) > tamMaoAtual:
            select = input("Faz quantos?\n")
        
        return int(select)