import pygame as pyg

side = 'A'
front = 'B'
corner = 'C'

class Sensor_Sprait(pyg.sprite.Sprite): #Objeto de cada sensor
    def __init__(self, x, y, variation, angle, root_path):
        super().__init__()
        self.path = root_path
        self.idk = variation

        self.image = pyg.image.load( self.path + 'Sensor' + self.idk + '.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (x,y)) #1100,267
        self.mask = pyg.mask.from_surface(self.image)
        
        self.this_x = x
        self.this_y = y

        self.angle = angle
        self.separation_x = 1100 - x
        self.separation_y = 267 - y

    def update(self, axis_x, axis_y, angle):
        self.image = pyg.image.load( self.path + 'Sensor' + self.idk + '.png' ).convert_alpha()

        self.image = pyg.transform.rotate( self.image, angle )

        self.rect = self.image.get_rect( center = (axis_x, axis_y) )

def draw_sensors(all_sensros, display):
    for sensor in all_sensros:
        sensor.draw( display )
    
def sense(sensor_data, all_sensors, all_hitboxes):

    default_data = 1
    reduction_factor = 0.25
    collitions = 0

    pointer = 0
    subPointer = 0

    for sensor_pack in all_sensors:
        for sensor in sensor_pack:
            subPointer += 1
            for hitbox in all_hitboxes:
                if pyg.sprite.spritecollide( sensor.sprite,hitbox,False,pyg.sprite.collide_mask):
                    collitions = subPointer
                sensor_data[pointer] = default_data - (reduction_factor * collitions)
        subPointer = 0
        collitions = 0
        pointer += 1

    return sensor_data

def generate_sensors(root_path):

    #LEFT---------------------------------------
    Sensor_Left_A = pyg.sprite.GroupSingle( )
    Sensor_Left_B = pyg.sprite.GroupSingle( )
    Sensor_Left_C = pyg.sprite.GroupSingle( )

    Sensor_LA = Sensor_Sprait(1100,300,side,90,root_path)
    Sensor_LB = Sensor_Sprait(1100,310,side,90,root_path)
    Sensor_LC = Sensor_Sprait(1100,320,side,90,root_path)

    Sensor_Left_A.add( Sensor_LA )
    Sensor_Left_B.add( Sensor_LB )
    Sensor_Left_C.add( Sensor_LC )

    #RIGHT--------------------------------------
    Sensor_Right_A = pyg.sprite.GroupSingle( )
    Sensor_Right_B = pyg.sprite.GroupSingle( )
    Sensor_Right_C = pyg.sprite.GroupSingle( )

    Sensor_RA = Sensor_Sprait(1100,235,side,90,root_path)
    Sensor_RB = Sensor_Sprait(1100,225,side,90,root_path)
    Sensor_RC = Sensor_Sprait(1100,215,side,90,root_path)

    Sensor_Right_A.add( Sensor_RA )
    Sensor_Right_B.add( Sensor_RB )
    Sensor_Right_C.add( Sensor_RC )

    #FRONT--------------------------------------
    Sensor_Front_A = pyg.sprite.GroupSingle( )
    Sensor_Front_B = pyg.sprite.GroupSingle( )
    Sensor_Front_C = pyg.sprite.GroupSingle( )

    Sensor_FA = Sensor_Sprait(1045,267,front,0,root_path)
    Sensor_FB = Sensor_Sprait(1035,267,front,0,root_path)
    Sensor_FC = Sensor_Sprait(1025,267,front,0,root_path)

    Sensor_Front_A.add( Sensor_FA )
    Sensor_Front_B.add( Sensor_FB )
    Sensor_Front_C.add( Sensor_FC )

    #CORNER RIGHT-------------------------------

    #CORNER LEFT--------------------------------
    
    return Sensor_Left_A, Sensor_Left_B, Sensor_Left_C, Sensor_Right_A, Sensor_Right_B, Sensor_Right_C, Sensor_Front_A,Sensor_Front_B, Sensor_Front_C