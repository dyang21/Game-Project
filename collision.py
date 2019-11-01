#takes rect object and list of other rects. returns which tile it collides with
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#char obj,how much being moved, objects to be collided with
def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    #moving the rect along movement variable; has to move one axis at a time because of collision test resets
    rect.x += movement[0]
    #test for collisions 
    hit_list = collision_test(rect,tiles)
    #enables stopping at collisions for left and right. 
    for tile in hit_list:
        #move left or right
        if movement[0] > 0:
            #the right border of the rect does not collide with the left border of the tile.
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    #seperated this because the hit_list is reassigned
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    #return collision types and location of rect obj
    return rect, collision_types
