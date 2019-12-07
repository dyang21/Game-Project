import pygame as pg
from os.path import join

class buttons:
    def __init__(self,color,x,y,width,height,text,size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font = pg.font.Font(join("assets","health","zero_hour.ttf"),size)
        self.font.set_bold(True)
        self.text = self.font.render(text,True,(0,0,0))
        
    def drawButton(self,screen):
        pg.draw.rect(screen, (0,0,0), (self.x,self.y,self.width,self.height))
        pg.draw.rect(screen,self.color,(self.x + 4,self.y + 4,self.width - 8,self.height - 8))
        
        screen.blit(self.text, (self.x + (self.width/2 - self.text.get_width()/2), self.y + (self.height/2 - self.text.get_height()/2)))
        
    def overButton(self,pos): 
        if pos[0] > self.x  and pos[0] < self.x + self.width and pos[1] > self.y  and pos[1] < self.y + self.height:
            return True
        else:
            return False
        
playButton = buttons((255,255,255),116,106,210,60,"Play",30) 
#color,x,y,width,height,text

scoreButton = buttons((255,255,255),140,180,160,45,"High Scores", 14)

quitButton = buttons((255,255,255),170,245,100,30,"Quit",15)

      
        
####Menu

retryButton = buttons((100,100,100),120,48,200,60,"Retry",19) 

pauseMenuQuit = buttons((100,100,100),140,200,160,45,"Quit",17) 

##victory
retryVic = buttons((100,100,100),120,120,200,60,"Retry",19) #60, 180, 100, 50
scoreVic = buttons((100,100,100),30,200,130,50,"Scores",18)
quitVic = buttons((100,100,100),277,200,130,50,"Quit",18)

#highScore

backButton = buttons((255,255,255),170,245,100,30,"Back",16)
        