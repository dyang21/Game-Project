#TBI: fall damage based on vertical momentum
    #jumping blocks. rect
    #different stages.
    #make sure your dir is in the folder for this.

#standard libary
from os.path import join
import sys

#Third Party Imports.
import pygame as pg

#Local Imports
import gamescreen
import player_char #all things related to char aside from animations
import animations as an
import collision
import music


pg.init() # initiates pygame

pg.display.set_caption('Lost Goblin')
        
win = gamescreen.window()
user = player_char.player()

screen = pg.display.set_mode(win.WINDOW_SIZE) # initiate the window

game_map = gamescreen.loadMap('GameMap.txt')

dirt_img = pg.image.load(join('blocks','dirt.png'))
grass_img = pg.image.load(join('blocks','grass.png'))
bullet_img = pg.transform.scale((pg.image.load("star_gold.png")),(10,10)) 


# pygame.Rect(0,25,300,65) x,y, width, height
#screen.blit(pygame.transform.scale(win.display, win.WINDOW_SIZE),(0,0))

# win.display.blit(bullet_img,(user.player_rect.x  - resize[0] + (player_img.get_width())/2, user.player_rect.y - resize[1] + (player_img.get_height())/2))

#all_sprites = pygame.sprite.Group((user(),))

Game_State = "Game"

while True: # game loop
    win.display.fill((146,244,255)) # clear screen by filling it with blue
       
    #gives how much player moved, difference of how much player moved and around half screen length
    win.float_resize[0] += (user.player_rect.x - win.float_resize[0] - 153)/18
    win.float_resize[1] += (user.player_rect.y - win.float_resize[1] - 105)/18
    #making it int because blit does not take decimals well
    resize = win.float_resize[:]
    resize[0] = int(resize[0])
    resize[1] = int(resize[1])
    
    
    
    #(surface,rgb,rect(x,y,width,height))
    pg.draw.rect(win.display,(100, 192, 207),pg.Rect(0,25,300,65)) #background
    #Rect(x,y,width,height). mutiple rs difference for lag effect. greatest to least. change location. not size
    for object in win.bg_objects:
        obj_rect = pg.Rect(object[1][0]-resize[0]*object[0],object[1][1]-resize[1]*object[0],object[1][2],object[1][3])
        if object[0] == 0.5:
            pg.draw.rect(win.display,(138, 140, 181),obj_rect)
        else:
            pg.draw.rect(win.display,(0, 247, 255),obj_rect)
        
    
    tile_rects = [] #collison test rect tiles
    y = 0
    for layer in game_map:
        #sets to x to go from left to right
        #16 x 16 is the measurements of the dirt and grass images.
        x = 0
        for tile in layer:
            if tile == '1':
                #2nd parameter is location remember. 
                win.display.blit(dirt_img,(x*16 - resize[0],y*16 - resize[1]))
            if tile == '2':
                win.display.blit(grass_img,(x*16 - resize[0],y*16 - resize[1]))
            if tile != '0':
                #makes blocks for collision. params(location,size(keep it at resolution)) 
                tile_rects.append(pg.Rect(x*16,y*16,16,16))
            x += 1
        #changes layer
        y += 1


    #speed can be adjusted here; used for move
    player_movement = [0,0]
    if user.moving_right == True:
        player_movement[0] += 2
    if user.moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += user.vertical_momentum
    #gravity.
    user.vertical_momentum += 0.2
    #max height of jump
    if user.vertical_momentum > 3:
        user.vertical_momentum = 3 
    
    #control image switch
    if player_movement[0] > 0:
        user.player_action, user.player_frame = player_char.change_action(user.player_action, user.player_frame,"in_motion")
        user.player_flip = False
        user.flip2 = True
    if player_movement[0] < 0:
        user.player_action, user.player_frame = player_char.change_action(user.player_action, user.player_frame,"in_motion")
        user.player_flip = True
        user.flip2 = False
    if player_movement[0] == 0:
        user.player_action, user.player_frame = player_char.change_action(user.player_action, user.player_frame,"idle")
        user.player_flip = user.flip2
        

        
    #might be hard to see but collisions is being created here, important in that it moves the collision rects and player
    user.player_rect, collisions = collision.move(user.player_rect, player_movement, tile_rects)
    
    #put make that true for collisions up also
    if collisions['bottom'] == True:
        user.air_timer = 0
        #resets vm
        user.vertical_momentum = 0
    elif collisions["top"] == True:
        user.vertical_momentum = 0
    else:
        user.air_timer += 1
        
    user.player_frame += 1 #keeps track of frames
    
    #loops through animation action frames
    if user.player_frame >= len(an.animation_database[user.player_action]):
        user.player_frame = 0
        
    player_image_id = an.animation_database[user.player_action][user.player_frame]
    #animation frames dict containes each id and their image object
    player_img = an.animation_frames[player_image_id]
    
    #flip(image,over y?,over x?) so basically the transform part of the img param
    win.display.blit(pg.transform.flip(player_img,user.player_flip,False),(user.player_rect.x - resize[0], user.player_rect.y - resize[1]))
    

    for event in pg.event.get(): # event loop
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                user.moving_right = True
            elif event.key == pg.K_LEFT:
                user.moving_left = True
            elif event.key == pg.K_UP:
                #only able to jump after 20 counts
                if user.air_timer < 20 and user.enableDoubleJump == True:
                    user.enableDoubleJump = False
                    user.vertical_momentum = -5.6
                elif user.air_timer < 20:
                    #remember. negative y value means going up
                    user.vertical_momentum = -5
                    user.enableDoubleJump = True
                    #jump_sound.play(1)
            elif event.key == pg.K_1:
                pg.mixer.music.fadeout(1*1000) #milliseconds
            elif event.key == pg.K_2:
                pg.mixer.music.play(-1)
            elif event.key == pg.K_a:
                newBullet = True
                                  
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                user.moving_right = False
            elif event.key == pg.K_LEFT:
                user.moving_left = False
    
    
    #scales display to window size at top leftscreen.blit 
    #new_image = pg.transform.scale(IMAGE, (50, 30)) params are new width and height
    screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
    pg.display.flip() # flip
    win.clock.tick(60) # frames per sec
