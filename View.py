from pydoc import Helper
from tkinter import CENTER
import pygame as pyg

import Movement as mv

pyg.init() #Pygame inicializa

#Crear pantalla
display_size = 1280, 720
display = pyg.display.set_mode(display_size)

pyg.display.set_caption("Tester View") #Titulo de ventana

width = 1280
height = 720

#Some stuffs

player_points = 1000
points_losted = 0.017

FPS = 60
angle = 0
rotation = 1
speed = 3
car_coor = [1100,267]

def setImage(coord,path):
    imgA = pyg.image.load(path).convert_alpha()
    imgB = imgA.get_rect()
    imgB.move_ip(coord[0],coord[1])
    return imgA,imgB

#IDK----------------------------------------------------------------------------------------------
class Top_Sprait(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pyg.image.load( 'Resources/Top.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (640,270))
        self.mask = pyg.mask.from_surface(self.image)

class Bot_Sprait(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pyg.image.load( 'Resources/Bot.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (640,420))
        self.mask = pyg.mask.from_surface(self.image)

class Goal_Sprait(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pyg.image.load( 'Resources/Goal.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (72,360))
        self.mask = pyg.mask.from_surface(self.image)


class Car_Sprait(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pyg.image.load( 'Resources/Car.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (1100,267)) #(1134,267)
        self.mask = pyg.mask.from_surface(self.image)
    
    def update(self, axis_x, axis_y, angle, center):
        self.image = pyg.image.load( 'Resources/Car.png' ).convert_alpha()

        self.rect.x += axis_x
        self.rect.y += axis_y

        self.image = pyg.transform.rotate( self.image, angle )

        self.rect = self.image.get_rect( center = (center[0],center[1]) )

#imagenes-------------------------------------------------------------------------------------
root_path = 'Resources/'

#Background------------------------------------------------
Background_path = root_path + 'Track.png'

Background_coor = [0,0]

Background_setter = setImage(Background_coor,Background_path)

#Bordes-----------------------------------------------------
Car_spr = pyg.sprite.GroupSingle( )

Top_spr = pyg.sprite.GroupSingle( )
Bot_spr = pyg.sprite.GroupSingle( )
Goal_spr = pyg.sprite.GroupSingle( )

Car_spr.add( Car_Sprait() )

Top_spr.add( Top_Sprait() )
Bot_spr.add( Bot_Sprait() )
Goal_spr.add( Goal_Sprait() )

#Empezar too----------------------------------------------------------------------------------
run = True
clock = pyg.time.Clock()

while run:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False

    key = pyg.key.get_pressed() #Aqui van los valores del giroscopio

    #Movimiento
    movement = mv.spriteMovement(Car_spr,speed, angle, rotation, car_coor, key)
    movement[0]
    angle = movement[2]
    car_coor = movement[3]
    print( movement[1] )
    print( car_coor )

    #Colisiones
    if pyg.sprite.spritecollide( Car_spr.sprite,Top_spr,False,pyg.sprite.collide_mask):
        player_points -= points_losted
        print('Chocaste con la pared TOP')

    if pyg.sprite.spritecollide( Car_spr.sprite,Bot_spr,False,pyg.sprite.collide_mask):
        player_points -= points_losted
        print('Chocaste con la pared BOT')

    if pyg.sprite.spritecollide( Car_spr.sprite,Goal_spr,False,pyg.sprite.collide_mask):
        print('Victoria') 
    
    print( f'Points: {player_points}' )

    #Agregar imagenes
    display.blit( Background_setter[0], Background_setter[1] )

    Car_spr.draw( display )

    pyg.display.flip()
    clock.tick(60)

pyg.quit