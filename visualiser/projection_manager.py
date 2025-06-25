"""
projection_manager.py

ProjectionManager for MiniFEA renderer: builds perspective and orthographic projection matrices.
"""
import numpy as np

class ProjectionManager:
    """
    Provides projection matrices given a Camera and viewport aspect ratio.
    """
    def __init__(self):
        pass

    def get_proj_matrix(self, camera, aspect: float) -> np.ndarray:
        """
        Compute a 4x4 projection matrix based on the camera mode.

        Args:
            camera: instance of Camera with attributes:
                    - mode: 'persp' or 'ortho'
                    - fov: vertical field of view in radians (for persp)
                    - ortho_size: half-height of view volume (for ortho)
                    - near: near clipping plane distance
                    - far:  far clipping plane distance
            aspect: viewport width/height ratio

        Returns:
            4x4 numpy.ndarray of dtype float32
        """
        near = camera.near
        far  = camera.far

        if camera.mode == 'persp':
            f = 1.0 / np.tan(camera.fov / 2.0)
            M = np.zeros((4,4), dtype=np.float32)
            M[0,0] = f / aspect
            M[1,1] = f
            M[2,2] = (far + near) / (near - far)
            M[2,3] = (2 * far * near) / (near - far)
            M[3,2] = -1.0
            return M

        elif camera.mode == 'ortho':
            # ortho_size is half-height
            h = camera.ortho_size
            w = h * aspect
            # left, right, bottom, top
            l, r = -w, w
            b, t = -h, h
            M = np.zeros((4,4), dtype=np.float32)
            M[0,0] = 2.0 / (r - l)
            M[1,1] = 2.0 / (t - b)
            M[2,2] = -2.0 / (far - near)
            M[0,3] = -(r + l) / (r - l)
            M[1,3] = -(t + b) / (t - b)
            M[2,3] = -(far + near) / (far - near)
            M[3,3] = 1.0
            return M

        else:
            raise ValueError(f"Unknown camera mode '{camera.mode}'")
