

def occurrences(string):
    charCount = {}
    alreadycounted = []
    newstring = ""
    for char in string:
        if char.isupper:
            newstring += char.lower()
        else:
            newstring += char  
    for lowerchar in newstring:
        if lowerchar not in alreadycounted:
            charCount[lowerchar] = newstring.count(lowerchar)
            alreadycounted.append(lowerchar)
    return charCount, newstring

def main():
    string = "Jeff Bezo "
    charCount, newstring = occurrences(string.strip())
    for i in charCount:
        print(charCount[i])
    mostInstances = max(charCount, key = charCount.get)
    a = newstring.replace(mostInstances,"&",-1)
    print(chr(ord("sadasdas")))

class Projectile(pg.sprite.Sprite):
    def __init__(self,user_moving_left,x,y,flip): 
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        if user_moving_left == True: #
            self.image = pg.transform(self.image,True, False)
    def update(self):
        if self.direction == "left":
            self.rect.x -= 10
        else:
            self.rect.x += 10