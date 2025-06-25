"""
input_controller.py

Maps keyboard and mouse events to camera, view manager, scene, and shader actions.
"""
import numpy as np
from OpenGL.GLUT import glutLeaveMainLoop
import sys
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
        self.camera      = camera
        self.views       = view_manager
        self.scene       = scene
        self.shader      = shader
        self.exit        = exit_callback or (lambda: None)
        self.key_map     = key_map or {'1': 'Top', '2': 'Front', '3': 'Side', '4': 'Iso'}
        self.fit_center  = fit_center
        self.fit_radius  = fit_radius

    def on_key(self, key, x=None, y=None):
        # Normalize key to str
        k = key.decode('utf-8') if isinstance(key, bytes) else key

        # Exit on Escape
        if k == '\x1b':
            # tell GLUT to exit its main loop
            glutLeaveMainLoop()
            return

        # Snap to view presets
        if k in self.key_map:
            preset = self.key_map[k]
            self.views.goTo(preset)
            # Re-fit to frame the entire model
            if self.fit_center is not None and self.fit_radius is not None:
                self.camera.fit(self.fit_center, self.fit_radius)
            return

        # Reset camera
        if k.lower() == 'r':
            self.camera.reset()
            if self.fit_center is not None and self.fit_radius is not None:
                self.camera.fit(self.fit_center, self.fit_radius)
            return

        # Toggle deformation overlay
        if k.lower() == 'd':
            self.scene.toggle_deformed_visibility()
            return

        # Cycle colormap
        if k.lower() == 'c':
            if self.shader:
                self.shader.cycle_colormap()
            return
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
