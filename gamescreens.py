#Made by Donald Yang
#imgs made by

from os.path import join
import os
import json

import pygame as pg
from random import choice

from collision import rectTest


pg.init()

def loadMaps(folder_path):
    """
    parameters: str
    loads map into dictionary
    returns dict
    
    """
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
    """
    parameters: str,str
    loads imgs into seperate list
    returns lists
    
    """
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



def loadScores(time = 0 , update = False):
    with open("high_scores.json") as f1:
        data1 = json.load(f1)
    user = "Player " + str(len(data1) + 1)
    save = data1.copy() # now the scores are saved into the win object
    if update == True:
        data1.update({str(user):float((f" {time:.2f}"))})   
        with open("high_scores.json", "w") as f2:
            json.dump(data1,f2)
    return save
    


class window():
    def __init__(self):
        self.WINDOW_SIZE = (696,466) # 300 200. ratio 3 by 2 is most common
        self.screen = pg.display.set_mode(self.WINDOW_SIZE) # initiate the window
        self.display = pg.Surface((438,292)) # surface for rendering; scaled to window size at end
        self.clock = pg.time.Clock()
        self.menuBG_img = pg.transform.scale(pg.image.load(join("Backgrounds/blue.png")),(self.WINDOW_SIZE)).convert()
        self.gameBG_img = pg.transform.scale(pg.image.load(join("Backgrounds/darkPurple.png")),(self.WINDOW_SIZE)).convert()
        self.bg_objects = [[1/4.5,[10,7.5]],[1/2,[129,55]],[1/2.7,[210,100]],[1/2.2,[400,50]],[1/4.5,[500,71]],[1/2,[650,55]],[1/2.7,[800,150]]] #order means which one overlap one another. ex index 2 overlaps 1
        self.bg_imgs,self.ship_parts = loadImgs("Damage", "ship_parts")
        self.difference = [0,0] # x and y. based on how far camera moves.
        self.captions = pg.display.set_caption('Lost in Space')
        self.stage_num = 0
        self.state = "GameMap0"
        self.maps_database = loadMaps("GameMaps")
        self.health_font = pg.font.Font(join("health","zero_hour.ttf"),17)
        self.health_font.set_bold(True)
        self.health_font.set_underline(True)
        self.vertCubesDatabase = {} #same displacement for entire horizontal line in y
        self.vertCubeData = {} #one vert disappearing cube.
        self.horiCubeDatabase = {} #also same displacement in x
        self.disCubeData = {} #static disappearing cub
        self.time_font = pg.font.Font(join("health","zero_hour.ttf"),15)
        self.time = 0 #seconds
        self.turns = 0 #for hor cubes
        self.pause = False
        self.scores = loadScores()

        
    def singleText(self,fontsize,message,x,y,bold = True, color = (0,0,0),underline = False):
        text = pg.font.Font(join("health","zero_hour.ttf"),fontsize)
        text.set_bold(bold)
        text.set_underline(underline)
        rendered_text = text.render(message,True, color)
        self.display.blit(rendered_text,(x,y))
        
    def paragraph(self,paragraph,size,x,y):
        rawMessage = paragraph.split("\n")
        text = pg.font.Font(join("health","zero_hour.ttf"),size)
        for line in rawMessage:
            rendered_text = text.render(line,True, (0,0,0))
            self.display.blit(rendered_text,(x,y))
            y += (text.get_height() + 4)
        

    def bgParallaxScroll(self,resize):
        """
        parameters: int
        blits bg imgs from class attribute. 
        returns none
        """

        #(surface,rgb,rect(x,y,width,height))
    #pg.draw.rect(win.display,(100, 192, 207),pg.Rect(0,25,300,65)) #background
    #Rect(x,y,width,height). mutiple rs difference for lag effect. greatest to least. change location.

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
        """
        parameters: int
        blits user health onto screen
        returns none
        """
        message = "Lives Left: " + str(user_health)
        rendered_text = self.health_font.render(message,True, (0,0,0))
        self.display.blit(rendered_text,(self.display.get_width() - rendered_text.get_width() - 1, 1 ))

    def showTimer(self,time):
        """
        parameters: float
        blits time onto screen
        returns none
        """
        if self.pause == False:
            self.time += 1/60
        message = "Timer:" + f" {self.time:.2f}"
        rendered_text = self.time_font.render(message,True, (0,0,0))
        self.display.blit(rendered_text,(1.5 , 1.5))


    def drawCube(self,rect,side,color):
        """
        parameters: rect,int,tuple
        draws the sides of the cube
        returns none
        """
        vertices = [[rect.x,rect.y]]
        startPt = [rect.x,rect.y]
        formulas = [(8,-8),(side,0),(-8,8),(0,side),(8,-8),(0,-side),(0,side),(-side,0),(0,-side),(0,side),(-8,8)]
        for direction in formulas:
            startPt[0] += direction[0]
            startPt[1] += direction[1]
            vertices.append(startPt[:]) #make vertices database
        pg.draw.lines(self.display,color,False,vertices,1)
    #pg.draw.polygon(win.display,(21,121,143),vertices[:4]) #works but doesnt look good

    def makeCube(self,x,y,tile_rects,side,color,enableCol,anotherList = False):
        """
        parameters: int,int,list,int,tuple,bool,bool
        creates rect for cube and blits it on the screen
        returns none
        """

        self.colRect = pg.Rect((x*side),(y*side),side,side)

        if enableCol == True:
            tile_rects.append(self.colRect)

        if anotherList != False:
            anotherList.append(self.colRect)

        displayRect = pg.Rect(self.colRect.x - self.difference[0],self.colRect.y - self.difference[1],side,side)
        self.drawCube(displayRect,side,color)
        pg.draw.rect(self.display,color,displayRect,1)


    def makeVerticalMovingCubes(self,x,y,user,tile_rects,color,vert_rects): #layer,speed,
        """
        parameters: int,int,object,list,tuple,list
        creates vertical moving cubes. using dictionary to keep track of speed and displacement
        returns none
        """
        if y not in self.vertCubesDatabase:

            self.vertCubesDatabase[y] = {"speed": -0.005 * choice([1,-1]),"displacement": 0} #includes all cubes with the y value. Not to be mistaken for an individual tile
        if abs(self.vertCubesDatabase[y]["displacement"]) >= abs(self.vertCubesDatabase[y]["speed"] * 60 * 6): #6. sec?
            self.vertCubesDatabase[y]["speed"] = -self.vertCubesDatabase[y]["speed"]  #changes direction

                #make another database for individual blocks
        #self.makeCube(x,y - (self.vertCubesDatabase[y]["displacement"]),tile_rects,18,color,True)

        if self.vertCubeData.get((x,y)) == None or self.vertCubeData[(x,y)] < 1:
            self.makeCube(x,y - (self.vertCubesDatabase[y]["displacement"]),tile_rects,18,color,True,vert_rects)
            
        if self.pause == False:
            col_list = rectTest(user.player_rect,vert_rects,True)

            for tile in col_list:

                defaultX = (tile.x/18)
                defaultY = round((tile.y/18) + self.vertCubesDatabase[y]["displacement"])

                if (defaultX,defaultY) not in self.vertCubeData:
                    self.vertCubeData[(defaultX,defaultY)] = 0

            
                if self.vertCubeData[(defaultX,defaultY)] < 2: # 2 secs?
                    self.vertCubeData[(defaultX,defaultY)] += 3/600


        if self.pause == False:
            self.vertCubesDatabase[y]["displacement"] += self.vertCubesDatabase[y]["speed"]

        #save the dispalcement let the tile droppppp in database

    def disappearingCubes(self,x,y,user,tile_rects,color,dis_rects):
        """
        parameters: int,int,object,list,tuple,list
        creates disappearingCubes. Using dictionary to keep track of state of cubes
        returns none
        """
        if self.disCubeData.get((x,y)) == None or self.disCubeData[(x,y)] < 1:
            self.makeCube(x,y,tile_rects,18,color,True,dis_rects)
        col_List = rectTest(user.player_rect,dis_rects,True)


        if self.pause == False:
            for tile in col_List:
                defaultX = (tile.x/18)
                defaultY = (tile.y/18)
                if (defaultX,defaultY) not in self.disCubeData:
                    self.disCubeData[(defaultX,defaultY)] = 0
                if self.disCubeData[(defaultX,defaultY)] < 1: #1 secs
                    self.disCubeData[(defaultX,defaultY)] += 3/600





    def horiCube(self,x,y,color,tile_rects,hor_rects,user):
        """
        parameters: int,int,tuple,list,list,object
        creates and blits horizontal moving cubes onto the screen. keeps track of movement through dictionary database
        returns none
        """
        if y not in self.horiCubeDatabase:
            #speed for horCubes is dependent on the number of horcubes in a single y axis, due to last code line on funct
            self.horiCubeDatabase[y] = {"speed": -0.0125 * choice([1,-1]),"displacement": 0} #includes all cubes with the y value. Not to be mistaken for an individual tile



        if abs(self.horiCubeDatabase[y]["displacement"]) >= abs(self.horiCubeDatabase[y]["speed"] * 60 * 10): #2. sec?
            self.horiCubeDatabase[y]["speed"] = -self.horiCubeDatabase[y]["speed"]  #changes direction

        if self.colRect.x <= 0:
            self.horiCubeDatabase[y]["speed"] = -self.horiCubeDatabase[y]["speed"]



        self.makeCube(x - self.horiCubeDatabase[y]["displacement"] ,y,tile_rects,18,color,True,hor_rects)

        col_list = rectTest(user.player_rect,hor_rects,True)
        for tile in col_list:


            #no exact value because pg rect x & y values only allow int params
            self.turns += 0.115
            if self.turns >= 1:
                #user.player_rect.x  -= abs(self.horiCubeDatabase[y]["speed"]) /self.horiCubeDatabase[y]["speed"]
                user.horiDiff -= abs(self.horiCubeDatabase[y]["speed"]) /self.horiCubeDatabase[y]["speed"]
                self.turns -= 1

                # player movement is being reset so dito


        #the more hor cubes in a single y axis, the faster it becomes
        if self.pause == False:
            self.horiCubeDatabase[y]["displacement"] += self.horiCubeDatabase[y]["speed"]


    def portal(self,x,y):
        """
        parameters: int,int
        blits ship part onto the screen
        returns ship rect
        """
        colPortal = pg.Rect(x*18,y*18,33,48)
        portalIMG = self.ship_parts[int(self.state[-1])]
        self.display.blit(portalIMG,(colPortal.x - self.difference[0], colPortal.y - self.difference[1]))
        return colPortal
