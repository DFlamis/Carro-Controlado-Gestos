import serial

try:
    alv = serial.Serial('com3',9600)
    data = alv.readline()

except TimeoutError:
    print('No pues valio queso xd')

finally:
    print('Listoh')
