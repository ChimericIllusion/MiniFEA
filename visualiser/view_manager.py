"""
view_manager.py

Registry for camera view presets: map names to camera configurations and apply them.
"""
import numpy as np

class ViewManager:
    """
    Holds named camera presets and applies them on demand.
    """
    def __init__(self, camera):
        """
        Args:
            camera: instance of Camera to control.
        """
        self.camera = camera
        self._presets = {}  # name -> config dict

    def add(self, name, config):
        """
        Register a new view preset.

        Args:
            name (str): preset identifier (e.g. 'Top').
            config (dict): camera parameters:
                {
                  'position': array-like (3,),
                  'target': array-like (3,),
                  'up': array-like (3,),
                  'mode': 'persp'|'ortho',
                  'fov': float,
                  'ortho_size': float,
                  'near': float,
                  'far': float
                }
        """
        # ensure arrays are numpy
        cfg = config.copy()
        cfg['position'] = np.asarray(cfg['position'], dtype=float)
        cfg['target']   = np.asarray(cfg['target'], dtype=float)
        cfg['up']       = np.asarray(cfg['up'], dtype=float)
        self._presets[name] = cfg

    def goTo(self, name):  # noqa: N802
        """
        Apply a registered preset by name.

        Args:
            name (str): key of preset to activate.
        Raises:
            KeyError if preset not found.
        """
        if name not in self._presets:
            raise KeyError(f"View preset '{name}' not registered")
        cfg = self._presets[name]
        # apply to camera
        cam = self.camera
        cam.position   = cfg['position'].copy()
        cam.target     = cfg['target'].copy()
        cam.up         = cfg['up'].copy()
        cam.mode       = cfg['mode']
        cam.fov        = cfg['fov']
        cam.ortho_size = cfg['ortho_size']
        cam.near       = cfg['near']
        cam.far        = cfg['far']
        # recompute spherical coords
        offset = cam.position - cam.target
        cam._radius = np.linalg.norm(offset)
        # prevent gimbal lock
        cam._theta = np.arctan2(offset[2], offset[0])
        cam._phi   = np.arccos(offset[1] / cam._radius)

    @property
    def presets(self):
        """
        Return list of registered preset names.
        """
        return list(self._presets.keys())

    @property
    def current(self):
        """
        Return the name of the last-applied preset, if tracked. Optional.
        """
        # Could track last name; for now return None
        return None
