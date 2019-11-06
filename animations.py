from os.path import join 

import pygame

#pygame.init()

#Gives images for each frame. action unspecified 
animation_frames = {}

#path to folder. image_duration is set ex[7,7]; 7 == seven frame appended to the list
def loadAnimation(path,image_duration): #assumes the images in the folder are in NAME# format
    image_name = path.split('\\')[-1]
    #what images of the animations should it be showing for each frame
    frame_database = []
    n = 0
    for img in image_duration: 
        image_id = image_name + "_" + str(n)
        image_location = path + "\\"  + image_id + ".png" 
        animation_image = pygame.image.load(image_location)
        animation_image.set_colorkey((0,0,0))  #img background transparency
        #try using other scalers to transform img bigger. pygame smoothscale is terrible
        animation_frames[image_id] = animation_image.copy()
        for i in range(img):
            frame_database.append(image_id)
        n += 1
    return frame_database # == animation_database['action']


#Gives sequence of images for every action.
animation_database = {}
#get frames to secs
animation_database['idle'] = loadAnimation(join('characters_pics','idle'),[160,160])    #160/60 or fps specified below to secs
animation_database["in_motion"] = loadAnimation(join('characters_pics','in_motion','walking'),[15,15,15,15,15])
