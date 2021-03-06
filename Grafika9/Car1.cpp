#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#include <unistd.h>

#define ESCAPE 27

int window;
float rotation_tri = 0.0f;
float rotation_quad = 0.0f;

void initGL(int width, int height){
  glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
  glClearDepth(1.0);
  glDepthFunc(GL_LESS);
  glEnable(GL_DEPTH_TEST);
  glShadeModel(GL_SMOOTH);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(45.0f, (GLfloat) width / (GLfloat) height, 0.1f, 100.0f);
  glMatrixMode(GL_MODELVIEW);
}

void resizeGLScene(int width, int height){
  if (height == 0) {
    height = 1;
  }
  glViewport(0, 0, width, height);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(45.0f, (GLfloat) width / (GLfloat) height, 0.1f, 100.0f);
  glMatrixMode(GL_MODELVIEW);
}

void drawWheel(float x, float y) {
  int timeElapsed = glutGet(GLUT_ELAPSED_TIME);
  float revolveScale1 = 0.2f;
  glPushMatrix();
  glColor3f(0.0, 0.0, 1.0);
  glTranslatef(x, y, 0.0f);
  glRotatef(timeElapsed * revolveScale1,0.0,0.0,1.0);
  glutSolidSphere(0.75, 20, 20);
  glColor3f(1.0, 1.0, 1.0);
  for(int i=0; i<5; ++i) {
    glPushMatrix();
    glRotatef(72.0f*i,0.0,0.0,1.0);
    glTranslatef(0.44f, 0.0, 0.0);
    glutSolidSphere(0.1f, 16, 16);
    glPopMatrix();
  }
  glTranslatef(0.0f, 0.0f, 0.0f);
  glutSolidSphere(0.1, 16, 16);
  glPopMatrix();
  glFlush();
  glutPostRedisplay();
}

void drawCar(){
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glLoadIdentity();
  glTranslatef(-5.0f, 0.0f, -15.0f);
  glBegin(GL_POLYGON);
  glColor3f(0.0f, 1.0f, 0.0f);
  glVertex3f(9.0f, 1.0f, 0.0f);
  glVertex3f(9.0f, 2.0f, 0.0f);
  glVertex3f(7.0f, 2.0f, 0.0f);
  glVertex3f(5.0f, 3.0f, 0.0f);
  glVertex3f(3.0f, 3.0f, 0.0f);
  glVertex3f(2.0f, 2.0f, 0.0f);
  glVertex3f(1.0f, 2.0f, 0.0f);
  glVertex3f(1.0f, 1.0f, 0.0f);
  glEnd();
  drawWheel(3.0f, 1.0f);
  drawWheel(6.5f, 1.0f);
  glutSwapBuffers();
}

void keyPressed(unsigned char key, int x, int y){
  usleep(100);
  if (key == ESCAPE){
    glutDestroyWindow(window);
  }
  exit(0);
}

int main(int argc, char **argv){
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH);
  glutInitWindowSize(640, 480);
  glutInitWindowPosition(0, 0);
  window = glutCreateWindow("Tugas Grafika 9");
  glutDisplayFunc(&drawCar);
  glutIdleFunc(&drawCar);
  glutReshapeFunc(&resizeGLScene);
  glutKeyboardFunc(&keyPressed);
  glutMainLoop();
  return 1;
}
