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


## Rendering Capabilities

MiniFEA includes a built-in, real-time 3D viewer powered by OpenGL (via PyOpenGL and GLUT) for interactive visualization of undeformed and deformed meshes.

### Core Components

* **Renderer**

  * Manages the OpenGL context, main loop, and draw callbacks
  * Clears buffers, computes MVP (Model-View-Projection) via `ProjectionManager` + `Camera`, and issues draw calls both for wireframe and debug spheres at nodes&#x20;
  * Renders an overlaid HUD (view name, FPS, deformation state, colormap legend) via `HUDOverlay`&#x20;

* **Scene**

  * Wraps `MeshData`, creates and uploads VBO/EBO buffers for node positions and (optional) displacements
  * Draws undeformed wireframe and, when toggled, an overlaid deformed mesh&#x20;

* **ShaderManager**

  * Compiles/links GLSL vertex & fragment shaders from disk
  * Manages 1D colormap textures (PNG LUTs) and uniform updates for MVP and colormap lookup
  * Supports cycling through multiple colormaps at runtime&#x20;

* **ProjectionManager**

  * Generates 4×4 perspective or orthographic projection matrices based on camera parameters (FOV, ortho size, near/far) and viewport aspect ratio&#x20;

* **Camera**

  * Arcball-style orbit around a target, with pan, zoom (dolly or ortho scale), and reset
  * Provides a right-handed “look-at” view matrix and automatic “fit to bounding sphere” functionality&#x20;

* **ViewManager**

  * Registers named camera presets (e.g. Top, Front, Side, Iso) and applies them on key press
  * Keeps configuration of position, target, up-vector, projection mode, and clipping planes&#x20;

* **InputController**

  * Maps keyboard & mouse events to viewer actions:

    * **Keys**:

      * `1–4`: switch to preset views
      * `r`: reset camera (and refit)
      * `d`: toggle deformed overlay
      * `c`: cycle colormap
      * `Esc`: exit viewer
    * **Mouse**:

      * Left-drag: orbit
      * Right-drag: pan
      * Scroll wheel: zoom&#x20;

### Workflow

1. **Instantiate** your `VisualData` adapter with raw nodes, elements, displacements, scalar field, and BC flags.
2. **Build** a `Scene` from the adapter and call `initialize_gl()` once the OpenGL context exists.
3. **Create** a `Renderer`, supplying the `Scene`, shader paths, colormap list, `Camera`, `ProjectionManager`, `HUDOverlay`, and `InputController`.
4. **Start** the viewer with `.start()`, entering an interactive loop for live mesh inspection, deformation toggling, and colormap exploration.

---



