#pragma once

#include <GL/glew.h>

// Compile a GLSL shader from source. Throws on error (you can log instead).
GLuint compileShader(GLenum type, const char* src);

// Link a vertex+fragment into a program. Returns program handle.
GLuint compileAndLink(const char* vertSrc, const char* fragSrc);
