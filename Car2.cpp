#include <GL/glew.h>
#include <GL/glut.h>
#include <iostream>
#include <string>

std::string vertexShader = "#version 430\n"
                           "in vec3 pos;"
                           "void main() {"
                           "gl_Position = vec4(pos, 1);"
                           "}";

std::string fragmentShader = "#version 430\n"
                             "void main() {"
                             "gl_FragColor = vec4(0, 1, 0, 0);"
                             "}";


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
    GLfloat vertices[] =
		{
			-0.3, -0.3, 0,
			0.3, -0.3, 0,
			0.3, 0.3, 0,
			-0.3, 0.3, 0
    };

		GLuint elements[] =
		{
    	0, 1, 2,
    	2, 3, 0
		};

    GLuint vboId;
    glGenBuffers(1, &vboId);
    glBindBuffer(GL_ARRAY_BUFFER, vboId);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    return vboId;
}

void init(){
    glClearColor(0, 0, 0, 0);
    GLuint vboId = loadDataInBuffers();
    GLuint vShaderId = compileShaders(vertexShader, GL_VERTEX_SHADER);
    GLuint fShaderId = compileShaders(fragmentShader, GL_FRAGMENT_SHADER);
    GLuint programId = linkProgram(vShaderId, fShaderId);
    GLuint posAttributePosition = glGetAttribLocation(programId, "pos");
    GLuint vaoId;
    glGenVertexArrays(1, &vaoId);
    glBindVertexArray(vaoId);
    glBindBuffer(GL_ARRAY_BUFFER, vboId);
    glVertexAttribPointer(posAttributePosition, 3, GL_FLOAT, false, 0, 0);
    glEnableVertexAttribArray(posAttributePosition);
    glUseProgram(programId);
}

void display(){
    glClear(GL_COLOR_BUFFER_BIT);
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
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
