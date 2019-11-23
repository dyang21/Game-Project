#dy
from pygame import Rect


#takes rect object and list of other rects. returns which tile it collides with
def rectTest(player_rect,tiles,testVertRect): #side,displacement; divide it by the side and add it by the displacement
    col_List = []
    if testVertRect == False:
        for tile in tiles:
            if player_rect.colliderect(tile):
                col_List.append(tile)

                
    else:

        preciseRect = Rect(player_rect.x,player_rect.y + 2  ,42,player_rect.height)


        for tile in tiles:
            
            if preciseRect.colliderect(tile):

                print(1)
                
                col_List.append(tile) #second tile would be the time it has been stepped on, and to include Rect collision
                #player_rect.bottom = tile.top
                
    return col_List



#char obj,how much being moved, objects to be collided with
def col(player_rect,movement,tiles): #(rect,[ints,],[rects,])
    col_types = {'top':False,'bottom':False,'right':False,'left':False}
    player_rect.y += movement[1]
    hit_list = rectTest(player_rect,tiles,False)
    #enables stopping at collisions for left and right. 
    for tile in hit_list:
        #move left or right
        if movement[1] > 0:
            player_rect.bottom = tile.top
            col_types['bottom'] = True
        elif movement[1] < 0:
            player_rect.top = tile.bottom
            col_types['top'] = True
    #seperated because the collision list is reassigned
    player_rect.x += movement[0]
    hit_list = rectTest(player_rect,tiles,False)
    for tile in hit_list:
        if movement[0] > 0:
            #prevents border collision 
            player_rect.right = tile.left
            col_types['right'] = True

        elif movement[0] < 0:
            player_rect.left = tile.right
            col_types['left'] = True

    #return collision types and location of rect obj
    #print(col_types)
    return col_types
