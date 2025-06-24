"""
mesh_data.py

Core data structures for MiniFEA renderer: MeshData holds raw node/element arrays,
performs normalization to 3D, and prepares flat buffers for GPU upload.
"""
import numpy as np

class MeshData:
    """
    Stores raw mesh and field data and provides normalized buffers for rendering.

    Attributes:
        nodes (np.ndarray): Original node coordinates, shape (n_nodes, dim).
        elems (np.ndarray): Element connectivity, shape (n_elems, nodes_per_elem).
        disp (np.ndarray): Displacements per node, shape (n_nodes, dim) or None.
        field (np.ndarray): Scalar field per node or element, shape (n_nodes,) or (n_elems,) or None.
        _nodes3d (np.ndarray): Internal 3D node positions, shape (n_nodes, 3).
        node_buffer (np.ndarray): Flattened float32 buffer of node positions.
        disp_buffer (np.ndarray): Flattened float32 buffer of displacements (if provided).
        index_buffer (np.ndarray): Flattened int32 buffer of element connectivity.
    """

    def __init__(self, nodes, elems, disp=None, field=None):
        """
        Initialize MeshData.

        Args:
            nodes: array-like of shape (n_nodes, 2) or (n_nodes, 3).
            elems: array-like of ints, shape (n_elems, nodes_per_elem).
            disp: optional displacements, same shape as nodes.
            field: optional scalar field per node or per element.
        """
        self.nodes = np.asarray(nodes, dtype=float)
        self.elems = np.asarray(elems, dtype=int)
        self.disp = np.asarray(disp, dtype=float) if disp is not None else None
        self.field = np.asarray(field, dtype=float) if field is not None else None

        # Normalize all coordinate arrays to 3D
        self._nodes3d = self._normalize_to_3d(self.nodes)
        if self.disp is not None:
            disp3 = self._normalize_to_3d(self.disp)
        else:
            disp3 = None

        # Prepare GPU-friendly buffers
        self.node_buffer = self._nodes3d.flatten().astype(np.float32)
        self.disp_buffer = disp3.flatten().astype(np.float32) if disp3 is not None else None
        self.index_buffer = self.elems.flatten().astype(np.int32)

    def _normalize_to_3d(self, arr):
        """
        Pad 2D coordinates with zeros to make 3D arrays.

        Args:
            arr: np.ndarray of shape (n_nodes, 2) or (n_nodes, 3)

        Returns:
            np.ndarray of shape (n_nodes, 3)
        """
        arr = np.asarray(arr, dtype=float)
        if arr.ndim != 2 or arr.shape[1] not in (2, 3):
            raise ValueError(f"Expected array of shape (n,2) or (n,3), got {arr.shape}")
        if arr.shape[1] == 2:
            zeros = np.zeros((arr.shape[0], 1), dtype=arr.dtype)
            return np.hstack([arr, zeros])
        return arr

    def update_displacements(self, disp):
        """
        Update the displacement buffer with new values.

        Args:
            disp: array-like of shape (n_nodes, 2) or (n_nodes, 3)
        """
        disp3 = self._normalize_to_3d(disp)
        self.disp = disp3
        self.disp_buffer = disp3.flatten().astype(np.float32)

    def update_field(self, field):
        """
        Update the scalar field buffer with new values.

        Args:
            field: array-like of shape (n_nodes,) or (n_elems,)
        """
        self.field = np.asarray(field, dtype=float)
