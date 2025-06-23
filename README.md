# MiniFEA

MiniFEA is a lightweight, modular Finite Element Analysis (FEA) library written in Python.  
It is designed to serve as an educational and extensible foundation for structural mechanics simulations.

# Purpose
MiniFEA provides a clean and transparent implementation of core FEA principles — from stiffness matrix assembly to displacement solving and stress postprocessing — enabling engineers, researchers, and students to understand and extend the fundamentals of FEA software design.

# Scope
- 1D bar and 2D truss element support
- Global stiffness matrix construction
- Boundary condition handling
- Static linear elastic analysis
- Stress, strain, and displacement postprocessing
- Clear, testable, and extensible architecture

# Future Plans
- Add 2D quadrilateral elements for plane stress/strain problems
- Implement beam bending (Euler-Bernoulli elements)
- Introduce modal analysis (natural frequencies and mode shapes)
- Mesh import/export functionality (e.g., JSON, VTK)
- Visualizations for stress fields and deformation plots
- Extend to basic nonlinear material models

# Project Goals
- Deliver a self-contained FEA core suitable for learning and rapid prototyping
- Prioritize clarity, correctness, and modularity over black-box abstractions
- Provide thorough documentation and examples for educational use

# General Ideas


Adjustable deformation scale
Add a slider or hot-key (e.g. “+”/“–”) so you can dial the exaggeration factor on the fly rather than hard-coding it.

Field selector
Let the user switch between displacement, axial stress, strain, reaction forces, etc. (e.g. press “f” to cycle through available fields and update the colormap).

On-screen legend & colorbar
Overlay a dynamic colorbar with min/max values and units; update it whenever you change field or scale.

Node/element labeling
Toggle labels for node-IDs and element-IDs (e.g. “n” for nodes, “e” for elements) to aid debugging and mesh inspection.

Screenshot/export
Bind a key (e.g. “s”) to dump the current view to a PNG or SVG, complete with legend and axes.

Interactive tooltips
Hover over a node or element to pop up its computed value (e.g. displacement magnitude, stress).

Camera controls & presets
• Enable 3D orbit/rotate if you add 3D later,
• Add “home” and named-view presets so you can jump between front/top/side views.










Tools


