import sys, pygame, time
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *
from random import uniform
from math import pi as PI

class Particle:

    # initialise
    def __init__(self):

        # active settings
        self.is_active = False
        self.life = 0.0
        self.ageing = 0.0

        # colour
        self.r = 0.0
        self.g = 0.0
        self.b = 0.0

        # coordinates
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        # velocity
        self.xv = 0.0
        self.yv = 0.0
        self.zv = 0.0

        # acceleration
        self.xa = 0.0
        self.ya = 0.0
        self.za = 0.0

class SmokeParticleSystem:

    # constants
    NUMBER_OF_PARTICLES = 500

    # initialise
    def __init__(self, x, y, z):
        self.active = True
        self.x = x
        self.y = y
        self.z = z
        self.particles = [Particle() for i in range(self.NUMBER_OF_PARTICLES)]
        for particle in self.particles:
          self.reset_particle(particle)

    def reset_particle(self, particle):
        particle.active = True
        particle.life = 1.0
        particle.ageing = uniform(0.01, 0.04)

        color = uniform(0.0, 0.3)
        particle.r = color
        particle.g = color
        particle.b = color

        particle.x = self.x
        particle.y = self.y + uniform(-0.05, 0.05)
        particle.z = self.z

        particle.xv = uniform(-0.02, 0.02)
        particle.yv = uniform(-0.02, 0.02)
        particle.zv = uniform(0.20, 0.40)

    def render(self):

      # for each particle
      for particle in self.particles:
        # get coordin * (1 - particle.life)ates of particle
        x = particle.x
        y = particle.y
        z = particle.z

        glPushAttrib(GL_CURRENT_BIT)

        # set colour of particle
        glColor4f(particle.r, particle.g, particle.b, particle.life)

        # draw particle
        VERTEX_POS = 0.025

        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x+VERTEX_POS, y+VERTEX_POS, z)
        glVertex3f(x-VERTEX_POS, y+VERTEX_POS, z)
        glVertex3f(x+VERTEX_POS, y-VERTEX_POS, z)
        glVertex3f(x-VERTEX_POS, y-VERTEX_POS, z)
        glEnd()

        # update particle with velocity
        particle.x += particle.xv
        particle.y += particle.yv
        particle.z += particle.zv

        # update particle's life
        particle.life -= particle.ageing

        if particle.life <= 0.0:
          self.reset_particle(particle)

        glPopAttrib()


class RainParticleSystem:

    # constants
    NUMBER_OF_PARTICLES = 500

    # initialise
    def __init__(self, x, y, z, offset):
        self.x = x
        self.y = y
        self.z = z
        self.offset = offset
        self.particles = [Particle() for i in range(self.NUMBER_OF_PARTICLES)]
        for particle in self.particles:
          self.reset_particle(particle)

    def reset_particle(self, particle):
        particle.life = 1.0
        particle.ageing = uniform(0.01, 0.04)

        particle.r = 0
        particle.g = 0
        particle.b = uniform(0.2, 0.5)

        particle.x = self.x + uniform(-self.offset, self.offset)
        particle.y = self.y + self.offset + uniform(-0.005, 0.005)
        particle.z = self.z + uniform(-self.offset, self.offset)

        particle.xv = 0
        particle.yv = 0
        particle.zv = 0

        particle.xa = 0
        particle.ya = -0.04
        particle.za = 0

    def render(self):

      # for each particle
      for particle in self.particles:
        # get coordinates of particle
        x = particle.x
        y = particle.y
        z = particle.z

        glPushAttrib(GL_CURRENT_BIT)

        # set colour of particle
        glColor4f(particle.r, particle.g, particle.b, 0.5)

        # draw particle

        glBegin(GL_LINES)
        glVertex3f(x, y - 0.08, z)
        glVertex3f(x, y, z)
        glEnd()

        # update particle with velocity
        particle.xv += particle.xa
        particle.yv += particle.ya
        particle.zv += particle.za

        particle.x += particle.xv
        particle.y += particle.yv
        particle.z += particle.zv

        if particle.y <= -10.0:
          particle.y = -10.0
          particle.xv = uniform(-0.04, 0.04)
          particle.yv *= -uniform(0.2, 0.4)
          particle.zv = uniform(-0.04, 0.04)

        # update particle's life
        particle.life -= particle.ageing

        if particle.life <= 0.0:
          self.reset_particle(particle)


        glPopAttrib()

def main():
  pygame.init()
  pygame.display.set_caption('Grafika')
  viewport = (800,600)
  hx = viewport[0]/2
  hy = viewport[1]/2
  srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
  glEnable(GL_BLEND)
  glClearColor(0.196078, 0.6, 0.8, 1.0)
  glEnableClientState(GL_VERTEX_ARRAY)

    # most obj files expect to be smooth-shaded

  # LOAD OBJECT AFTER PYGAME INIT
  obj = OBJ('Car.obj', swapyz=True)

  clock = pygame.time.Clock()

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  width, height = viewport
  gluPerspective(90.0, width/float(height), 1, 100.0)
  glEnable(GL_DEPTH_TEST)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  smoke = SmokeParticleSystem(0.0, 0.5, 2.0)
  rain = RainParticleSystem(0.0, 0.0, 0.0, 5.0)

  rotate = move = False
  lx, ly, lz = 0.0, 50.0, 0.0
  rx, ry, rz = 0.0, 0.0, 0.0
  tx, ty, tz = 0.0, 0.0, 5.0
  panx = pany = panz = rotx = roty = rotz = colr = colg = colb = movx = movy = movz = 0
  red = green = blue = 1.0
  posx = posy = posz = 0
  smoke_active = rain_active = True

  x = 0.0
  xv = 0.0

  z = 0.0
  zv = 0.0

  y = 0.0
  yv = 0.0
  ya = -0.04

  counter = 0
  start = time.time()

  while 1:
    clock.tick(200)

    for e in pygame.event.get():
      if e.type == QUIT:
        sys.exit()
      elif e.type == KEYDOWN:
        if e.key == K_ESCAPE:
          sys.exit()
        elif e.key == K_q:
          panx = -1
        elif e.key == K_w:
          panx = 1
        elif e.key == K_a:
          pany = -1
        elif e.key == K_s:
          pany = 1
        elif e.key == K_z:
          panz = -1
        elif e.key == K_x:
          panz = 1
        elif e.key == K_e:
          rotx = -1
        elif e.key == K_r:
          rotx = 1
        elif e.key == K_d:
          roty = -1
        elif e.key == K_f:
          roty = 1
        elif e.key == K_c:
          rotz = -1
        elif e.key == K_v:
          rotz = 1
        elif e.key == K_t and red > 0:
          colr = -0.0625
        elif e.key == K_y and red < 1:
          colr = 0.0625
        elif e.key == K_g and green > 0:
          colg = -0.0625
        elif e.key == K_h and green < 1:
          colg = 0.0625
        elif e.key == K_b and blue > 0:
          colb = -0.0625
        elif e.key == K_n and blue < 1:
          colb = 0.0625
        elif e.key == K_u:
          movx = -100
        elif e.key == K_i:
          movx = 100
        elif e.key == K_j:
          movy = -100
        elif e.key == K_k:
          movy = 100
        elif e.key == K_m:
          movz = -100
        elif e.key == K_COMMA:
          movz = 100
        elif e.key == K_SPACE:
          yv += 0.4

        elif e.key == K_1:
          xv = -0.4
        elif e.key == K_2:
          zv = -0.4
        elif e.key == K_3:
          zv = 0.4
        elif e.key == K_4:
          xv = 0.4
        elif e.key == K_9:
          rain_active = not rain_active
        elif e.key == K_0:
          smoke_active = not smoke_active

      elif e.type == KEYUP:
        panx = pany = panz = rotx = roty = rotz = colr = colg = colb = movx = movy = movz = xv = zv = 0
      elif e.type == MOUSEBUTTONDOWN:
        if e.button == 1:
          rotate = True
        elif e.button == 3:
          move = True
      elif e.type == MOUSEBUTTONUP:
        if e.button == 1:
          rotate = False
        elif e.button == 3:
          move = False
      elif e.type == MOUSEMOTION:
        i, j = e.rel
        if rotate:
          rx += i
          ry += j
        if move:
          tx += i
          ty -= j

    tx += panx
    ty += pany
    tz += panz

    rx += rotx
    ry += roty
    rz += rotz

    lx += movx
    ly += movy
    lz += movz

    red += colr
    green += colg
    blue += colb

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION,  (lx, ly, lz, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (red, green, blue, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)


    # RENDER OBJECT
    glTranslate(tx, ty, -tz)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glRotate(rz, 0, 0, 1)
    #loadImage()
    #glRotate(PI, 1, 0, 0)

    #glRotate(-100, 1, 0, 0)

    if y <= -10.0:
      y = -10.0
      yv *= -uniform(0.2, 0.6)
    else:
      yv += ya
    y += yv

    x += xv
    z += zv

    glColor3f(0.0, 0.8, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-400.0,-10.0,400.0)
    glVertex3f(400.0,-10.0,400.0)
    glVertex3f(400.0,-10.0,-400.0)
    glVertex3f(-400.0,-10.0,-400.0);
    glEnd()

    glPushMatrix()
    glTranslate(x, y, z)

    glPushMatrix()
    glRotate(-90, 1, 0, 0)
    glCallList(obj.gl_list)
    glPopMatrix()
    if smoke_active:
        smoke.render()
    glPopMatrix()

    glPushMatrix()
    glTranslate(x, 0, z)
    if rain_active:
        rain.render()
    glPopMatrix()

    pygame.display.flip()

    counter += 1
    print("FPS :", counter/(time.time()-start))

if __name__ == '__main__':
  main()
