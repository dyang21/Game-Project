
#music made by (youtuber)

from os.path import join
import pygame as pg
pg.init()
pg.mixer.init()
#sound(0gg or wav) and music(mp3). pygame has terrible mp3 support
#jump_sound = pygame.mixer.music.load("Music\in_motion\jump.mp3")
bg_Sound = pg.mixer.music.load(join('Music','Cyber','Double_the_Bits.mp3'))
pg.mixer.music.set_volume(0.9)
#0 once, 5 six times music plays, -1 loops forever
jumpSound = pg.mixer.Sound(join("Music","in_motion","sfx_shieldUp.ogg")) #some files unsupported
fallSound = pg.mixer.Sound(join("Music","sfx_lose.ogg"))
stageComplete = pg.mixer.Sound(join("Music","sfx_complete.ogg"))

#pg.mixer.music.play(-1)
