"""
hud_overlay.py

Renders on-screen HUD elements: current view, FPS, deformation state, and colormap legend.
"""
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18

class HUDOverlay:
    """
    Draws 2D HUD elements in an orthographic overlay.
    """
    def __init__(self, view_manager, shader_manager, scene, fps_callback=None):
        """
        Args:
            view_manager: ViewManager instance
            shader_manager: ShaderManager instance
            scene: Scene instance
            fps_callback: callable returning current FPS
        """
        self.views = view_manager
        self.shader = shader_manager
        self.scene = scene
        self.fps_callback = fps_callback or (lambda: 0)

    def _draw_text(self, x, y, text):
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    def draw(self, width, height):
        # Setup orthographic projection for HUD
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

        # Retrieve HUD data
        current_view = self.views.current or 'Custom'
        fps = self.fps_callback()
        cmap_idx = self.shader.current if self.shader.tex_ids else -1
        deform = 'On' if self.scene.deformed_visible else 'Off'

        # Text placement
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

        # Restore matrices & depth test
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
