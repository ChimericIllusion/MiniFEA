#include "mesh_utils.hpp"
#include <cmath>

void buildConeCylinderMesh(
    float length,
    float radius,
    std::vector<glm::vec3>& V,
    std::vector<GLuint>& I,
    int segs
) {
    V.clear(); I.clear();
    float cylH = length * 0.8f;
    float coneH = length - cylH;

    // cylinder ring
    for (int i = 0; i < segs; ++i) {
        float a = 2.0f * M_PI * i / segs;
        float x = cos(a) * radius, y = sin(a) * radius;
        V.emplace_back(x, y, 0.0f);
        V.emplace_back(x, y, cylH);
    }
    // cone base ring
    int baseStart = (int)V.size();
    for (int i = 0; i < segs; ++i) {
        float a = 2.0f * M_PI * i / segs;
        float x = cos(a) * radius * 0.6f, y = sin(a) * radius * 0.6f;
        V.emplace_back(x, y, cylH);
    }
    // cone apex
    V.emplace_back(0.0f, 0.0f, length);
    int apex = (int)V.size() - 1;

    // cylinder quads -> two triangles each
    for (int i = 0; i < segs; ++i) {
        int i0 = 2*i, i1 = 2*i+1;
        int j0 = 2*((i+1)%segs), j1 = 2*((i+1)%segs)+1;
        I.push_back(i0); I.push_back(j0); I.push_back(i1);
        I.push_back(i1); I.push_back(j0); I.push_back(j1);
    }
    // cone triangles
    for (int i = 0; i < segs; ++i) {
        int b0 = baseStart + i;
        int b1 = baseStart + ((i+1)%segs);
        I.push_back(b0); I.push_back(b1); I.push_back(apex);
    }
}
