import pygame
from random import randint , choice
import time

class Drop:
    def __init__(self,surface , color , x, y , width , height ,gravity):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.time = 0
        self.g= gravity

    def fall(self):
        self.y =int( self.y + (self.g/2)*self.time**2 )
        if self.y > 700:
            self.y = -1*randint(300,1500)
            self.time = 0.03
        self.time += 0.01
        pygame.draw.rect(self.surface , self.color ,[ self.x , self.y , self.width , self.height ])
