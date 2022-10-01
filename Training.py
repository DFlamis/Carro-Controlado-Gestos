import pygame as pyg
import random as rn
import numpy as np

import Movement as mv
import Sensors as sn
import Walls

from serial import*
from keras.utils import to_categorical
import sys

# import NeuronalNetwork.Draw as dw
from NeuronalNetwork.Saki import QLAgent


#General variables-----------------------------------------------------------------------------------------------------------------------------------
root_AI_path = 'AI_Resources/'
episodes = 0

rewards_touched = 0

fps = 60
rotation = 4
speed = 5
angle_AI = 0

car_AI_coor = [1100,267]

display_size = 1280,720
display = pyg.display.set_mode(display_size)

color = (0,0,0)

#Car-------------------------------------------------------------------------------------------------------------------------------------------------
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

car_AI_sprite = Car_Sprait( root_AI_path )
car_AI_spr = pyg.sprite.GroupSingle( car_AI_sprite )

#Sensors---------------------------------------------------------------------------------------------------------------------------------------------
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

#Walls-----------------------------------------------------------------------------------------------------------------------------------------------
walls = Walls.walls_for_training( root_AI_path )

Wall_A = walls[0]
Wall_B = walls[1]
Wall_C = walls[2]
Wall_D = walls[3]

reward_spr = walls[4]

#Implementation--------------------------------------------------------------------------------------------------------------------------------------
all_sensors = [Sensor_Left_A, Sensor_Left_B, Sensor_Left_C, Sensor_Right_A, Sensor_Right_B, Sensor_Right_C, Sensor_Front_A, Sensor_Front_B, Sensor_Front_C]

left_sensors = [Sensor_Left_C, Sensor_Left_B, Sensor_Left_A]
right_sensors = [Sensor_Right_C, Sensor_Right_B, Sensor_Right_A]
frontal_sensors = [Sensor_Front_C, Sensor_Front_B, Sensor_Front_A]

all_sensors_test = [left_sensors,right_sensors,frontal_sensors]

sensor_data = [1,1,1]
sensor_data_default = [1,1,1]

all_AI_hitboxes = [Wall_A, Wall_B, Wall_C, Wall_D]

hitbox = rn.choice( all_AI_hitboxes )

#Neuronal Network------------------------------------------------------------------------------------------------------------------------------------
def define_parameters():
	params = dict()
	params['epsilon_decay_linear'] = 1 / 100
	params['learning_rate'] = 0.001
	params['first_layer_size'] = 12  # neurons in the first layer
	params['second_layer_size'] = 8  # neurons in the second layer
	params['episodes'] = 150
	params['memory_size'] = 400000
	params['batch_size'] = 1000
	params['weights_path'] = 'AI_memory-12-8-c150.hdf5'
	params['train'] = True #True -> para entrenar -- False -> recordar
	if params['train']:
		params['load_weights'] = False
	else:
		params['load_weights'] = True
	return params

params = define_parameters()
thinker = QLAgent( params )

#Game------------------------------------------------------------------------------------------------------------------------------------------------
run = True

while run:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
    
    

    #NEURONAL NETWORK SECTION START -----------------------------------------------------------------------------------------------------------------

    reward = 0
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

    #Movement----------------------------------------------------------------------------------------------------------------------------------------
    movement_AI = mv.spriteNeuronalMovement(car_AI_sprite, speed, angle_AI, rotation, car_AI_coor, key_AI, all_sensors)
    movement_AI[0]
    angle_AI = movement_AI[2]
    car_AI_coor = movement_AI[3]

    sensor_data = sensor_data_default
    sensor_data = sn.sense( sensor_data, all_sensors_test, all_AI_hitboxes )

    #Training----------------------------------------------------------------------------------------------------------------------------------------
    if pyg.sprite.spritecollide( car_AI_sprite,hitbox,False,pyg.sprite.collide_mask):
        is_crashed = 1
        reward = -20
        car_AI_coor = [1100,267]
        angle_AI = 0
        distance = 0
        episodes += 1
        hitbox = rn.choice( all_AI_hitboxes )
    
    if pyg.sprite.spritecollide( car_AI_sprite,reward_spr,False,pyg.sprite.collide_mask):
        reward = 10
        rewards_touched += 1
        car_AI_coor = [1100,267]
        angle_AI = 0
        episodes += 1
        hitbox = rn.choice( all_AI_hitboxes )
    
    # if key_AI == 'UP':
    #     reward = 1
    
    #NEURONAL NETWORK SECTION 2 START----------------------------------------------------------------------------------------------------------------
    human_key = pyg.key.get_pressed()

    if params['train']:
        thinker.train_short_memory( last_state, last_move, reward, new_state, is_crashed == 1 )
        thinker.remember( last_state, last_move, reward, new_state, is_crashed == 1 )
    
    if params['episodes'] == episodes or human_key[pyg.K_s]:
        thinker.model.save_weights(params['weights_path'])
        sys.exit()
    #NEURONAL NETWORK SECTION 2 END------------------------------------------------------------------------------------------------------------------

    #Draws-------------------------------------------------------------------------------------------------------------------------------------------
    display.fill( color )
    hitbox.draw( display )
    reward_spr.draw( display )
    car_AI_spr.draw( display )
    sn.draw_sensors( all_sensors, display ) #seonsores

    print( episodes )
    print( rewards_touched )

    pyg.display.flip()

