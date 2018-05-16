from particle import Particle
from random import uniform
from OpenGL.GL import *

class ParticleSystem:
    NUMBER_OF_PARTICLES = 1000

    def __init__(self, x_coord, y_coord):
        self.particles = self._init_particles(x_coord, y_coord)
        self.active = True

    def _init_particles(self, x_coord, y_coord):
        particles = [Particle() for i in range(self.NUMBER_OF_PARTICLES)]
        for particle in particles:
            particle.active = True
            particle.life = 1.0
            particle.ageing = 0
            particle.red = 36.0
            particle.green = 113.0
            particle.blue = 163.0
            particle.x = x_coord
            particle.y = y_coord
            particle.z = 0.0
            particle.xv = uniform(-0.08, 0.08)
            particle.yv = uniform(-0.08, 0.08)
            particle.zv = 0.2
        return particles

    def rain(self):
        has_active_particles = False
        for particle in self.particles:
            if particle.active:
                has_active_particles = True
                x = particle.x
                y = particle.y
                z = particle.z
                glPushMatrix()
                glTranslatef(0.0,0.0,-9.0)
                glPushAttrib(GL_CURRENT_BIT)
                glColor3f(particle.red, particle.green, particle.blue)
                VERTEX_POS = 0.02
                glBegin(GL_TRIANGLE_STRIP)

                glEnable(GL_BLEND);
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

                glVertex3f(x+VERTEX_POS, y+VERTEX_POS, z)
                glVertex3f(x-VERTEX_POS, y+VERTEX_POS, z)
                glVertex3f(x+VERTEX_POS, y-VERTEX_POS, z)
                glVertex3f(x-VERTEX_POS, y-VERTEX_POS, z)

                glEnd()

                particle.x += particle.xv
                particle.y += particle.yv
                particle.z += particle.zv
                # particle.life -= particle.ageing

                if particle.life <= 0.0:
                    particle.active = False

                glPopAttrib()
                glPopMatrix()

            if not has_active_particles:
                self.active = False
