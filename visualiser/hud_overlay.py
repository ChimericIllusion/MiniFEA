"""
hud_overlay.py

Renders on-screen HUD elements: current view, FPS, deformation state, colormap legend,
—and now also a fixed‐size 3-axis gizmo in the lower‐left corner.
"""
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
import glm

# **NEW IMPORT**
from .Gizmo import Gizmo

class HUDOverlay:
    """
    Draws 2D HUD elements in an orthographic overlay,
    plus a 3-axis orientation gizmo.
    """
    def __init__(self, view_manager, shader_manager, scene, fps_callback=None):
        """
        Args:
            view_manager: ViewManager instance
            shader_manager: ShaderManager instance
            scene: Scene instance
            fps_callback: callable returning current FPS
        """
        self.views        = view_manager
        self.shader       = shader_manager
        self.scene        = scene
        self.fps_callback = fps_callback or (lambda: 0)

        # --- NEW: setup 3-axis gizmo ---
        # Assumes your ViewManager holds a reference to the camera:
        self.camera = self.views.camera  
        self.gizmo = Gizmo()
        self.gizmo.init(
            arrowLength=0.1,   # world‐space length in NDC
            arrowRadius=0.005  # thickness
        )
        # Projection for gizmo is identity → direct NDC
        self._proj_ndc = glm.mat4(1.0)

    def _draw_text(self, x, y, text):
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    def draw(self, width, height):
        # --- 2D HUD setup ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)

        # Text info
        current_view = self.views.current or 'Custom'
        fps          = self.fps_callback()
        cmap_idx     = self.shader.current if self.shader.tex_ids else -1
        deform       = 'On' if self.scene.deformed_visible else 'Off'

        margin = 10
        line_h = 20
        lines = [
            f"View: {current_view}",
            f"FPS: {fps:.1f}",
            f"Deformation: {deform}",
            f"Colormap: {cmap_idx}"
        ]
        for i, text in enumerate(lines):
            self._draw_text(margin, height - margin - line_h * i, text)

        # Colormap swatch
        if self.shader.tex_ids:
            sw = 20
            glBindTexture(GL_TEXTURE_1D, self.shader.tex_ids[cmap_idx])
            glBegin(GL_QUADS)
            glTexCoord1f(0.0); glVertex2f(width - margin - sw, height - margin - sw)
            glTexCoord1f(1.0); glVertex2f(width - margin,     height - margin - sw)
            glTexCoord1f(1.0); glVertex2f(width - margin,     height - margin)
            glTexCoord1f(0.0); glVertex2f(width - margin - sw, height - margin)
            glEnd()
            glBindTexture(GL_TEXTURE_1D, 0)

        # --- NOW DRAW THE 3-AXIS GIZMO ---
        # Keep gizmo on top
        glDepthFunc(GL_LEQUAL)
        glDepthMask(GL_FALSE)

        # Camera orientation as a glm.quat
        cam_rot = self.camera.orientation_quat()
        self.gizmo.drawOverlay(cam_rot, self._proj_ndc)

        # Restore depth‐write for any further draws
        glDepthMask(GL_TRUE)

        # --- restore 2D HUD state ---
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()                     # MODELVIEW
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()                     # PROJECTION
        glMatrixMode(GL_MODELVIEW)
