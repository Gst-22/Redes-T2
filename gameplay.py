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
    match n:
        case 0:
            naipe = "♦"
        case 1:
            naipe = "♠"
        case 2:
            naipe = "♥"
        case 3:
            naipe = "♣"
        
    num = carta % 10
    match num:
        case 0:
            numero = '4'
        case 1:
            numero = '5'
        case 2:
            numero = '6'
        case 3:
            numero = '7'
        case 4:
            numero = 'Q'
        case 5:
            numero = 'J'
        case 6:
            numero = 'K'
        case 7:
            numero = 'A'
        case 8:
            numero = '2'
        case 9:
            numero = '3'
    carta_traduzida = naipe + numero
    return carta_traduzida

def compararCartas (cartaA, cartaB, vira):
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
        