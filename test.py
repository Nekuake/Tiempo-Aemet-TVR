medionuboso = [12, 13, 14, 15, 17]
mediolluvia = [23, 24, 25]
lluvia = [26, 27]
nieve = [33, 34, 35, 36]
while 1 == 1:
    codigo = int(input('>'))
    if codigo == 11:
        print('Despejado')
    elif codigo in medionuboso:
        print('Medio nuboso')
    elif codigo == 16:
        print('Cubierto')
    elif codigo in mediolluvia:
        print('Medio lluvia')
    elif codigo in lluvia:
        print('Lluvia')
    elif codigo in nieve:
        print('Nieve')
    elif codigo == 53:
        print('Tormenta')
    else:
        print(
        'NO SE RECONOCE EL CÓDIGO. SE VA A PONER EL CÓDIGO DE NUBLADO COMO PLACEHOLDER PERO HAY QUE REVISAR EL CODIGO RECIBIDO.')
