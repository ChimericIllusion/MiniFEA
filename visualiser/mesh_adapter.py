# visualiser/mesh_adapter.py

from dataclasses import dataclass, field
import numpy as np
from typing import List, Tuple, Dict, Union

@dataclass
class VisualData:
    """
    Container for FEA visualization data. Accepts 2D or 3D input and
    normalizes everything to 3D for downstream viewers.

    Attributes:
        raw_nodes:       ndarray, shape (n_nodes, 2) or (n_nodes, 3)
        elements:        list of (i, j) node-index tuples, zero-based
        raw_displacements:
                         ndarray, flat length n_nodes*2 or n_nodes*3
        scalar_field:    ndarray, length = n_elements
        bc_flags:        dict mapping node_id -> (ux_fixed, uy_fixed[, uz_fixed])
    """
    raw_nodes: np.ndarray
    elements: List[Tuple[int, int]]
    raw_displacements: np.ndarray
    scalar_field: np.ndarray
    bc_flags: Dict[int, Tuple[bool, ...]]

    # populated in __post_init__
    nodes: np.ndarray = field(init=False)
    displacements: np.ndarray = field(init=False)
    bc_flags3: Dict[int, Tuple[bool, bool, bool]] = field(init=False)

    def __post_init__(self):
        # --- Validate raw_nodes and pad to 3D ---
        nodes = np.asarray(self.raw_nodes, dtype=float)
        if nodes.ndim != 2 or nodes.shape[1] not in (2, 3):
            raise ValueError(f"raw_nodes must be shape (n,2) or (n,3), got {nodes.shape}")
        if nodes.shape[1] == 2:
            zcol = np.zeros((nodes.shape[0], 1), dtype=float)
            nodes = np.hstack([nodes, zcol])
        self.nodes = nodes
        n_nodes = nodes.shape[0]

        # --- Validate and reshape displacements to (n_nodes, 3) ---
        disp = np.asarray(self.raw_displacements, dtype=float)
        if disp.size not in (n_nodes * 2, n_nodes * 3):
            raise ValueError(f"raw_displacements length must be n*2 or n*3, got {disp.size}")
        if disp.size == n_nodes * 2:
            disp = disp.reshape(n_nodes, 2)
            disp = np.hstack([disp, np.zeros((n_nodes, 1), dtype=float)])
        else:
            disp = disp.reshape(n_nodes, 3)
        self.displacements = disp

        # --- Validate elements vs scalar_field length ---
        n_elems = len(self.elements)
        if self.scalar_field.ndim != 1 or self.scalar_field.size != n_elems:
            raise ValueError(
                f"scalar_field length must equal number of elements ({n_elems}), got {self.scalar_field.size}"
            )

        # --- Normalize bc_flags to 3-tuples, leave missing as (False,False,False) ---
        bc3: Dict[int, Tuple[bool, bool, bool]] = {}
        for nid in range(n_nodes):
            flags = self.bc_flags.get(nid, (False, False))
            if len(flags) == 2:
                bc3[nid] = (flags[0], flags[1], False)
            elif len(flags) == 3:
                bc3[nid] = flags
            else:
                raise ValueError(f"bc_flags[{nid}] must be 2- or 3-tuple, got {flags!r}")
        # Overwrite original bc_flags so downstream viewers always see 3-tuples
        self.bc_flags = bc3
        self.bc_flags3 = bc3
