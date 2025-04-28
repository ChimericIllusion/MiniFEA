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
