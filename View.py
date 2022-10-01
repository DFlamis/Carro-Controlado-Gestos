import math
import threading
import pygame as pyg
import random as rn
import numpy as np


import Movement as mv
import Connection as cn
import Sensors as sn
import Stages as stg
import Walls

import NeuronalNetwork.Draw as dw
from NeuronalNetwork.Saki import QLAgent

from serial import*
from keras.utils import to_categorical
import sys

pyg.init() #Pygame inicializa

#Crear pantalla-----------------------------------------------------------
is_training = False
display_size = 1920,720
display = pyg.display.set_mode(display_size)

pyg.display.set_caption("Map View - Celula/Mecatronica") #Titulo de ventana

#Some stuffs--------------------------------------------------------------
color_text = (0,0,0)
color_text_2 = (255,255,255)      

font = pyg.font.SysFont('Consolas',20)
winner_font = pyg.font.SysFont('Berlin Sans FB Demi Bold',130)
winner_font_points = pyg.font.SysFont('Berlin Sans FB Demi Bold',80)

root_Player_path = 'Player_Resources/'
root_AI_path = 'AI_Resources/'
root_Game_path = 'Game_Resources/'

fps = 60
rotation = 3.6 #1.7s 360g
speed = 6 #4sg 121c

default_coor = [1100,267]

car_coor = [1100,267]
car_AI_coor = [1100,267]

player_points = 1000
timer = 0

points_losted_per_second = 7
points_losted_per_tick = points_losted_per_second / fps

angle = 0
angle_AI = 0

is_crashed = 0 # 0 -> intacto // 1 -> choco

incentivarions = 0
distance = 0


trash = (1200,700)

def pasame_los_datos():
    # pointer = 0
    # while pointer < 1000:
    cleaner = ['S','F','B','L','R']
    atmega = Serial('COM16',9600)
    try:
        atmega.flushInput()
        mens = atmega.readline().strip()
        str_mens = str(mens.decode())
        if str_mens in cleaner:
            data.append( str_mens )
    except (KeyboardInterrupt,SystemExit):
        data.append('S')
    # pointer += 1

def setImage(coord,path):
    imgA = pyg.image.load(path).convert_alpha()
    imgB = imgA.get_rect()
    imgB.move_ip(coord[0],coord[1])
    return imgA,imgB

def reset( all_incentivations ):
    for incentivation in all_incentivations:
        incentivation.sprites()[0].reset()

#Neuronal Network------------------------------------------------------------------------------------------------------------------------------------
def define_parameters():
	params = dict()
	params['epsilon_decay_linear'] = 1 / 100
	params['learning_rate'] = 0.001
	params['first_layer_size'] = 24  # neurons in the first layer
	params['second_layer_size'] = 24  # neurons in the second layer
	params['episodes'] = 50
	params['memory_size'] = 400000
	params['batch_size'] = 1000
	params['weights_path'] = 'AI_memory-24-24-c400.hdf5'
	params['train'] = False #True -> para entrenar -- False -> recordar
	if params['train']:
		params['load_weights'] = False
	else:
		params['load_weights'] = True
	return params

params = define_parameters()
thinker = QLAgent( params )

episodes = 0

#Se inicializa para que su primera accion sea moverse hacia delante
arg_max = 2
key_AI = 'UP'

#Sprites---------------------------------------------------------------------------------------------------------------------------------------------

#Car----------------------------------------------------------------------

class Car_Sprait(pyg.sprite.Sprite):
    def __init__(self, root_path):
        super().__init__()
        self.path = root_path
        self.image = pyg.image.load( root_path + 'Car.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (1100,267))
        self.rect.center = (1100,267)
        self.mask = pyg.mask.from_surface(self.image)
    
    def update(self, axis_x, axis_y, angle, center):
        self.image = pyg.image.load( self.path + 'Car.png' ).convert_alpha()

        self.rect.x += axis_x
        self.rect.y += axis_y

        self.image = pyg.transform.rotate( self.image, angle )

        self.rect = self.image.get_rect( center = (center[0],center[1]) )
        
        self.rect.center = (center[0],center[1])
        self.mask = pyg.mask.from_surface(self.image)

#sensor-------------------------------------------------------------------
class Sensor_Sprait(pyg.sprite.Sprite):
    def __init__(self, x, y, variation, angle):
        super().__init__()

        self.image = pyg.image.load( root_AI_path + 'Sensor'+variation+'.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (x,y)) #1100,267
        self.mask = pyg.mask.from_surface(self.image)
        self.idk = variation

        self.this_x = x
        self.this_y = y

        self.angle = angle
        self.separation_x = 1100 - x
        self.separation_y = 267 - y

    def update(self, axis_x, axis_y, angle):
        self.image = pyg.image.load( root_AI_path + 'Sensor'+ self.idk +'.png' ).convert_alpha()

        self.image = pyg.transform.rotate( self.image, angle )

        self.rect = self.image.get_rect( center = (axis_x, axis_y) )

        self.mask = pyg.mask.from_surface(self.image)

#Incentivation------------------------------------------------------------
class Incentivation_Sprait(pyg.sprite.Sprite):
    def __init__(self, position, trash, angle):
        super().__init__()

        self.trash = trash
        self.start = position
        self.angle = angle

        self.image = pyg.image.load( root_AI_path + 'Incentivation.png' ).convert_alpha()
        self.rect = self.image.get_rect( center = (self.start) )
        self.image = pyg.transform.rotate( self.image, angle )
        self.mask = pyg.mask.from_surface(self.image)

    def to_trash(self):
        self.rect = self.image.get_rect( center = ( self.trash ) )
        self.mask = pyg.mask.from_surface(self.image)

    def reset(self):
        self.image = pyg.image.load( root_AI_path + 'Incentivation.png' ).convert_alpha()

        self.rect = self.image.get_rect( center = ( self.start ) )

        self.image = pyg.transform.rotate( self.image, self.angle )
        self.mask = pyg.mask.from_surface(self.image)
#Others-------------------------------------------------------------------

class Goal_Sprait(pyg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pyg.image.load( root_Game_path + 'Goal.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (72,360))
        self.mask = pyg.mask.from_surface(self.image)
    
#Background---------------------------------------------------------------
Background_path = root_Game_path + 'Track.png'

Background_coor = [0,0]

Background_setter = setImage(Background_coor,Background_path)

Decorations_path = root_Game_path + 'Decotarions.png'

Decorations_coor = [0,0]

Decorations_setter = setImage(Decorations_coor,Decorations_path)

#Srptes loaders--------------------------------------------------------------------------------------------------------------------------------------

#Car Sprites--------------------------------------------------------------
Car_Player_spr = pyg.sprite.GroupSingle( )
Car_AI_spr = pyg.sprite.GroupSingle( )

car_player_sprite = Car_Sprait( root_Player_path )
car_AI_sprite = Car_Sprait( root_AI_path )

Car_Player_spr.add( car_player_sprite )
Car_AI_spr.add( car_AI_sprite )

#Goal Sprites-------------------------------------------------------------
Goal_spr = pyg.sprite.GroupSingle( )
Goal_spr.add( Goal_Sprait() )

#Walls Sprites------------------------------------------------------------
walls = Walls.walls_generator(root_Player_path, root_AI_path)

Top_Player_spr = walls[0]
Bot_Player_spr = walls[1]
Obstacles_Player_spr = walls[2]

Top_AI_spr = walls[3]
Bot_AI_spr = walls[4]
Edge_AI_spr = walls[5]

#Sensor Sprites (1100,267) -----------------------------------------------
sensors = sn.generate_sensors( root_AI_path )

Sensor_Left_A = sensors[0]
Sensor_Left_B = sensors[1]
Sensor_Left_C = sensors[2]

Sensor_Right_A = sensors[3]
Sensor_Right_B = sensors[4]
Sensor_Right_C = sensors[5]

Sensor_Front_A = sensors[6]
Sensor_Front_B = sensors[7]
Sensor_Front_C = sensors[8]

#Incentivation Sprites----------------------------------------------------
incentivation_spr_A = pyg.sprite.GroupSingle( )
incentivation_spr_B = pyg.sprite.GroupSingle( )
incentivation_spr_C = pyg.sprite.GroupSingle( )
incentivation_spr_D = pyg.sprite.GroupSingle( )
incentivation_spr_E = pyg.sprite.GroupSingle( )

incentivation_A = Incentivation_Sprait( (870,360), trash, 0 )
incentivation_B = Incentivation_Sprait( (690,590), trash, 90 )#G
incentivation_C = Incentivation_Sprait( (600,345), trash, 0 )
incentivation_D = Incentivation_Sprait( (570,60), trash, 90 )#G
incentivation_E = Incentivation_Sprait( (360,390), trash, 0 )

incentivation_spr_A.add( incentivation_A )
incentivation_spr_B.add( incentivation_B )
incentivation_spr_C.add( incentivation_C )
incentivation_spr_D.add( incentivation_D )
incentivation_spr_E.add( incentivation_E )

#Implementation--------------------------------------------------------------------------------------------------------------------------------------
all_sensors = [Sensor_Left_A, Sensor_Left_B, Sensor_Left_C, Sensor_Right_A, Sensor_Right_B, Sensor_Right_C, Sensor_Front_A, Sensor_Front_B, Sensor_Front_C]

left_sensors = [Sensor_Left_C, Sensor_Left_B, Sensor_Left_A]
right_sensors = [Sensor_Right_C, Sensor_Right_B, Sensor_Right_A]
frontal_sensors = [Sensor_Front_C, Sensor_Front_B, Sensor_Front_A]

all_sensors_test = [left_sensors,right_sensors,frontal_sensors]

sensor_data = [1,1,1]
sensor_data_default = [1,1,1]

all_AI_hitboxes = [Top_AI_spr, Bot_AI_spr, Edge_AI_spr]
all_Player_hitboxes = [Top_Player_spr,Bot_Player_spr,Obstacles_Player_spr]

all_incentivations = [ incentivation_spr_A, incentivation_spr_B, incentivation_spr_C, incentivation_spr_D, incentivation_spr_E ]
distances = 0
key_human_test = 'S'

data = ['S']
reset_factory = 0

#Empezar todo----------------------------------------------------------------------------------------------------------------------------------------
run = True
clock = pyg.time.Clock()

while run:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False

    #NEURONAL NETWORK SECTION START -----------------------------------------------------------------------------------------------------------------

    reward = 1
    is_crashed = 0

    if not params['train']:
        thinker.epsilon = 0
    else:
        # agent.epsilon is set to give randomness to actions
        thinker.epsilon = 1 - (episodes * params['epsilon_decay_linear'])
        if thinker.epsilon < 0.01:
            thinker.epsilon = 0.01

    last_state = thinker.get_state(is_crashed,sensor_data) #Obtener el estado anterior

    if rn.random() < thinker.epsilon: #Validar si la decision tomada es aleatoria o "pensada" (predecida por la red neuronal)
        arg_max = rn.randint(0,2)
        last_move = to_categorical( arg_max,num_classes=3 )
    else:
        prediction = thinker.model.predict( last_state.reshape((1,-1)) )
        arg_max = np.argmax( prediction[0] )
        last_move = to_categorical( arg_max, num_classes=3 )

    #accionar
    if arg_max == 0: #cero -> derecha
        key_AI = 'RIGHT'
    elif arg_max == 1: #uno -> izquierda
        key_AI = 'LEFT'
    else: #si no, avanza
        key_AI = 'UP'
    
    new_state = thinker.get_state( is_crashed, sensor_data )

    #NEURONAL NETWORK SECTION END -------------------------------------------------------------------------------------------------------------------

    # key_human_test = data[-1]

    key_helper = data[-1] #Aqui poner la coneccion bluetooth
    print( key_helper )
    key_human_test = pyg.key.get_pressed()
    factor = True

    if pyg.sprite.spritecollide( Car_Player_spr.sprite,Obstacles_Player_spr,False,pyg.sprite.collide_mask):
        if not key_human_test[pyg.K_DOWN]:
            factor = False
        player_points -= ( points_losted_per_tick + 0.5 )
        print('Chocaste con un obstaculo')

    if event.type == pyg.MOUSEBUTTONDOWN:
      pos = pyg.mouse.get_pos()
      car_player_sprite.update(0,0,angle,list(pos))
      car_coor = list(pos)

    #Movement player
    movement_player = mv.spritePlayerMovement(Car_Player_spr,speed, angle, rotation, car_coor, key_human_test, factor, key_helper)
    movement_player[0]
    angle = movement_player[2]
    car_coor = movement_player[3]

    #Movement AI
    movement_AI = mv.spriteNeuronalMovement(Car_AI_spr, speed, angle_AI, rotation, car_AI_coor, key_AI, all_sensors)
    movement_AI[0]
    angle_AI = movement_AI[2]
    car_AI_coor = movement_AI[3]

    sensor_data = sensor_data_default
    sensor_data = sn.sense( sensor_data, all_sensors_test, all_AI_hitboxes )

    # print( f'SENSOR: {sensor_data}' )

    #Colisiones--------------------------------------------------------------------------------------------------------------------------------------
    #PLAYER---------------------------------------------------------------
    if pyg.sprite.spritecollide( Car_Player_spr.sprite,Top_Player_spr,False,pyg.sprite.collide_mask):
        player_points -= points_losted_per_tick
        print('Chocaste con la pared TOP')

    if pyg.sprite.spritecollide( Car_Player_spr.sprite,Bot_Player_spr,False,pyg.sprite.collide_mask):
        player_points -= points_losted_per_tick
        print('Chocaste con la pared BOT')
    
    if key_human_test[pyg.K_r] or player_points < 1:
        car_coor = [1100,267]
        car_player_sprite.update( 0,0,0,[1100,267] )
        angle = 0
        player_points = 1000
        reset_factory = pyg.time.get_ticks() / 1000
     
    #NEURONAL NETWORK SECTION 2 START----------------------------------------------------------------------------------------------------------------

    # print( incentivarions )

    # if params['train']:
    #     thinker.train_short_memory( last_state, last_move, reward, new_state, is_crashed == 1 )
    #     thinker.remember( last_state, last_move, reward, new_state, is_crashed == 1 )

    #NEURONAL NETWORK SECTION 2 END------------------------------------------------------------------------------------------------------------------

    #Draw things-------------------------------------------------------------------------------------------------------------------------------------

    #Things for draw------------------------------------------------------
    points_losted_text = 'Puntos: ' + str( round(player_points) )
    screen_points = font.render(points_losted_text, True, color_text)

    timer = round((pyg.time.get_ticks() / 1000) - reset_factory,2)
    timer_text = 'Tiempo: ' + str( timer )
    screen_timer = font.render( timer_text, True, color_text )

    # sensor_text = 'Sensores: I: ' + str( round(sensor_data[0],2) ) + ' |C: ' + str( round(sensor_data[2],2) ) + ' |D: ' + str( round(sensor_data[1],2) )
    # screen_sensor = font.render( sensor_text, True, color_text )

    # last_distance_text = 'Distancia maxima: ' + str( distance ) + ' / ' + str(distances)
    # screen_last_distance = font.render( last_distance_text, True, color_text )
    #Draw visual elements------------------------------------------------------
    
    #Background-----------------------------------------------------------
    display.blit( Background_setter[0], Background_setter[1] )
    # display.blit( Decorations_setter[0], Decorations_setter[1] )

    #Optional draws-------------------------------------------------------
    #HITBOX
    # Walls.draw_hitboxes( all_AI_hitboxes, display )
    # Walls.draw_hitboxes( all_Player_hitboxes, display )
    # Walls.draw_hitboxes( all_incentivations, display )

    Edge_AI_spr.draw( display )

    sn.draw_sensors( all_sensors, display ) #seonsores

    # display.blit( screen_player_position, (980,30) ) #Escribir la coordenada actual del jugador

    #Players--------------------------------------------------------------
    # Car_Player_spr.draw( display )
    Car_AI_spr.draw( display )

    #Top draws-----------------------------------------------------------
    display.blit( screen_points, (150,10) )
    display.blit( screen_timer, (980,10) )

    # display.blit( screen_sensor, (150,30) )
    # display.blit( screen_episode, (150,55) ) #Episodios de aprendizaje
    # display.blit( screen_last_distance, (150,120) )
   
    if pyg.sprite.spritecollide( Car_Player_spr.sprite,Goal_spr,False,pyg.sprite.collide_mask):
        winner_text = 'Ganaste!!'
        screen_winner = winner_font.render( winner_text, True, color_text_2 )

        winner_points_text = 'Puntaje: ' + str( round(player_points) )
        screen_winner_points = winner_font_points.render( winner_points_text, True, color_text_2 )

        display.blit( screen_winner, (500,300) )
        display.blit( screen_winner_points, (530,400) )
        
        print('Victoria')

    pyg.display.flip()
    clock.tick( fps )

    # if params['episodes'] == episodes:
    #     thinker.model.save_weights(params['weights_path'])
    #     sys.exit()

    dw.draw_Neuronal_Network(display,2500)
    dw.draw_nn( thinker.model.weights, arg_max, last_state, display, 2500 )

pyg.quit
