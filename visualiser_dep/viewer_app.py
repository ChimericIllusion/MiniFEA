# visualiser/viewer_app.py
from vispy import app
from .render2d import TrussViewer
from visualiser_dep.visualiser23 import Visualiser23

# visualiser/viewer_app.py

def launch_viewer(data, scale=1.0, cmap='viridis'):
    """
    Launch the appropriate viewer (2D or 3D) based on data dimensionality.
    """
    # 3D mode: full XYZ data → use the combined 2D/3D OpenGL viewer
    if data.nodes.shape[1] == 3:
        from visualiser_dep.visualiser23 import Visualiser23
        vis = Visualiser23(
            nodes=data.nodes,
            elements=data.elements,
            displacements=data.displacements,
            field=data.scalar_field,
            scale=scale
        )
        vis.start()
        return

    # 2D mode: strip off the Z coordinate and any Z‐BC flags
    from visualiser_dep.render2d import TrussViewer

    nodes2d = data.nodes[:, :2]
    disp2d  = data.displacements[:, :2]
    bc2d    = {
        nid: (ux, uy)
        for nid, (ux, uy, *_rest) in data.bc_flags.items()
    }

    viewer = TrussViewer(
        nodes=nodes2d,
        elements=data.elements,
        displacements=disp2d,
        scalar_field=data.scalar_field,
        bc_flags=bc2d,
        scale=scale,
        cmap=cmap
    )
    viewer.start()
