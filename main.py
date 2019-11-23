#Made by Donald Yang


    #jumping blocks. rect
    #fall off stage. reach y boundary. -1 life. go to spawn xy


#standard libary
from os.path import join
import sys

#Third Party Imports.
import pygame as pg

#Local Imports
import gamescreen
import player_char #all things related to char aside from animations
win = gamescreen.window() #an require set mode to scale
user = player_char.player()      
import animations as an
import collision as col
import music


pg.init()
    
         
        
    

#all_sprites = pygame.sprite.Group((user(),))
#2 is block. 3 is spawn. 4 is gate. rest TBD

while True: # game loop
    win.display.fill(((0,0,0))) 
    win.display.blit(win.background_img,(0,0))
    
    user.right_border = (len(win.maps_database[win.state][0])) * 18 # 4sided. first line cannot be empty spaces
    user.bottom_border = (len(win.maps_database[win.state])+3.7) * 18
   
    #gives how much player moved, difference of how much player moved and around half screen length
    win.difference[0] += (user.player_rect.x - win.difference[0] -204  )/18 #164
    win.difference[1] += (user.player_rect.y -win.difference[1] -141)/18 #110
    #move all the objects by thhe resize value

    win.difference[1] = int(win.difference[1]) #helps prevents player shaking on moving platform


    win.bgParallaxScroll(win.difference)
    
    if win.difference[0] < 0:
        win.difference[0] = 0
    elif win.difference[0] > (user.right_border) - win.display.get_width():
        win.difference[0] = (user.right_border) - win.display.get_width() # + block.width because images blit from top left. subtract by win.display.width for same reason.
  

    
        

    
    #loops through animation action frames
    try:
        player_image_id = an.animation_database[user.player_action][user.player_frame]
        player_img = an.animation_frames[player_image_id]
    except:
        user.player_frame = 0
    
    #flip(image,over y?,over x?) so basically the transform part of the img param
    

    
    tile_rects = []      
    #collison test rect tiles
    y = 0
    for layer in win.maps_database[win.state]:
        #sets to x to go from left to right
        #key: 2 for floor,3 for spawnpoint,4 for portal,5 for key, 6 for gate, 7 for enemies, 8 for moving platforms
        x = 0
        for tileIndex in range(len(layer)-1):
            if layer[tileIndex] == '2':
                
                win.makeCube(x,y,tile_rects,18,(21,121,143),True)
                             
            elif layer[tileIndex] == '3' and user.spawned == False:#spawn location
                 
                user.player_rect.x,user.player_rect.y = x*18 ,y*18
                user.spawned = True
                
            elif layer[tileIndex] == '4': #Stage Finish Line
                
                colPortal = pg.Rect(x*18,y*18,33,48)
                portalIMG = win.ship_parts[int(win.state[-1])]
                win.display.blit(portalIMG,(colPortal.x - win.difference[0], colPortal.y - win.difference[1]))
                
            elif layer[tileIndex] == "5": #moving blocks
                
                 win.makeVerticalMovingCubes(x,y,user,tile_rects,(21,121,143))
                 
                #print(user.vertical_momentum)
            x += 1
        y += 1
    
    user.move()  
    user.boundaries()
    user.update() #animation assigned to movement
    
    
    win.display.blit(pg.transform.flip(player_img,user.player_flip,False),((user.player_rect.x - win.difference[0]), (user.player_rect.y - 18- win.difference[1])))
    
    if user.player_rect.colliderect(colPortal) and user.spawned == True:
        music.stageComplete.play()
        win.stage_num += 1
        win.state = win.state[:-1] + str(win.stage_num)
        user.spawned = False
    
    

    preciseRect = pg.Rect(user.player_rect.x - win.difference[0],user.player_rect.y + 10 - win.difference[1],42,user.player_rect.height)
    pg.draw.rect(win.display,(0,0,0),preciseRect)
        
    #important in that it moves the collision rects and player
    
    collisions = col.col(user.player_rect, user.player_movement, tile_rects) #rect and dict. moves the player rect
    #put make that true for collisions up also
    if collisions['bottom'] == True:
        user.air_timer = 0
        #resets vm
        user.vertical_momentum = 0
    elif collisions["top"] == True:
        user.vertical_momentum = 0
    else:
        user.air_timer += 1
        
    #print(user.player_rect.y)
    

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
                    music.jumpSound.play()
                    user.enableDoubleJump = False
                    user.vertical_momentum = -5.6
                elif user.air_timer < 20:
                    music.jumpSound.play()
                    user.vertical_momentum = -5
                    user.enableDoubleJump = True
                    #jump_sound.play(1)
            elif event.key == pg.K_1:
                pg.mixer.music.fadeout(1*1000) #milliseconds
            elif event.key == pg.K_2:
                pg.mixer.music.play(-1)

                                  
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                user.moving_right = False
            elif event.key == pg.K_LEFT:
                user.moving_left = False
                
    
    win.lifeCount(user.health)
    win.showTimer(win.time)

    win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
    pg.display.flip() 
    win.clock.tick(60) # fps
   
