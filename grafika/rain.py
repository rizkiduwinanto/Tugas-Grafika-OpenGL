import pygame
import random
from OpenGL.GL import *
from random import randint , choice

class Drop:
    def __init__(self, r, g, b, x, y, z, width, height, gravity):
        self.r = r
        self.g = g
        self.b = b
        self.x = x
        self.y = y
        self.z = z
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
        # pygame.draw.rect(self.surface , self.color ,[ self.x , self.y , self.z, self.width , self.height ])
        glColor3f(self.r, self.g, self.b)
        glBegin(GL_LINES)
        glVertex3f(self.x, self.y, self.z)
        glVertex3f(self.x, self.y+0.5, self.z)
        glEnd()
