import pygame
from os.path import join
#dictionary comprehension
#{c:string.count()}

pygame.init
states = {
    "Oregon": "OR",
    "Florida" : "FL",
    "California" : "CA",
    "New York" : "NY",
    "Michigan": "MI"
}



cities = {
    "CA" : "San Franciso",
    "MI" : "Michigan",
    "FL" : "Florida",
    "OR" : "Oregon",
    "NY" : "New York"
}

#items give you the index string and its : value. so use index 1
#for i,v in states.items():
    #print(cities[v])

#def applyRules(self,char):

#rules = {"x':}
    #return self.rules.get(char,"lol")
    
#path to folder. image_duration is set ex[7,7]

#fall damage based on vertical momentum
#jumping blocks. rect
#different stages.
#make sure your dir is in the folder for this.


#put loadanimations into playeruser. pygame.sprite.Sprite

# main and then all the code in sources
import random, sys

class Hero(pygame.sprite.Sprite):
    def __init__(self,name,pos,imagepath):
        pygame.sprite.Sprite.__init__(self)
        self.name = name 
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.direction = "right"
        self.strength, self.speed, self.itel = (2,3,5)
    def move(self,dir):
        if dir == "down":
            self.rect.y += self.speed
        if dir == "up":
            self.rect.y -= self.speed
        elif dir == "right":
            self.rect.x += self.speed
            if self.direction == "left":
                self.drection = "right"
                self.image = pygame.transform.flip(self.image,True, False)
        elif dir == "left":
            self.rect.x -= self.speed
            if self.direction == "right":
                self.drection = "left"
                self.image = pygame.transform.flip(self.image,True, False)
    def fight(self,opponent):
        return random.choice(True,False)
                
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
            
class Controller:
    def __init__(self,width=640, height = 480):
        self.screen = pygame.display.set_mode((width,height))
        self.background == pygame.Surface(self.screen.get_size,())
        self.width = width
        pygame.font.init()
        self.height = height
        self.hero = Hero("Bob",(width/3, height/3), "hero.png")
        self.enemy = Hero('BadGuy', (width-100,height-150),"enemy.png") #Subclass  dont do this
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group((self.hero,self.enemy))
        self.STATE = "Game"
    def mainloop(self):
        while True:
            if self.STATE = "Game":
                self.gameloop()
            elif self.STATE == "Exit":
                self.endloop()
    def gameloop(self):
        pygame.key.set_repeat(1,50) #set events, 50 millisecond between repeat
        while self.STATE = "Game":
            self.background.fill(149,249,12)
            for event in pygame.event.get(): #gets list of all event called
                if event.type == pygame.Quit:
                    sys.exit() #memory get cleaned up
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.hero.move("up")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.hero.move("down")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.hero.move("left")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
        hits = pygame.sprite.spritecollide(self.enemy,self.bullets,True)
        if hits = 3: #or just (hits) IMPORTANT
            self.STATE = "EXIT"
            
        self.bullets.update()
        
        self.screen.blit(self.background,(0,0))
        self.bullets.draw(self.screen)
        self.screen.blit(self.hero.image, (self.hero.rect.x, self.hero.rect.y))
        self.screen.blit(self.enemy.image, (self.enemy.rect.x, self.enemy.rect.y))
        pygame.display.flip()
        
        def endloop(self):
            self.hero.kill()
            myfont = pygame.font.SysFont(None,30) #style,size
            message = myfont.render("Game Over",False,(0,0,0))
            self.screen.blit(message,((self.width)/2,(self.height)/2))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()


def main():
    game = Controller()
    game.mainloop()
    
main()
                        
                        

    

        

            
            
        
    