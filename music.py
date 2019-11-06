from os.path import join
import pygame as pg
pg.init()
#sound(0gg or wav) and music(mp3). pygame has terrible mp3 support
#jump_sound = pygame.mixer.music.load("Music\in_motion\jump.mp3")
pg.mixer.music.load(join('Music','Cyber','Double_the_Bits.mp3'))
#0 once, 5 six times music plays, -1 loops forever
pg.mixer.music.play(-1)
