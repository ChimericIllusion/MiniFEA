"""
camera.py

Camera for MiniFEA renderer: supports orbit, pan, zoom, reset, and provides view matrix.
"""
import numpy as np

def normalize(v):
    return v / np.linalg.norm(v)

def look_at(eye, target, up):
    """
    Create a right-handed look-at view matrix.
    """
    f = normalize(target - eye)
    s = normalize(np.cross(f, up))
    u = np.cross(s, f)
    M = np.eye(4, dtype=np.float32)
    M[0, :3] = s
    M[1, :3] = u
    M[2, :3] = -f
    M[:3, 3] = -M[:3, :3] @ eye
    return M

class Camera:
    """
    Arcball-style camera around a target point, with perspective or ortho projection.
    """
    def __init__(self,
                 position=(1.5, 1.5, 1.5),
                 target=(0.0, 0.0, 0.0),
                 up=(0.0, 1.0, 0.0),
                 mode='persp',
                 fov=np.radians(60.0),
                 ortho_size=1.0,
                 near=0.1,
                 far=100.0):
        """
        Args:
            position: initial camera eye position (x,y,z)
            target: point to look at
            up: world up vector
            mode: 'persp' or 'ortho'
            fov: vertical field of view in radians (for persp)
            ortho_size: half-height of view volume (for ortho)
            near, far: clipping planes
        """
        self._init_cfg = dict(
            position=np.array(position, dtype=float),
            target=np.array(target, dtype=float),
            up=np.array(up, dtype=float),
            mode=mode,
            fov=fov,
            ortho_size=ortho_size,
            near=near,
            far=far
        )
        self.reset()

    def reset(self):
        """
        Restore camera to initial configuration.
        """
        cfg = self._init_cfg
        self.position = cfg['position'].copy()
        self.target   = cfg['target'].copy()
        self.up       = cfg['up'].copy()
        self.mode     = cfg['mode']
        self.fov      = cfg['fov']
        self.ortho_size = cfg['ortho_size']
        self.near     = cfg['near']
        self.far      = cfg['far']

        # Spherical coords for orbit control
        offset = self.position - self.target
        self._radius = np.linalg.norm(offset)
        # avoid gimbal: compute angles
        self._theta = np.arctan2(offset[2], offset[0])   # around y-axis
        self._phi   = np.arccos(offset[1] / self._radius)  # polar

    def orbit(self, dx, dy, sensitivity=0.005):
        """
        Orbit the camera around the target by screen deltas.
        dx, dy in pixels; sensitivity scales movement.
        """
        self._theta += dx * sensitivity
        self._phi   = np.clip(self._phi + dy * sensitivity, 0.01, np.pi - 0.01)
        # recompute position
        r = self._radius
        self.position = self.target + np.array([
            r * np.sin(self._phi) * np.cos(self._theta),
            r * np.cos(self._phi),
            r * np.sin(self._phi) * np.sin(self._theta)
        ], dtype=float)

    def pan(self, dx, dy, sensitivity=0.002):
        """
        Pan camera and target in the view plane.
        """
        # compute right and up in world space
        view_dir = normalize(self.target - self.position)
        right = normalize(np.cross(view_dir, self.up))
        up   = normalize(np.cross(right, view_dir))
        shift = (-right * dx + up * dy) * sensitivity * self._radius
        self.position += shift
        self.target   += shift

    def zoom(self, delta, sensitivity=0.1):
        """
        Zoom camera in/out. For persp: move eye along view dir.
        For ortho: adjust ortho_size.
        """
        if self.mode == 'persp':
            view_dir = normalize(self.target - self.position)
            self._radius = max(1e-3, self._radius * (1.0 - delta * sensitivity))
            self.position = self.target - view_dir * self._radius
        else:
            self.ortho_size = max(1e-3, self.ortho_size * (1.0 - delta * sensitivity))

    def get_view_matrix(self):
        """
        Return 4x4 view matrix as float32 ndarray.
        """
        return look_at(self.position, self.target, self.up)
    def fit(self, center: np.ndarray, radius: float, scale: float = 3.0):
        """
        Center on 'center' and back off so the entire
        bounding sphere of 'radius' is visible.
        """
        # 1) update target & radius
        self.target = center.copy()
        self._radius = radius * scale

        # 2) recompute position using existing angles _theta/_phi
        self.position = self.target + np.array([
            self._radius * np.sin(self._phi) * np.cos(self._theta),
            self._radius * np.cos(self._phi),
            self._radius * np.sin(self._phi) * np.sin(self._theta),
        ], dtype=float)

        # 3) now recompute spherical coords so orbit stays in sync
        offset = self.position - self.target
        self._radius = np.linalg.norm(offset)
        self._theta  = np.arctan2(offset[2], offset[0])
        self._phi    = np.arccos(offset[1] / self._radius)