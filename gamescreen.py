#Made by Donald Yang
#imgs made by

from os.path import join
import os

import pygame as pg
from random import choice

from collision import rectTest


pg.init()

def loadMaps(folder_path):
    maps_database = {}
    for file in os.listdir(folder_path):
        if file.endswith("txt"):
            map_data = []
            try:
                with open(folder_path + "\\" + file,"r") as my_file:
                    data = my_file.read().split("\n")
                    for line in data:
                        map_data.append(list(line))
            except FileNotFoundError:
                print("file not found: "+ file)
            maps_database[file[:-4]] = map_data
    return maps_database

def loadImgs(bgFolder_Path,shipFolder_Path): 
    bg_database,ship_parts = [],[]
    for img in os.listdir(bgFolder_Path):
        loaded_img = pg.image.load(bgFolder_Path + "\\" + img).convert()
        loaded_img.set_colorkey((0,0,0))
        bg_database.append(loaded_img)
    for img in os.listdir(shipFolder_Path):
        loaded_img = pg.transform.scale(pg.image.load(shipFolder_Path + "\\" + img).convert(),(33,48))
        loaded_img.set_colorkey((255,255,255))
        ship_parts.append(loaded_img)
    return bg_database,ship_parts

        
class window():
    def __init__(self):
        self.WINDOW_SIZE = (696,466) # 300 200. ratio 3 by 2 is most common
        self.screen = pg.display.set_mode(self.WINDOW_SIZE) # initiate the window
        self.display = pg.Surface((438,292)) # surface for rendering; scaled to window size at end
        self.clock = pg.time.Clock() 
        self.background_img = pg.transform.scale(pg.image.load(join("Backgrounds","darkpurple.png")),(self.WINDOW_SIZE)).convert()
        self.bg_objects = [[1/4.5,[10,7.5]],[1/2,[129,55]],[1/2.7,[210,100]],[1/2.2,[400,50]],[1/4.5,[500,71]],[1/2,[650,55]],[1/2.7,[800,150]]] #order means which one overlap one another. ex index 2 overlaps 1
        self.bg_imgs,self.ship_parts = loadImgs((join('SpaceShooter_Assets','PNG','Damage')),("ship_parts"))
        self.difference = [0,0] # x and y. based on how far camera moves.
        self.captions = pg.display.set_caption('Lost in Space') 
        self.stage_num = 0
        self.state = "GameMap0"
        self.maps_database = loadMaps("GameMaps")
        self.health_font = pg.font.Font(join("health","zero_hour.ttf"),17)
        self.health_font.set_bold(True)
        self.health_font.set_underline(True)
        self.vertCubesDatabase = {} #entire horizontal line
        self.vertCubeData = {} #one cube
        self.time_font = pg.font.Font(join("health","zero_hour.ttf"),15)
        self.time = 0 #seconds
        
        
    def bgParallaxScroll(self,resize):
        """
        #(surface,rgb,rect(x,y,width,height))
    #pg.draw.rect(win.display,(100, 192, 207),pg.Rect(0,25,300,65)) #background
    #Rect(x,y,width,height). mutiple rs difference for lag effect. greatest to least. change location.
        """
        n = 0 #dont make this an infinite loop lest you crash it
        #pg.draw.rect(self.display,(250, 255, 50),pg.Rect(10,250,120,270))
        for eachObject in self.bg_objects:
            try:
                x,y = eachObject[1][0]-resize[0]*eachObject[0],  eachObject[1][1]-resize[1]*eachObject[0] #x,y 
                self.display.blit(self.bg_imgs[n],(x,y))
                n += 1
            except:
                n = 0
            
    
    def lifeCount(self,user_health):
        message = "Lives Left: " + str(user_health)
        rendered_text = self.health_font.render(message,True, (0,0,0))
        self.display.blit(rendered_text,(self.display.get_width() - rendered_text.get_width() - 1, 1 ))
        
    def showTimer(self,time):
        self.time += 1/60
        message = "Timer:" + f" {self.time:.2f}" 
        rendered_text = self.time_font.render(message,True, (0,0,0))
        self.display.blit(rendered_text,(1.5 , 1.5))
        
        
    def drawCube(self,rect,side,color):
        vertices = [[rect.x,rect.y]]
        startPt = [rect.x,rect.y] 
        formulas = [(8,-8),(side,0),(-8,8),(0,side),(8,-8),(0,-side),(0,side),(-side,0),(0,-side),(0,side),(-8,8)]
        for direction in formulas:
            startPt[0] += direction[0]
            startPt[1] += direction[1]
            vertices.append(startPt[:]) #make vertices database
        pg.draw.lines(self.display,color,False,vertices,1)
    #pg.draw.polygon(win.display,(21,121,143),vertices[:4]) #works but doesnt look good
    
    def makeCube(self,x,y,tile_rects,side,color,enableCol):
        
        self.colRect = pg.Rect((x*side),(y*side),side,side)
        
        if enableCol == True:
            tile_rects.append(self.colRect)
            
        displayRect = pg.Rect(self.colRect.x - self.difference[0],self.colRect.y - self.difference[1],side,side)
        self.drawCube(displayRect,side,color)
        pg.draw.rect(self.display,color,displayRect,1)
    
    
    def makeVerticalMovingCubes(self,x,y,user,tile_rects,color): #layer,speed,
        enableCol = True
        
        if y not in self.vertCubesDatabase:
            
            self.vertCubesDatabase[y] = {"speed": -0.0015 * choice([1,-1]),"displacement": 0} #includes all cubes with the y value. Not to be mistaken for an individual tile
        
        
        if abs(self.vertCubesDatabase[y]["displacement"]) >= abs(self.vertCubesDatabase[y]["speed"] * 60 * 25): #2.5 sec
            self.vertCubesDatabase[y]["speed"] = -self.vertCubesDatabase[y]["speed"]  #changes direction 
            
                #make another database for individual blocks
                
                
                
                

        #self.makeCube(x,y - (self.vertCubesDatabase[y]["displacement"]),tile_rects,18,color,True)    
            
            
            
        col_list = rectTest(user.player_rect,tile_rects,True)
        for tile in col_list:
            
            defaultX = (tile.x/18)
            defaultY = round((tile.y/18) + self.vertCubesDatabase[y]["displacement"])
            
            if (defaultX,defaultY) not in self.vertCubeData:
                self.vertCubeData[(defaultX,defaultY)] = 0
                
            
            if self.vertCubeData[(defaultX,defaultY)] < 3:
                self.vertCubeData[(defaultX,defaultY)] += 1/600

            
            
            else:

                enableCol = False
        
                
        if self.vertCubeData.get((x,y)) == None or self.vertCubeData[(x,y)] < 1:
            self.makeCube(x,y - (self.vertCubesDatabase[y]["displacement"]),tile_rects,18,color,enableCol) 

        self.vertCubesDatabase[y]["displacement"] += self.vertCubesDatabase[y]["speed"]
        
        

            


            

            
            
            
                
                
                
            
            
            
            
            

        
        



    
    
    
        





    
