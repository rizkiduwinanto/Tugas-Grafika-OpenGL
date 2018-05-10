import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *

def main():
	pygame.init()
	viewport = (800,600)
	hx = viewport[0]/2
	hy = viewport[1]/2
	srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

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


	rotate = move = False
	lx, ly, lz = 0, 50, 0
	rx, ry, rz = 0, 0, 0
	tx, ty, tz = 0, 0, 5
	panx = pany = panz = rotx = roty = rotz = colr = colg = colb = movx = movy = movz = 0
	red = green = blue = 1.0
	while 1:
		clock.tick(30)
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
					rx, ry, rz = 0, 0, 0
					tx, ty, tz = 0, 0, 5

			elif e.type == KEYUP:
				panx = pany = panz = rotx = roty = rotz = colr = colg = colb = movx = movy = movz = 0
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
		# loadImage()
		glCallList(obj.gl_list)
		
		glBegin(GL_QUADS)
		glVertex3f(-4000.0,-100,10000.0)
		glVertex3f(4000.0,-100,10000.0)
		glVertex3f(4000.0,80,-10000.0)
		glVertex3f(-4000.0,80,-10000.0);
		glEnd()

		pygame.display.flip()

if __name__ == '__main__':
	main()
