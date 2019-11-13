
import pygame as pg
class Projectile(pg.sprite.Sprite):
    def __init__(self,user_moving_left,x,y,flip): 
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        if user_moving_left == True: #
            self.image = pg.transform(self.image,True, False)
    def update(self):
        if self.direction == "left":
            self.rect.x -= 10
        else:
            self.rect.x += 10
            
#writing to: printing to file; output file: file being writtenuu
# when you open with w it deletes everything # append creates file is DOE and adds n. print add lines in files because it appends it and considers \n ? 
