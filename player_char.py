import pygame as pg
from music import fallSound

class player(pg.sprite.Sprite): 
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0 # necessary because movement speed rounds down. miliseconds
        self.player_flip = False # flipping idle image 
        self.enableDoubleJump = False
        self.player_action = "static"
        self.player_frame = 0
        self.spawn_loc, self.spawned = [50,50], False #48              #43
        self.player_rect = pg.Rect(self.spawn_loc[0],self.spawn_loc[1],43,50) # x,y, width and height. get_rect not implemented because image size change
        self.right_border, self.bottom_border = 0, 0
        self.health = 3
    def move(self): #keypresses
        self.player_movement = [0,0] #do this because it has to be reset each time
        if self.moving_right == True:
            self.player_movement[0] +=4 #adjust horizontal speed here
        elif self.moving_left == True:
            self.player_movement[0] -= 4
        self.player_movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.26 #gravity
        if self.vertical_momentum > 5: #max gravity 
            self.vertical_momentum = 5
        #elf.player_movement[1] += self.vertical_momentum
    def new_action(self,old_action,frame_value,new_action):
        if old_action != new_action:
            old_action = new_action
            frame_value = 0 #resets to new animation 1st frame image.
        return old_action,frame_value
    def update(self):
        
        if self.player_movement[0] != 0:
            self.player_action, self.player_frame = self.new_action(self.player_action, self.player_frame, "walk")
            if self.player_movement[0] > 0:
                self.player_flip = False
            else:
                self.player_flip = True
        if self.player_movement[0] == 0:
            self.player_action, self.player_frame = self.new_action(self.player_action,self.player_frame,"static")
        if self.player_movement[1] < 0:
            self.player_action, self.player_frame = self.new_action(self.player_action,self.player_frame,"jump")
        self.player_frame += 1
        
    def boundaries(self):
        if self.player_rect.y >= self.bottom_border:
            fallSound.play()
            self.health -= 1
            self.spawned = False
        elif self.player_rect.x >= self.right_border -43:
            self.player_rect.x = self.right_border - 43
        elif self.player_rect.x <= 0 :
            self.player_rect.x = 0
        
                  
   
        



