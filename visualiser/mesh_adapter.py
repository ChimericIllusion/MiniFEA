# visualiser/mesh_adapter.py

from dataclasses import dataclass, field
import numpy as np
from typing import List, Tuple, Dict, Union

@dataclass
class VisualData:
    raw_nodes: np.ndarray                     # (n_nodes, 2) or (n_nodes, 3)
    elements: List[Tuple[int, int]]           # [(n1, n2), ...]
    raw_displacements: np.ndarray             # flat array length n_nodes*2 or n_nodes*3
    scalar_field: np.ndarray                  # (n_elements,)
    bc_flags: Dict[int, Tuple[bool, ...]]     # {node_id: (ux_fixed, uy_fixed[, uz_fixed])}

    # — these fields are populated after init —
    nodes: np.ndarray = field(init=False)             # always (n_nodes, 3)
    displacements: np.ndarray = field(init=False)     # always (n_nodes, 3)

    def __post_init__(self):
        # --- nodes: pad to 3D if needed ---
        nodes = np.asarray(self.raw_nodes, float)
        if nodes.ndim != 2 or nodes.shape[1] not in (2, 3):
            raise ValueError(f"nodes must be (n,2) or (n,3), got shape {nodes.shape}")
        if nodes.shape[1] == 2:
            nodes = np.hstack([nodes, np.zeros((nodes.shape[0], 1))])
        self.nodes = nodes

        # --- displacements: reshape to (n_nodes, dims) ---
        disp = np.asarray(self.raw_displacements, float)
        n, dims = nodes.shape
        if disp.size not in (n * 2, n * 3):
            raise ValueError(f"displacements length must be n*2 or n*3, got {disp.size}")
        if disp.size == n * 2:
            disp = disp.reshape(n, 2)
            disp = np.hstack([disp, np.zeros((n, 1))])
        else:
            disp = disp.reshape(n, 3)
        self.displacements = disp

        # --- bc_flags sanity check & pad to 3 ---
        for nid, flags in list(self.bc_flags.items()):
            if len(flags) == 2:
                self.bc_flags[nid] = (flags[0], flags[1], False)
            elif len(flags) != 3:
                raise ValueError(f"bc_flags at node {nid} must be a 2- or 3-tuple of bools")
