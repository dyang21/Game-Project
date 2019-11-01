import pygame

class window():
    def __init__(self):
        self.WINDOW_SIZE = (600,400) # 300 200. ratio 3 by 2 is most common
        self.display = pygame.Surface((360,240)) # surface for rendering; scaled to window size at end
        self.clock = pygame.time.Clock() 
        self.bg_objects = [[0.20,[150,100,25,100]],[0.25,[100,50,100,25]],[0.4,[50,150,50,75]],[0.5,[10,75,70,100]]] 
        #lag small > high,(rect param)
        self.float_resize = [0,0] # x and y. based on how far camera moves.


def loadMap(path):
    text_file = open(path,"r")
    data = (text_file.read()).split('\n')
    text_file.close
    organized_map = []
    for line in data:
        organized_map.append(list(line))
    return organized_map
    
