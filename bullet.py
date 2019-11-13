#ignore

import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self,direction,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        if direction == "right":
            self.image = pygame.transform(self.image,True, False)
    def update(self):
        if self.direction == "left":
            self.rect.x -= 10
        else:
            self.rect.x += 10

        
        
        