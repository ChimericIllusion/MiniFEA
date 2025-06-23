# visualiser/viewer_app.py
from vispy import app
from .render2d import TrussViewer

def launch_viewer(data, scale=1.0, field_name='scalar', cmap='bwr'):
    """
    Consistently pass `cmap` through to the TrussViewer.
    """
    viewer = TrussViewer(
        data,
        scale=scale,
        field_name=field_name,
        cmap=cmap
    )
    app.run()
    