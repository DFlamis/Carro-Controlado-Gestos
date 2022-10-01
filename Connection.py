from serial import*


def pasame_los_datos( ):
    data = 'S'
    cleaner = ['S','F','B','L','R']
    atmega = Serial('COM16',9600)
    mens = atmega.readline().strip()
    str_mens = str(mens.decode())
    if str_mens in cleaner:
        data = str_mens 
    
    return data

def pasame_los_datos( data ):
    # data = 'S'
    cleaner = ['S','F','B','L','R']
    atmega = Serial('COM16',9600)
    mens = atmega.readline().strip()
    str_mens = str(mens.decode())
    if str_mens in cleaner:
        data.appends( str_mens )
    
    return data