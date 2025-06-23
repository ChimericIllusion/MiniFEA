# main.py
import numpy as np

from visualiser.mesh_adapter import VisualData
from visualiser.viewer_app import launch_viewer
from visualiser.colour_maps import available_maps

# ——— Your FEA data ———
nodes         = np.array([[0, 0], [1, 1], [2, 0]])
elements      = [(0, 1), (1, 2), (0, 2)]
displacements = np.array([0, 0, 0.02, 0, 0.01, -0.01])
scalar_field  = np.array([100.0,  50.0, -75.0])
bc_flags      = {0: (True, True)}

data = VisualData(nodes, elements, displacements, scalar_field, bc_flags)

# ——— Pick your colormap ———
print("Available colormaps:", available_maps())
cmap = 'viridis'   # ← change this to any name from the list above

# ——— Launch! ———
launch_viewer(data, scale=10.0, cmap=cmap)
