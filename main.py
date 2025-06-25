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
    Returns a basic 3D pyramid wireframe:
      - nodes: 5 nodes (square base + apex)
      - elems: 8 bars (4 base edges + 4 sides)
      - disp: zero displacements
      - field: dummy scalar at each node
      - bc_flags: empty for now
    """
    nodes = np.array([
        [0.0, 0.0, 0.0],  # 0
        [1.0, 0.0, 0.0],  # 1
        [1.0, 0.0, 1.0],  # 2
        [0.0, 0.0, 1.0],  # 3
        [0.5, 1.0, 0.5],  # 4 
    ], dtype=float)

    elems = np.array([
        # base square
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0],
        # sides to apex
        [0, 4],
        [1, 4],
        [2, 4],
        [3, 4],
    ], dtype=int)

    disp = np.zeros_like(nodes)
    field = np.linspace(0.0, 1.0, nodes.shape[0])
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
    
    # Compute centroid
    centroid = nodes.mean(axis=0)
    radius = np.linalg.norm(nodes-centroid, axis=1).max()
    # 2) Build MeshData and Scene (no GL calls yet)
    mesh_data = MeshData(nodes, elems, disp=disp, field=field)
    scene     = Scene(mesh_data)

    # 3) Set up camera and view presets
    camera = Camera(
        position=(1.0, 1.0, 1.0),    # whatever your default eye is
        target=tuple(centroid),     # now dynamically centered
        up=(0,1,0),
        mode='persp',
        fov=np.radians(45.0),
        ortho_size=1.0,
        near=0.1,
        far=10.0
    )

    views  = ViewManager(camera)
    dummy_fov = np.radians(60.0)
    presets = {
    "Top":    ((centroid[0], centroid[1]+1.0, centroid[2]), (0,0,-1)),
    "Front":  ((centroid[0], centroid[1],   centroid[2]+1.0), (0,1,0)),
    "Side":   ((centroid[0]+1.0, centroid[1], centroid[2]), (0,1,0)),
    "Iso":    ((centroid[0]+1.0, centroid[1]+1.0, centroid[2]+1.0), (0,1,0)),
    }
    for name,(pos,up) in presets.items():
        views.add(name, {
            "position": pos,
            "target":   tuple(centroid),
            "up":       up,
            "mode":     "ortho" if name!="Iso" else "persp",
            "fov":      dummy_fov if name!="Iso" else np.radians(45.0),
            "ortho_size": 1.0,
            "near":     0.1,
            "far":      10.0,
        })

    # ← SNAP TO ISO BEFORE RENDERER STARTS
    views.goTo("Iso")
    camera.fit(centroid, radius)
    # 4) Projection manager
    proj_mgr = ProjectionManager()

    # 5) Input controller
    input_ctrl = InputController(
        camera=camera,
        view_manager=views,
        scene=scene,
        shader=None,           # placeholder; Renderer will create ShaderManager
        exit_callback=lambda: sys.exit(0),
        fit_center=centroid,
        fit_radius=radius
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
