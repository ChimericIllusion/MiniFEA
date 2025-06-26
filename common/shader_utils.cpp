#include "shader_utils.hpp"
#include <iostream>

static void checkCompile(GLuint shader) {
    GLint ok;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &ok);
    if (!ok) {
        GLint len; glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &len);
        std::string log(len, ' ');
        glGetShaderInfoLog(shader, len, &len, &log[0]);
        std::cerr << "Shader compile error:\n" << log << std::endl;
        throw std::runtime_error("Shader compile failed");
    }
}

static void checkLink(GLuint prog) {
    GLint ok;
    glGetProgramiv(prog, GL_LINK_STATUS, &ok);
    if (!ok) {
        GLint len; glGetProgramiv(prog, GL_INFO_LOG_LENGTH, &len);
        std::string log(len, ' ');
        glGetProgramInfoLog(prog, len, &len, &log[0]);
        std::cerr << "Program link error:\n" << log << std::endl;
        throw std::runtime_error("Program link failed");
    }
}

GLuint compileShader(GLenum type, const char* src) {
    GLuint s = glCreateShader(type);
    glShaderSource(s, 1, &src, nullptr);
    glCompileShader(s);
    checkCompile(s);
    return s;
}

GLuint compileAndLink(const char* vertSrc, const char* fragSrc) {
    GLuint vs = compileShader(GL_VERTEX_SHADER, vertSrc);
    GLuint fs = compileShader(GL_FRAGMENT_SHADER, fragSrc);
    GLuint prog = glCreateProgram();
    glAttachShader(prog, vs);
    glAttachShader(prog, fs);
    glLinkProgram(prog);
    checkLink(prog);
    glDeleteShader(vs);
    glDeleteShader(fs);
    return prog;
}
