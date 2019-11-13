import pygame as pg

class player(pg.sprite.Sprite): 
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0 # necessary because movement speed rounds down. miliseconds
        self.flip2 = False # flipping idle image 
        self.enableDoubleJump = False
        self.player_action = "static"
        self.player_frame = 0
        self.player_flip = False
        self.spawn_loc, self.spawned = [50,50], False
        self.player_rect = pg.Rect(self.spawn_loc[0],self.spawn_loc[1],21,54) # x,y, width and height. get_rect not implemented because image size change
    def move(self):
        self.player_movement = [0,0] #do this because it has to be reset each time
        if self.moving_right == True:
            self.player_movement[0] +=4 #adjust horizontal speed here
        elif self.moving_left == True:
            self.player_movement[0] -= 4
        self.player_movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.2 #gravity
        if self.vertical_momentum > 3: #max height 
            self.vertical_momentum = 3
    def new_action(self,old_action,frame_value,new_action):
        if old_action != new_action:
            old_action = new_action
            frame_value = 0 #resets to new animation 1st frame image.
        return old_action,frame_value
    def update(self):
        if self.player_movement[0] > 0:
            self.player_action, self.player_frame = self.new_action(self.player_action, self.player_frame, "in_motion")
            self.player_flip = False
            self.flip2 = True
        if self.player_movement[0] < 0:
            self.player_action, self.player_frame = self.new_action(self.player_action, self.player_frame, "in_motion")
            self.player_flip = True
            self.flip2 = False
        if self.player_movement[0] == 0:
            self.player_action, self.player_frame = self.new_action(self.player_action,self.player_frame,"static")
            self.player_flip = self.flip2
        
                  
   
        



