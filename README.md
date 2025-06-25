# MiniFEA

MiniFEA is a lightweight, modular Finite Element Analysis (FEA) library written in Python.  
Its current focus is on providing an interactive rendering engine; core solving and physics modules are on the roadmap.

## Current Capabilities

### Real-Time Rendering
- **Built-in 3D Viewer** powered by OpenGL (via PyOpenGL & GLUT)  
  - Wireframe display of undeformed mesh  
  - Overlaid deformed mesh visualization  
  - Dynamic colormap legend & HUD (view name, FPS, deformation state)  
  - Preset cameras (Top, Front, Side, Isometric) + `r` to reset  
  - Interactive controls:  
    - Orbit (mouse drag)  
    - Pan (right drag)  
    - Zoom (scroll)  
    - `d` to toggle deformation overlay  
    - `c` to cycle colormaps  
    - `Esc` to exit  

### Rendering Architecture
- **Renderer**: manages GL context, draw loop & HUDOverlay  
- **Scene**: uploads node/element buffers (VBO/EBO), toggles deformed overlay  
- **ShaderManager**: compiles GLSL shaders, handles LUT textures  
- **Camera + ProjectionManager**: arcball controls, perspective/ortho matrices  
- **InputController**: keyboard/mouse mapping for live interaction  

---

## Planned Physics & Solver Features

> _These are not yet implemented. Contributions welcome!_

- **1D bar & 2D truss elements**  
- **Global stiffness matrix assembly**  
- **Boundary condition enforcement**  
- **Static linear‐elastic solver** (displacements → strains → stresses)  
- **Modal analysis** (natural frequencies & mode shapes)  
- **Beam bending (Euler–Bernoulli)**  
- **2D quadrilateral elements** (plane stress/strain)  
- **Mesh I/O** (JSON, VTK)  
- **Basic nonlinear materials**  

---

## Project Goals

- Provide a self-contained, transparent rendering core for mesh inspection  
- Lay the groundwork for a full FEA pipeline in Python  
- Emphasize clarity, modularity, and ease of extension  
- Offer thorough documentation and examples for both rendering and future solver APIs  
