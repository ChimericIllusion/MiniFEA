cmake_minimum_required(VERSION 3.14)
project(gizmo_module)

find_package(pybind11 REQUIRED)
find_package(glm REQUIRED)
find_package(GLEW REQUIRED)

pybind11_add_module(_gizmo
  gizmo.cpp
)
target_link_libraries(_gizmo
  PRIVATE glm::glm GLEW::GLEW
)
target_include_directories(_gizmo
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)
set_target_properties(_gizmo PROPERTIES
  PREFIX ""
  OUTPUT_NAME "gizmo"
)
