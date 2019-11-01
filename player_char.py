import pygame

class player(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0 # necessary because movement speed rounds down.
        self.flip2 = False
        self.enableDoubleJump = False
        self.player_action = "idle"
        self.player_frame = 0
        self.player_flip = False
        self.player_rect = pygame.Rect(100,100,23,54) # x,y, width and height. important
        
def change_action(old_action,frame_value,new_action):
    if old_action != new_action:
        old_action = new_action
        frame_value = 0
    return old_action,frame_value



