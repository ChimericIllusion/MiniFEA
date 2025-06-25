import numpy as np
def pyramid_truss():
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