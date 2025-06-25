// visualiser/shaders/line.vert
#version 330 core

layout(location = 0) in vec3 a_position;

uniform mat4 uMVP;

void main() {
    gl_Position = uMVP * vec4(a_position, 1.0);
}
