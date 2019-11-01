from os.path import join 

import pygame

pygame.init()

#Gives images for each frame. action unspecified 
animation_frames = {}

#path to folder. image_duration is set ex[7,7]
def loadAnimation(path,image_duration):
    image_name = path.split('\\')[-1]
    #what images of the animations should it be showing for each frame
    frame_database = []
    n = 0
    for img in image_duration: # 7 == seven frame appended to the list
        image_id = image_name + "_" + str(n)
        image_location = path + "\\"  + image_id + ".png" 
        animation_image = pygame.image.load(image_location).convert()
        animation_image.set_colorkey((0,0,0))  
        #use online scaler for image. pygame smoothscale is terrible
        animation_frames[image_id] = animation_image.copy()
        for i in range(img):
            frame_database.append(image_id)
        n += 1
    return frame_database # == animation_database['action']

