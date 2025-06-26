
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
