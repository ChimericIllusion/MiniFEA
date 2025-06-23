# colourmaps.py
import numpy as np
from vispy.color import get_colormap as _builtin_map, Colormap

def viridis():
    """VisPy’s built-in Viridis."""
    return _builtin_map('viridis')

def plasma():
    """VisPy’s built-in Plasma."""
    return _builtin_map('plasma')

def bwr():
    """VisPy’s built-in Blue-White-Red."""
    return _builtin_map('bwr')

def custom_diverging():
    """A bespoke blue→white→red diverging map."""
    colors = np.array([
        [0.0, 0.0, 0.5, 1.0],  # deep blue
        [1.0, 1.0, 1.0, 1.0],  # white
        [0.5, 0.0, 0.0, 1.0],  # dark red
    ], dtype=np.float32)
    return Colormap(colors, controls=[0.0, 0.5, 1.0])

# Registry
_COLORS = {
    'viridis':          viridis,
    'plasma':           plasma,
    'bwr':              bwr,
    'custom_diverging': custom_diverging,
}

def available_maps():
    """List of supported colormap names."""
    return list(_COLORS.keys())

def get_colormap(name):
    """
    Return a fresh Colormap instance for `name`.
    Raises ValueError if name not in registry.
    """
    try:
        return _COLORS[name]()
    except KeyError:
        raise ValueError(f"Unknown colormap '{name}'. Valid options: {available_maps()!r}")
