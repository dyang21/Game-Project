#Made by Donald Yang


    #jumping blocks. rect
    #different stages.
    #make sure your dir is in the folder for this.
    #fall off stage. reach y boundary. -1 life. go to spawn xy


#standard libary
from os.path import join
import sys

#Third Party Imports.
import pygame as pg

#Local Imports
import gamescreen
import player_char #all things related to char aside from animations
import animations as an
import collision as col
import music


pg.init() 

        
win = gamescreen.window()
user = player_char.player()




#all_sprites = pygame.sprite.Group((user(),))
#2 is block. 3 is spawn. 4 is gate. rest TBD


while True: # game loop
    win.display.fill(((0,0,0))) # stops
    win.display.blit(win.background_img,(0,0))
    
    win.right_border = (len(win.maps_database[win.state][0])-1) * 16#4sided. first line cannot be empty spaces
   
    #gives how much player moved, difference of how much player moved and around half screen length
    win.float_difference[0] += (user.player_rect.x - win.float_difference[0] -164 )/20
    win.float_difference[1] += (user.player_rect.y -win.float_difference[1] -110)/20
    #move all the objects by the resize value
    
    win.bgParallaxScroll(win.float_difference)
    
    if win.float_difference[0] < 0:
        win.float_difference[0] = 0
    elif win.float_difference[0] > (win.right_border + 16) - win.display.get_width():
        win.float_difference[0] = (win.right_border+16) - win.display.get_width() # + block.width because images blit from top left. subtract by win.display.width for same reason.
    #if user.player_rect.x == win.right_border -16:     
        #user.player_rect.x = win.right_border -16
    
          
    tile_rects = [] #collison test rect tiles
    y = 0
    for layer in win.maps_database[win.state]:
        #sets to x to go from left to right
        #key: 2 for floor,3 for spawnpoint,4 for portal,5 for key, 6 for gate, 7 for enemies, 8 for moving platforms
        x = 0
        for tile in layer:
            if tile == '2':
                #makes blocks for collision. move camera left. tiles move right
                colRect = pg.Rect(x*16,y*16,16,16)
                tile_rects.append(colRect)
                displayRect = pg.Rect(colRect.x - win.float_difference[0],
                colRect.y - win.float_difference[1],16,16)
                pg.draw.rect(win.display,(21,121,143),displayRect)
            elif tile == '3' and user.spawned == False:#spawn location 
                user.player_rect.x,user.player_rect.y = x*16 ,y*16
                user.spawned = True
            elif tile == '4': #Stage Finish Line
                colPortal = pg.Rect(x*16,y*16,33,48)
                portalIMG = win.ship_parts[int(win.state[-1])]
                win.display.blit(portalIMG,(colPortal.x - win.float_difference[0], colPortal.y - win.float_difference[1]))               
            x += 1
        y += 1
    
    if user.player_rect.colliderect(colPortal) and user.spawned == True:
        win.stage_num += 1
        tile_rects.clear()
        win.state = win.state[:-1] + str(win.stage_num)
        user.spawned = False

    
    
    user.move()
    user.update()   
    

        
    #important in that it moves the collision rects and player
    user.player_rect, collisions = col.col(user.player_rect, user.player_movement, tile_rects,win.right_border)
    
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
    win.display.blit(pg.transform.flip(player_img,user.player_flip,False),(user.player_rect.x - win.float_difference[0], user.player_rect.y - win.float_difference[1]))
    

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

    win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
    pg.display.flip() 
    win.clock.tick(60) # fps
    
