#Visualising
from dataclasses import dataclass
import numpy as np
from typing import List, Tuple, Dict

@dataclass
class VisualData:
    nodes: np.ndarray                    # (n_nodes, 2)
    elements: List[Tuple[int, int]]     # [(n1, n2), ...]
    displacements: np.ndarray           # (n_nodes * 2,)
    scalar_field: np.ndarray            # (n_elements,)
    bc_flags: Dict[int, Tuple[bool, bool]]  # {node_id: (ux_fixed, uy_fixed)}
