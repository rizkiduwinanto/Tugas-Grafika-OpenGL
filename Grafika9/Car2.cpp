#include <GL/glew.h>
#include <GL/glut.h>
#include <iostream>
#include <string>
#include <math.h>

std::string vertexShader = "#version 120\n"
                           "in vec3 pos;"
                           "void main() {"
                           "gl_Position = gl_ModelViewProjectionMatrix*vec4(pos, 1);"
                           "}";

std::string fragmentShader = "#version 120\n"
                             "void main() {"
                             "gl_FragColor = vec4(0, 1, 0, 0);"
                             "}";

std::string fragmentWheelShader = "#version 120\n"
                              "uniform vec4 color;"
														  "void main() {"
															"gl_FragColor = color;"
														  "}";

GLfloat color[] = {
      0, 1, 0, 1
};

GLfloat colorWheel[] = {
      0, 0, 1, 1
};

void rotate(float* vertices, int numberVertices, float centerX, float centerY, float angle){
	float angleSin = sin(angle);
	float angleCos = cos(angle);

	for (int i  = 0; i < numberVertices*3; i+=3){
		vertices[i] -= centerX;
		vertices[i+1] -= centerY;
		float xnew = vertices[i] * angleCos - vertices[i+1] * angleSin;
		float ynew = vertices[i] * angleSin + vertices[i+1] * angleCos;
		vertices[i] = xnew + centerX;
		vertices[i+1] = ynew + centerY;
	}
}

GLuint compileShaders(std::string shader, GLenum type){
    const char* shaderCode = shader.c_str();
    GLuint shaderId = glCreateShader(type);
    if (shaderId == 0) {
        std::cout << "Error creating shaders";
        return 0;
    }
    glShaderSource(shaderId, 1, &shaderCode, NULL);
    glCompileShader(shaderId);
    GLint compileStatus;
    glGetShaderiv(shaderId, GL_COMPILE_STATUS, &compileStatus);
    if (!compileStatus) {
        int length;
        glGetShaderiv(shaderId, GL_INFO_LOG_LENGTH, &length);
        char* cMessage = new char[length];
        glGetShaderInfoLog(shaderId, length, &length, cMessage);
        std::cout << "Cannot Compile Shader: " << cMessage;
        delete[] cMessage;
        glDeleteShader(shaderId);
        return 0;
    }

    return shaderId;
}

GLuint linkProgram(GLuint vertexShaderId, GLuint fragmentShaderId){
    GLuint programId = glCreateProgram();
    if (programId == 0) {
        std::cout << "Error Creating Shader Program";
        return 0;
    }
    glAttachShader(programId, vertexShaderId);
    glAttachShader(programId, fragmentShaderId);
    glLinkProgram(programId);
    GLint linkStatus;
    glGetProgramiv(programId, GL_LINK_STATUS, &linkStatus);
    if (!linkStatus) {
        std::cout << "Error Linking program";
        glDetachShader(programId, vertexShaderId);
        glDetachShader(programId, fragmentShaderId);
        glDeleteProgram(programId);
        return 0;
    }
    return programId;
}

GLuint loadDataInBuffers(){
		GLfloat vertices[] = {
		 	0.4f, -0.4f, 0.0f,
			-0.4f, -0.4f, 0.0f,
		 	-0.4f, 0.4f, 0.0f,
      0.4f, -0.4f, 0.0f,
			0.1f, 0.4f, 0.0f,
		 	-0.4f, 0.4f, 0.0f
		};

    GLfloat wheel[] = {
      0.1f, -0.1f, 0.0f,
      -0.1f, -0.1f, 0.0f,
      -0.1f, 0.1f, 0.0f,
      0.1f, -0.1f, 0.0f,
      0.1f, 0.1f, 0.0f,
      -0.1f, 0.1f, 0.0f,
    };

    GLuint vboId;
    glGenBuffers(1, &vboId);
    glBindBuffer(GL_ARRAY_BUFFER, vboId);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, 0);

    GLuint vboEd;
    glGenBuffers(1, &vboEd);
    glBindBuffer(GL_ARRAY_BUFFER, vboEd);
    glBufferData(GL_ARRAY_BUFFER, sizeof(wheel), wheel, GL_STATIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    return vboId;
}

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

void init(){
    glClearColor(0, 0, 0, 0);
    GLuint vboId = loadDataInBuffers();
    GLuint vShaderId = compileShaders(vertexShader, GL_VERTEX_SHADER);
    GLuint fShaderId = compileShaders(fragmentShader, GL_FRAGMENT_SHADER);
    GLuint programId = linkProgram(vShaderId, fShaderId);
    GLuint posAttributePosition = glGetAtribLocation(programId, "pos");
    GLuint vaoId;
    glGenVertexArrays(1, &vaoId);
    glBindVertexArray(vaoId);
    glBindBuffer(GL_ARRAY_BUFFER, vboId);
    glVertexAttribPointer(posAttributePosition, 3, GL_FLOAT, false, 0, 0);
    glEnableVertexAttribArray(posAttributePosition);
    glUseProgram(programId);
    GLuint colorLoc;
    colorLoc = glGetUniformLocation(programId, "color");
    glUniform4fv(colorLoc, 1, color);
}

void display(){
    glClear(GL_COLOR_BUFFER_BIT);
    glDrawArrays(GL_TRIANGLES, 0, 6);
    glutSwapBuffers();
}

int main(int argc, char** argv){
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE);
		glutInitWindowSize(640, 480);
	  glutInitWindowPosition(0, 0);
    glutCreateWindow("Tugas Grafika 9");
    glewInit();
    init();
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}
