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

## Renderer To-Do List

---

### 1. 3-Axis Gizmo Overlay

**Description:**
Render a fixed-size 3-axis gizmo in the viewport corner to show current camera orientation.

**Implementation Steps:**

* Create a Gizmo VAO with three arrow meshes (cone + cylinder), colored X = red, Y = green, Z = blue.
* In `drawOverlay()`, bind an identity model matrix, apply only the camera’s rotation quaternion, then draw the gizmo VAO.
* Position the gizmo at NDC corner coordinates (e.g. `(-0.9, -0.9)`) and disable depth-write (keep depth-test ≤).
* Ensure uniform camera-space scaling so the gizmo size remains constant when zooming.

**Testing Notes:**

* Capture reference renders for Top/Front/Side views and compare via CI pixel-diff.
* Unit-test that, given known camera quaternions, the computed gizmo model matrix aligns each axis correctly.

---

### 2. Embedded Scripting Console Hook

**Description:**
Embed a live Python REPL overlay for inspecting/modifying scene state, camera parameters, and renderer settings at runtime.

**Implementation Steps:**

* Initialize the Python interpreter at startup (via Python C API or pybind11) and expose engine APIs under a `fea_engine` module.
* Toggle the console UI with a hotkey (e.g. `` ` `` or `Ctrl+~`), capturing text input and rendering a scrollable text buffer.
* On Enter, feed the command to the interpreter (`PyRun_SimpleString()`), catch exceptions, and append results or tracebacks to the buffer.
* Expose key methods such as:

  * `fea_engine.camera.get_position()`
  * `fea_engine.scene.nodes['<id>'].transform.translate(x, y, z)`
  * `fea_engine.renderer.set_colormap('jet')`

**Testing Notes:**

* Run a headless test harness that executes sample console commands to ensure no crashes.
* Write coverage tests to verify every exposed API function responds as documented.
