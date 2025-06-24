import numpy as np
from visualiser.mesh_data import MeshData

def test_normalize_2d_and_3d():
    nodes2 = [[0,0],[1,2]]
    m2 = MeshData(nodes2, elems=[[0,1]])
    assert m2._nodes3d.shape == (2,3)
    nodes3 = [[0,0,0],[1,2,3]]
    m3 = MeshData(nodes3, elems=[[0,1]])
    assert np.allclose(m3._nodes3d, nodes3)
