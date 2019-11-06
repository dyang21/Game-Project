#takes rect object and list of other rects. returns which tile it collides with
def collision_test(player_rect,tiles):
    hit_list = []
    for tile in tiles:
        if player_rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#char obj,how much being moved, objects to be collided with
def move(player_rect,movement,tiles): #(rect,[ints,],[rects,])
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    player_rect.y += movement[1]
    hit_list = collision_test(player_rect,tiles)
    #enables stopping at collisions for left and right. 
    for tile in hit_list:
        #move left or right
        if movement[1] > 0:
            player_rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            player_rect.top = tile.bottom
            collision_types['top'] = True
    #seperated this because the hit_list is reassigned
    player_rect.x += movement[0]
    hit_list = collision_test(player_rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            #prevents border collision 
            player_rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            player_rect.left = tile.right
            collision_types['left'] = True

    #return collision types and location of rect obj
    return player_rect, collision_types
