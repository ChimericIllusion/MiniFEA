# main.py

import os
import sys
import numpy as np
from visualiser.mesh_data import MeshData
from visualiser.scene import Scene
from visualiser.camera import Camera
from visualiser.view_manager import ViewManager
from visualiser.projection_manager import ProjectionManager
from visualiser.input_controller import InputController
from visualiser.hud_overlay import HUDOverlay
from visualiser.renderer import Renderer

def load_example_truss():
    """
    Returns simple 2D truss example:
      - nodes: 3 nodes in an L shape
      - elems: two bars
      - disp: zero displacements
      - field: dummy scalar at each node
      - bc_flags: empty for now
    """
    nodes = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
    ])
    elems = np.array([
        [0, 1],
        [1, 2],
    ], dtype=int)
    disp = np.zeros_like(nodes)
    field = np.linspace(0.1, 0.3, nodes.shape[0])
    bc_flags = {}
    return nodes, elems, disp, field, bc_flags

def main():
    # Compute paths
    HERE      = os.path.dirname(os.path.abspath(__file__))
    SHADER_DIR = os.path.join(HERE, "visualiser", "shaders")
    vert_path = os.path.join(SHADER_DIR, "line.vert")
    frag_path = os.path.join(SHADER_DIR, "line.frag")
    colormaps = [
        # add paths here if you have colormap textures
        # os.path.join(SHADER_DIR, "colormaps", "viridis.png"),
    ]

    # 1) Load FEA data arrays
    nodes, elems, disp, field, bc_flags = load_example_truss()

    # 2) Build MeshData and Scene (no GL calls yet)
    mesh_data = MeshData(nodes, elems, disp=disp, field=field)
    scene     = Scene(mesh_data)

    # 3) Set up camera and view presets
    camera = Camera()
    views  = ViewManager(camera)
    dummy_fov = np.radians(60.0)
    for name, pos, up in [
        ("Top",   (0, 0, 1.0), (0, 1, 0)),
        ("Front", (0, 1.0, 0), (0, 0, 1)),
        ("Side",  (1.0, 0, 0), (0, 0, 1)),
    ]:
        views.add(name, {
            "position": pos,
            "target":   (0, 0, 0),
            "up":       up,
            "mode":     "ortho",
            "fov":      dummy_fov,
            "ortho_size": 1.0,
            "near":     0.1,
            "far":      10.0,
        })
    views.add("Iso", {
        "position":  (1.0, 1.0, 1.0),
        "target":    (0, 0, 0),
        "up":        (0, 1, 0),
        "mode":      "persp",
        "fov":       np.radians(45.0),
        "ortho_size": None,
        "near":      0.1,
        "far":       10.0,
    })

    # 4) Projection manager
    proj_mgr = ProjectionManager()

    # 5) Input controller
    input_ctrl = InputController(
        camera=camera,
        view_manager=views,
        scene=scene,
        shader=None,           # placeholder; Renderer will create ShaderManager
        exit_callback=lambda: sys.exit(0),
    )

    # 6) HUD overlay (stub FPS callback)
    hud = HUDOverlay(
        view_manager=views,
        shader_manager=None,   # placeholder; Renderer will assign real shader
        scene=scene,
        fps_callback=lambda: 60.0
    )

    # 7) Create renderer and start loop
    renderer = Renderer(
        scene=scene,
        vert_path=vert_path,
        frag_path=frag_path,
        colormaps=colormaps,
        camera=camera,
        proj_mgr=proj_mgr,
        hud=hud,
        input_ctrl=input_ctrl,
        width=800,
        height=600,
        title="MiniFEA Truss Viewer"
    )
    renderer.start()

if __name__ == "__main__":
    main()
