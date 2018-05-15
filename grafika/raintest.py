#!/usr/bin/python3

from random import randint , choice
from rain import *
try:
    import pygame
except ImportError:
    print("please install pygame module with 'pip install pygame'")

#colors
#colors are in rgb (red , green , blue) format
gloomywhite = (220 , 220 , 220 )
white = (255 , 255 , 255)
un = (230, 230, 250)
purple = ( 138, 43, 226 )
blue = ( 0 , 0 , 230 )
rainblue = (36, 113, 163 )
clock = pygame.time.Clock()
#

pygame.init()
gamedisplay = pygame.display.set_mode((900,600))
pygame.display.set_caption('PurpleRain')
pygame.display.update()

gameexit = False
drops = []
widths = [i for i in range(1,5)]
heights = [i for i in range(15,40,4)]
gravities = [ i for i in range(2,20,4)]
size = list(zip(widths , heights,gravities))

#making the rain drops
for i in range(500):
    x = randint(10,890)
    y = -1*randint(300 , 1500)
    width , height , g = choice(size)
    raindrop = Drop(gamedisplay , rainblue ,x,y,width , height,g)
    drops.append(raindrop)

#main loop
while not gameexit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameexit=True

    gamedisplay.fill(white)

    for d in drops:
        d.fall()
    pygame.display.update()
    clock.tick(70)

pygame.display.quit()
quit()
