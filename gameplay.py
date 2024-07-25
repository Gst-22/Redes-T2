import random

def sorteia (tam):
    sorteio = random.sample(range(40), tam)
    return sorteio

def sorteiaMaos(tam_mao):
    cartado = []
    for i in range(4):
        mao = sorteia(tam_mao)
        cartado.append(mao)
    return cartado

def traduzCartas (sorteio):
    cartas = []
    for carta in sorteio:
        n = int(carta / 10)
        match n:
            case 0:
                naipe = "Ouro"
            case 1:
                naipe = "Espada"
            case 2:
                naipe = "Copa"
            case 3:
                naipe = "Paus"
        
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
        cartas.append(numero + " de " + naipe)

    return cartas