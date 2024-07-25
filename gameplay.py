import random

def sorteia (tam):
    sorteio = random.sample(range(40), tam)
    return sorteio

def sorteiaMaos(tam_mao):
    todas_cartas = sorteia(tam_mao * 4)
    carteado = []
    for i in range(4):
        mao = []
        for j in range(tam_mao):
            mao.append(todas_cartas[i * tam_mao + j])
        carteado.append(mao)
    return carteado

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
