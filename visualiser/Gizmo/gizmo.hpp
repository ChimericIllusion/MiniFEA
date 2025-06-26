// ======================= gizmo.cpp =======================
#include "gizmo.hpp"
#include "common/shader_utils.hpp"
#include "common/mesh_utils.hpp"

#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <vector>

// Vertex shader source
static const char* gizmoVertSrc = R"GLSL(
#version 330 core
layout(location=0) in vec3 aPos;
uniform mat4 uMVP;
out vec3 vColor;
uniform vec3 uColor;
void main() {
    vColor = uColor;
    gl_Position = uMVP * vec4(aPos, 1.0);
}
)GLSL";

// Fragment shader source
static const char* gizmoFragSrc = R"GLSL(
#version 330 core
in vec3 vColor;
out vec4 fragColor;
void main() {
    fragColor = vec4(vColor, 1.0);
}
)GLSL";

void Gizmo::init(float arrowLength, float arrowRadius) {
    size = arrowLength;
    cornerNDC = {-0.9f, -0.9f};

    shader = compileAndLink(gizmoVertSrc, gizmoFragSrc);

    std::vector<glm::vec3> verts;
    std::vector<GLuint> idx;
    buildConeCylinderMesh(arrowLength, arrowRadius, verts, idx);
    GLsizei idxCount = static_cast<GLsizei>(idx.size());

    glGenVertexArrays(1, &vao);
    glGenBuffers(1, &vbo);
    glGenBuffers(1, &ebo);

    glBindVertexArray(vao);
      glBindBuffer(GL_ARRAY_BUFFER, vbo);
      glBufferData(GL_ARRAY_BUFFER,
                   verts.size() * sizeof(glm::vec3),
                   verts.data(),
                   GL_STATIC_DRAW);

      glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                            sizeof(glm::vec3), (void*)0);
      glEnableVertexAttribArray(0);

      glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
      glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                   idxCount * sizeof(GLuint),
                   idx.data(),
                   GL_STATIC_DRAW);
    glBindVertexArray(0);
}

void Gizmo::drawOverlay(const glm::quat& camRot,
                        const glm::mat4& projNDC) {
    // backup and disable depth-write
    GLint oldMask;
    glGetIntegerv(GL_DEPTH_WRITEMASK, &oldMask);
    glDepthMask(GL_FALSE);
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);

    glUseProgram(shader);
    glBindVertexArray(vao);

    glm::mat4 base = glm::translate(glm::mat4(1.0f), glm::vec3(cornerNDC, 0.0f))
                   * glm::mat4_cast(glm::inverse(camRot))
                   * glm::scale(glm::mat4(1.0f), glm::vec3(size));

    auto setMVPandColor = [&](const glm::mat4& M, const glm::vec3& col) {
        glm::mat4 mvp = projNDC * M;
        glUniformMatrix4fv(
          glGetUniformLocation(shader, "uMVP"),
          1, GL_FALSE, glm::value_ptr(mvp)
        );
        glUniform3fv(
          glGetUniformLocation(shader, "uColor"),
          1, glm::value_ptr(col)
        );
    };

    // +X axis: rotate -90° about Y
    setMVPandColor(
      glm::rotate(base, glm::radians(-90.0f), glm::vec3(0,1,0)),
      {1,0,0}
    );
    glDrawElements(GL_TRIANGLES, idxCount, GL_UNSIGNED_INT, 0);

    // +Y axis: rotate +90° about X
    setMVPandColor(
      glm::rotate(base, glm::radians(90.0f), glm::vec3(1,0,0)),
      {0,1,0}
    );
    glDrawElements(GL_TRIANGLES, idxCount, GL_UNSIGNED_INT, 0);

    // +Z axis: no extra rotation
    setMVPandColor(base, {0,0,1});
    glDrawElements(GL_TRIANGLES, idxCount, GL_UNSIGNED_INT, 0);

    // restore depth-write
    glDepthMask(oldMask);
    glBindVertexArray(0);
    glUseProgram(0);
}

// Optional: pybind11 wrapper to expose to Python
#ifdef BUILD_PYBIND11
#include <pybind11/pybind11.h>
namespace py = pybind11;
PYBIND11_MODULE(_gizmo, m) {
    py::class_<Gizmo>(m, "Gizmo")
        .def(py::init<>())
        .def("init", &Gizmo::init,
             py::arg("arrowLength") = 0.1f,
             py::arg("arrowRadius") = 0.005f)
        .def("drawOverlay", &Gizmo::drawOverlay,
             py::arg("camRot"), py::arg("projNDC"));
}
#endif
