#pragma once

#include <vector>
#include <glm/glm.hpp>

// Builds a combined cylinder+cone mesh along +Z axis.
// - length: total arrow length
// - radius: cylinder radius (cone base is 0.6*radius)
// - V: output list of 3D positions
// - I: output list of triangle indices
// - segs: number of radial segments
void buildConeCylinderMesh(
    float length,
    float radius,
    std::vector<glm::vec3>& V,
    std::vector<GLuint>& I,
    int segs = 24
);
