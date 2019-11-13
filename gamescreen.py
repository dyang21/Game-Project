#Made by Donald Yang
#imgs made by

from os.path import join
import os

import pygame as pg

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
            except OSError:
                print("Error finding this file: "+ file)
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
        self.WINDOW_SIZE = (600,400) # 300 200. ratio 3 by 2 is most common
        self.screen = pg.display.set_mode(self.WINDOW_SIZE) # initiate the window
        self.display = pg.Surface((420,280)) # surface for rendering; scaled to window size at end
        self.clock = pg.time.Clock() 
        self.background_img = pg.transform.scale((pg.image.load(join("SpaceShooter_Assets","Backgrounds","darkpurple.png"))).convert(),(self.WINDOW_SIZE))
        self.bg_objects = [[1/4.5,[10,7.5]],[1/2,[129,55]],[1/2.7,[210,100]],[1/2.2,[400,50]]] #order means which one overlap one another. ex index 2 overlaps 1
        self.bg_imgs,self.ship_parts = loadImgs((join('SpaceShooter_Assets','PNG','Damage')),("ship_parts"))
        self.float_difference = [0,0] # x and y. based on how far camera moves.
        self.captions = pg.display.set_caption('Lost in Space') 
        self.stage_num = 0
        self.state = "GameMap0"
        self.maps_database = loadMaps("GameMaps")
        self.right_border = 0
        
    def bgParallaxScroll(self,resize):
        """
        #(surface,rgb,rect(x,y,width,height))
    #pg.draw.rect(win.display,(100, 192, 207),pg.Rect(0,25,300,65)) #background
    #Rect(x,y,width,height). mutiple rs difference for lag effect. greatest to least. change location.
        """
        n = 0
        #pg.draw.rect(self.display,(250, 255, 50),pg.Rect(10,250,120,270))
        for eachObject in self.bg_objects:
            x,y = eachObject[1][0]-resize[0]*eachObject[0],  eachObject[1][1]-resize[1]*eachObject[0] #x,y 
            self.display.blit(self.bg_imgs[n],(x,y))
            if n >= len(self.bg_imgs)-1:
                n = 0
            else:
                n += 1




    
