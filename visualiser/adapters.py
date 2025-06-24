# adapters.py

"""
adapters.py

VisualData adapter: takes raw arrays from the user, builds a MeshData,
and optionally a Scene.
"""
import numpy as np
from .mesh_data import MeshData
from .scene import Scene

class VisualData:
    """
    Adapter so that external code sees:
      .nodes, .elements, .displacements, .scalar_field, .bc_flags
    and can get a GPU-ready Scene.
    """
    def __init__(self,
                 nodes,
                 elements,
                 displacements=None,
                 scalar_field=None,
                 bc_flags=None):
        self.nodes = np.asarray(nodes, dtype=float)
        self.elements = np.asarray(elements, dtype=int)
        self.displacements = (np.asarray(displacements, dtype=float)
                              if displacements is not None else None)
        self.scalar_field = (np.asarray(scalar_field, dtype=float)
                              if scalar_field is not None else None)
        self.bc_flags = bc_flags or {}

    def to_mesh_data(self):
        """
        Construct and return a MeshData instance from stored arrays.
        """
        return MeshData(
            nodes=self.nodes,
            elems=self.elements,
            disp=self.displacements,
            field=self.scalar_field
        )

    def to_scene(self):
        """
        Build a Scene from this VisualData, including GL buffer initialization.
        Must be called after an OpenGL context is active.
        """
        mesh_data = self.to_mesh_data()
        scene = Scene(mesh_data)
        scene.initialize_gl()
        return scene
    