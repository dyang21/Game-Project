#dy

#takes rect object and list of other rects. returns which tile it collides with
def rectTest(player_rect,tiles):
    col_List = []
    for tile in tiles:
        if player_rect.colliderect(tile):
            col_List.append(tile)
    return col_List

#char obj,how much being moved, objects to be collided with
def col(player_rect,movement,tiles,right_border): #(rect,[ints,],[rects,])
    col_types = {'top':False,'bottom':False,'right':False,'left':False}
    player_rect.y += movement[1]
    hit_list = rectTest(player_rect,tiles)
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
    if player_rect.x >= right_border:
        player_rect.x = right_border
    elif player_rect.x <= 0 :
        player_rect.x = 0
    player_rect.x += movement[0]
    hit_list = rectTest(player_rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            #prevents border collision 
            player_rect.right = tile.left
            col_types['right'] = True
        elif movement[0] < 0:
            player_rect.left = tile.right
            col_types['left'] = True
    #return collision types and location of rect obj
    return player_rect, col_types
