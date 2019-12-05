
from os.path import join
from os.path import dirname

import sys
import json

#Third Party Imports.
import pygame as pg

#Local Imports
import gamescreens
import player_char #all things related to char aside from animations
win = gamescreens.window() #an require set mode to scale
user = player_char.player()
import animations as an
import collision as col
import music
import UI as ui






def playerNumber(data1):
    user = "Player " + str(len(data1) + 1)
    return user


        

def pauseMenu():
    pg.draw.rect(win.display,(255,255,255),(100,30,win.display.get_width() -200 ,win.display.get_height()- 60))
        #def singleText(self,fontsize,message,x,y,bold = True, color = (0,0,0),#underline = False):
    
    win.singleText(12,"Press ESC to Resume",105,140)
        
    ui.retryButton.drawButton(win.display)
    ui.pauseMenuQuit.drawButton(win.display)
    
def victoryScreen():
    win.state = "VictoryScreen"
    with open("high_scores.json") as f1:
        data1 = json.load(f1)
    
    data1.update({str(playerNumber(data1)):float((f" {win.time:.2f}"))})   
    

    save = data1.copy() # now the scores are saved into the win object
    
    
    
    win.scores = save #list
    
    with open("high_scores.json", "w") as f2:
        json.dump(data1,f2)
    
    while win.state == "VictoryScreen":
        
        win.display.fill(((0,0,0)))
        win.display.blit(win.gameBG_img,(0,0)) #change
        
        win.singleText(33,"You Win!",105,10,bold = True, color = (0,0,0),underline = True) #title
        
        win.singleText(22,"Your score: " + f" {win.time:.2f}",32,75,bold = True, color = (0,0,0)) #title
        
        ui.retryVic.drawButton(win.display)
        ui.scoreVic.drawButton(win.display)
        ui.quitVic.drawButton(win.display)
        
        mousePos = pg.mouse.get_pos()
        scaleMousePos = [i * 0.63  for i in (mousePos)]
        for event in pg.event.get(): # event loop

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type == pg.MOUSEBUTTONDOWN:

                if ui.retryVic.overButton(scaleMousePos): 
                    win.state = "gameMap0"
                    gameLoop()
                    
                if ui.scoreVic.overButton(scaleMousePos): 
                    highScorePage()
                    
                elif ui.quitVic.overButton(scaleMousePos): 
                    pg.quit()
                    sys.exit()
            
        win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
        pg.display.flip()
    

    
    
        
        
        
        
        
        
        
        
        
def introLoop():
    win.state = "intro"
    introState = "summary"
    
    while win.state == "intro":
        
        win.display.fill(((255,255,255)))
        win.display.blit(win.gameBG_img,(0,0))
        
        if introState == "summary":    
            message1 = "Oh no! Your spaceship has just crashed\non an unknown planet. The impact has\nbroken your ship into pieces (still in\nmiraculously good condition) and\nscattered it through the planet. It's\nnow up to you to retrieve the parts so\nyou can rebuild your ship and blast off\ninto space again!"
            
            win.paragraph(message1,13,3,50)

            win.singleText(20, "Introduction",118,16,False,(0,0,0), True)
            
        
        elif introState == "instructions":
            win.singleText(20, "Instructions",118,16,False,(0,0,0), True)
            message2 = "Use arrow keys to move \nTap up arrow quickly to double jump\nFalling off the map would result in\na substraction in lives\nIf you have no lives, you lose\nThe time it takes to complete the is\nthe score metric.\nPress escape for the menu "
            
            win.paragraph(message2,14,3,50)
            
        win.singleText(14, "Click anywhere to continue",55,263,False,(0,0,0))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if introState == "summary":
                    introState = "instructions"
                elif introState == "instructions":
                    gameLoop()
        
        
                
        win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
        pg.display.flip()






#drawText(self,fontsize,message,x,y,bold = True, color = (0,0,0)):

def menuLoop():
    win.state = "menu"
    while win.state == "menu":
        win.display.fill(((0,0,0)))
        win.display.blit(win.menuBG_img,(0,0))
        
        
        ui.playButton.drawButton(win.display)
        ui.quitButton.drawButton(win.display)
        ui.scoreButton.drawButton(win.display)
        
        
        win.singleText(33,"Lost in Space",20,30,bold = True, color = (0,0,0)) #title
        
        mousePos = pg.mouse.get_pos()
        scaleMousePos = [i * 0.63  for i in (mousePos)]
        
    
        for event in pg.event.get(): # event loop

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:

                if ui.playButton.overButton(scaleMousePos): 
                    win.state = "intro"
                    introLoop()
                    
                if ui.scoreButton.overButton(scaleMousePos): 
                    highScorePage()
                
                
                if ui.quitButton.overButton(scaleMousePos): 
                    pg.quit()
                    sys.exit()
                
        win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
        pg.display.flip()


def highScorePage():
    win.state = "high score"
    highScore = sorted((win.scores).values())[:5]
    result = {}
    for i in highScore:
        for k,v in (win.scores).items():
            if i == v:
                result[k] = v

    
    while win.state == "high score":
        win.display.fill(((0,0,0)))
        win.display.blit(win.gameBG_img,(0,0)) #change
        win.singleText(20, "High Scores",118,16,False,(0,0,0), True)
        
        y = 50
        for k,v in result.items():
            win.singleText(16, str(k) + " : " + str(v) ,40,y,False,(0,0,0))
            y += 30
        
        ui.backButton.drawButton(win.display)
        
        mousePos = pg.mouse.get_pos()
        scaleMousePos = [i * 0.63  for i in (mousePos)]

        for event in pg.event.get(): # event loop

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if ui.backButton.overButton(scaleMousePos): 
                    menuLoop()

            
            
        win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
        pg.display.flip()
        
def gameOver():
    win.state = "Game Over"
    while win.state == "Game Over":
        win.display.fill(((0,0,0)))
        win.display.blit(win.menuBG_img,(0,0))
        
        mousePos = pg.mouse.get_pos()
        scaleMousePos = [i * 0.63  for i in (mousePos)]
        #singleText(self,fontsize,message,x,y,bold = True, color = (0,0,0),underline = False):
        
        win.singleText(27, "Game Over",95,100)
        
        ui.backButton.drawButton(win.display)
    
        
        for event in pg.event.get(): # event loop

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:

                if ui.backButton.overButton(scaleMousePos): 
                    menuLoop()
                 
        win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
        pg.display.flip()



def gameLoop():
    pg.mixer.music.play(-1)
    user.health = 5
    win.state = "GameMap0"
    win.stage_num = 0
    win.time = 0
    user.spawned = False
    while win.state[:4] == "Game": # game loop


        win.display.fill(((0,0,0)))
        win.display.blit(win.gameBG_img,(0,0))

        try:
            user.right_border = (len(win.maps_database[win.state][0]) - 1) * 18 # 4sided. first line cannot be empty spaces
        except:
            victoryScreen()
        
        user.bottom_border = (len(win.maps_database[win.state])+3.7) * 18

        #gives how much player moved, difference of how much player moved and around half screen length
        win.difference[0] += (user.player_rect.x - win.difference[0] -204  )/10 #164
        win.difference[1] += (user.player_rect.y -win.difference[1] -135)/10#110
        #move all the objects by thhe resize value

        win.difference[0] = int(win.difference[0])
        win.difference[1] = int(win.difference[1]) #helps prevents player shaking on vert platform


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
        tile_rects,vert_rects, hor_rects, dis_rects = [], [], [], [] #all the tiles are here

        #collison test rect tiles
        y = 0
        for layer in win.maps_database[win.state]:
            #sets to x to go from left to right
            #key: 2 for floor,3 for spawnpoint,4 for portal,5 for key, 6 for gate, 7 for enemies, 8 for moving platforms
            x = 0
            for tileIndex in range(len(layer)-1):

                if layer[tileIndex] == '1':

                    win.makeCube(x,y,tile_rects,18,(21,121,143),True)

                elif layer[tileIndex] == '2' and user.spawned == False:#spawn location

                    user.player_rect.x,user.player_rect.y = x*18 ,y*18
                    user.spawned = True

                elif layer[tileIndex] == '3': #Stage Finish Line

                    colPortal = win.portal(x,y)

                elif layer[tileIndex] == "4": #vert moving & disappearing blocks

                    win.makeVerticalMovingCubes(x,y,user,tile_rects,(150, 105, 21),vert_rects)

                elif layer[tileIndex] == "5": # horizontal mov block
                    win.horiCube(x,y,(113, 45, 181),tile_rects,hor_rects,user)
                elif layer[tileIndex] == "6": # static disappearing tile
                    win.disappearingCubes(x,y,user,tile_rects,(107, 130, 124),dis_rects)



                x += 1
            y += 1

        #user.player_rect.x += 1
        user.player_movement = [0,0]
        user.player_movement[0] += user.horiDiff

        if user.pause == False:
            user.move()
        user.boundaries()
        user.update() #animation assigned to movement

        #check if it has collision with bottom tile

        win.display.blit(pg.transform.flip(player_img,user.player_flip,False),((user.player_rect.x - win.difference[0]), (user.player_rect.y - 18- win.difference[1])))

        if user.player_rect.colliderect(colPortal) and user.spawned == True:
            music.stageComplete.play()
            win.stage_num += 1
            win.state = win.state[:-1] + str(win.stage_num)



            user.spawned = False

        if user.spawned == False:
            win.vertCubeData.clear()
            win.vertCubeData.clear()
            win.disCubeData.clear()

        if user.health == 0:
            gameOver()


        # preciseRect = pg.Rect(user.player_rect.x - win.difference[0],user.player_rect.y + 10 - win.difference[1],42,user.player_rect.height)
        #pg.draw.rect(win.display,(0,0,0),preciseRect)

        #important in that it moves the collision rects and player

        collisions = col.col(user.player_rect, user.player_movement, tile_rects) #rect and dict. moves the player rect
        #put make that true for collisions up also
        if collisions["top"] == True:
            user.vertical_momenuetum = 0
            user.vertical_momentum = -user.vertical_momentum
        if collisions['bottom'] == True:
            user.air_timer = 0
            #resets vm

        else:
            user.air_timer += 1

        #print(user.player_rect.y)
        if win.state == "GameMap8":
            pass
            #self.victoryLoop()
            
        mousePos = pg.mouse.get_pos()
        scaleMousePos = [i * 0.63  for i in (mousePos)]

        for event in pg.event.get(): # event loop
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
                
            if event.type == pg.MOUSEBUTTONDOWN and win.pause == True:
                if ui.retryButton.overButton(scaleMousePos):
                    win.state = "GameMap0"
                    user.pause,user.spawned,win.pause,win.time = 0,0,0,0
                    user.health = 5
                    pg.mixer.music.play(-1)
                    
                elif ui.pauseMenuQuit.overButton(scaleMousePos):
                    pg.quit()
                    sys.exit()
                    

                    

                
                
            if event.type == pg.KEYDOWN:
                if user.pause == False:
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
                if event.key == pg.K_1:
                    pg.mixer.music.play(-1)
                if event.key == pg.K_2:
                    pg.mixer.music.fadeout(1*1000) #milliseconds

                if event.key == pg.K_3:
                    if win.pause == True:
                        win.pause, user.pause = False, False
                        pg.mixer.music.play(-1)
                    else:    
                        user.pause = True
                        #user.vertical_momentum = 0
                        win.pause = True
                
                
                

                    


                


            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    user.moving_right = False
                elif event.key == pg.K_LEFT:
                    user.moving_left = False
        
        
        if win.pause == True:
            pauseMenu()
            pg.mixer.music.fadeout(1*300)

        win.lifeCount(user.health)
        win.showTimer(win.time)

        win.screen.blit(pg.transform.scale(win.display, win.WINDOW_SIZE),(0,0))
        pg.display.flip()
        win.clock.tick(60) # fps
        
menuLoop()