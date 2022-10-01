import pygame as pyg

class Wall_Sprait(pyg.sprite.Sprite):
    def __init__(self, root_path, file_name):
        super().__init__()

        self.image = pyg.image.load( root_path + file_name + '.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (640,360)) #640,270
        self.mask = pyg.mask.from_surface(self.image)

def draw_hitboxes( hitboxes, display ):
    for hitbox in hitboxes:
        hitbox.draw( display )

def walls_generator(root_Player_path, root_AI_path):
    #Player--------------------------------------
    Top_Player_spr = pyg.sprite.GroupSingle( )
    Bot_Player_spr = pyg.sprite.GroupSingle( )
    Obstacles_Player_spr = pyg.sprite.GroupSingle( )

    Top_Player_sprite = Wall_Sprait( root_Player_path, 'Top' )
    Bot_Player_sprite = Wall_Sprait( root_Player_path, 'Bot' )
    Obstacles_Player_Sprite = Wall_Sprait( root_Player_path, 'Obstacles' )

    Top_Player_spr.add( Top_Player_sprite )
    Bot_Player_spr.add( Bot_Player_sprite )
    Obstacles_Player_spr.add( Obstacles_Player_Sprite )

    #AI------------------------------------------
    Top_AI_spr = pyg.sprite.Group( )
    Bot_AI_spr = pyg.sprite.Group( )
    Edge_AI_spr = pyg.sprite.GroupSingle( )

    Top_AI_sprite = Wall_Sprait( root_AI_path, 'Top' )
    Bot_AI_sprite = Wall_Sprait( root_AI_path, 'Bot' )
    Edge_AI_sprite = Wall_Sprait( root_AI_path, 'Edges' )

    Top_AI_spr.add( Top_AI_sprite )
    Bot_AI_spr.add( Bot_AI_sprite )
    Edge_AI_spr.add( Edge_AI_sprite )

    return Top_Player_spr, Bot_Player_spr,Obstacles_Player_spr, Top_AI_spr, Bot_AI_spr, Edge_AI_spr

def walls_for_training( root_AI_path ):

    #AI------------------------------------------
    Wall_A_spr = pyg.sprite.Group( )
    Wall_B_spr = pyg.sprite.Group( )
    Wall_C_spr = pyg.sprite.Group( )
    Wall_D_spr = pyg.sprite.Group( )
    Reward_spr = pyg.sprite.Group( )

    Wall_A_sprite = Wall_Sprait( root_AI_path, 'Wall_A' )
    Wall_B_sprite = Wall_Sprait( root_AI_path, 'Wall_B' )
    Wall_C_sprite = Wall_Sprait( root_AI_path, 'Wall_C' )
    Wall_D_sprite = Wall_Sprait( root_AI_path, 'Wall_D' )
    Reward_sprite = Wall_Sprait( root_AI_path, 'Rewards' )

    Wall_A_spr.add( Wall_A_sprite )
    Wall_B_spr.add( Wall_B_sprite )
    Wall_C_spr.add( Wall_C_sprite )
    Wall_D_spr.add( Wall_D_sprite )
    Reward_spr.add( Reward_sprite )

    return Wall_A_spr, Wall_B_spr, Wall_C_spr, Wall_D_spr, Reward_spr