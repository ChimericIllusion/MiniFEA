"""
input_controller.py

Maps keyboard and mouse events to camera, view manager, scene, and shader actions.
"""
import numpy as np
class InputController:
    """
    Handles user input and dispatches to renderer components.
    """
    def __init__(self,
                 camera,
                 view_manager,
                 scene,
                 shader,
                 exit_callback=None,
                 key_map=None,
                 fit_center=None,
                 fit_radius=None):
        """
        Args:
            camera: Camera instance (orbit/pan/zoom/reset).
            view_manager: ViewManager instance (goTo presets).
            scene: Scene instance (toggle_deformed_visibility).
            shader: ShaderManager instance (cycle_colormap).
            exit_callback: optional callable to invoke on exit (Esc).
            key_map: dict mapping key strings to view names, e.g. {'1':'Top', ...}.
        """
        self.camera      = camera
        self.views       = view_manager
        self.scene       = scene
        self.shader      = shader
        self.exit        = exit_callback or (lambda: None)
        # default keys for view presets
        self.key_map     = key_map or {'1':'Top', '2':'Front', '3':'Side', '4':'Iso'}
        self.fit_center = fit_center
        self.fit_radius = fit_radius

    def on_key(self, key, modifiers=None):
        """
        Call in response to a key press.

        Args:
            key (str): the key identifier (e.g. '1','r','D','Escape').
            modifiers: optional set of modifier keys.
        """
        k = key.decode('utf-8')
        # handle Escape key
        if k == '\x1b' or k.lower() == 'escape':
            return self.exit()
        if k in self.key_map:
            # switch to named view
            name = self.key_map[k]
            self.views.goTo(name)
            self.camera.fit(self.fit_center, self.fit_radius)
        elif k == 'r':
            # reset camera orientation
            self.camera.reset()
            # recenter on mesh centroid
            self.camera.fit(self.fit_center, self.fit_radius)
        elif k == 'd':
            # toggle deformed overlay
            self.scene.toggle_deformed_visibility()
        elif k == 'c':
            # cycle through colormaps
            self.shader.cycle_colormap()
        elif k == 'escape':
            # exit application
            self.exit()
    
    def on_mouse_drag(self, dx, dy, button):
        """
        Call on mouse drag.

        Args:
            dx, dy (float): drag deltas in pixels.
            button (str): 'left' or 'right' (or other).
        """
        if button == 'left':
            self.camera.orbit(dx, dy)
        else:
            # any other button (e.g. right or shift+drag) pans
            self.camera.pan(dx, dy)

    def on_scroll(self, delta):
        """
        Call on scroll wheel movement.

        Args:
            delta (float): positive for scroll up, negative for down.
        """
        self.camera.zoom(delta)
