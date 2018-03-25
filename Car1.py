#! /usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

def drawWheel():
    glColor3f(0.0, 1.0, 0.0)
    glTranslate(3, 1, 0)
    glutSolidSphere(0.5, 20, 20)
    glTranslate(5, 1, 0)
    glutSolidSphere(0.5, 20, 20)

def drawCar():
    glBegin(GL_POLYGON)
    glColor(0.0, 1.0, 1.0, 1.0)
    glVertex3f(9.0, 1.0, 0,0)
    glVertex3f(9.0, 2.0, 0,0)
    glVertex3f(7.0, 2.0, 0,0)
    glVertex3f(5.0, 3.0, 0,0)
    glVertex3f(3.0, 3.0, 0,0)
    glVertex3f(2.0, 2.0, 0,0)
    glVertex3f(1.0, 2.0, 0,0)
    glVertex3f(1.0, 1.0, 0,0)
    glEnd()

def render():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1, 1.0, 2000.0)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslate(-5, 0, -20)
    #drawCar()
    drawWheel()
    glPopMatrix()
    glTranslate(3.0, 1.0, 0.0)
    glutSwapBuffers()

def idle():
    glutPostRedisplay()

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    windowid = glutCreateWindow(b'Grafika Tugas 9')
    glClearColor(0, 0, 0, 1)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(render)
    glutIdleFunc(idle)
    glutMainLoop()
