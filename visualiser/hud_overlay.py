"""
hud_overlay.py

Renders on-screen HUD elements: current view, FPS, deformation state, colormap legend,
—and now also a fixed-size 3-axis gizmo in the lower-left corner.
"""
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18

class HUDOverlay:
    """
    Draws 2D HUD elements in an orthographic overlay,
    plus a 3-axis orientation gizmo via immediate-mode GL.
    """
    def __init__(self, view_manager, shader_manager, scene, fps_callback=None):
        self.views        = view_manager
        self.shader       = shader_manager
        self.scene        = scene
        self.fps_callback = fps_callback or (lambda: 0)
        self.camera       = self.views.camera  # assume has get_view_matrix()

    def _draw_text(self, x, y, text):
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    def _draw_gizmo(self):
        # 1) Setup identity NDC projection/modelview
        glMatrixMode(GL_PROJECTION)
        glPushMatrix(); glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix(); glLoadIdentity()

        # 2) Draw on top
        glDisable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glDepthMask(GL_FALSE)

        # 3) Move to lower-left corner
        glTranslatef(-0.9, -0.9, 0.0)

        # 4) Build rotation-only matrix from camera view
        V = self.camera.get_view_matrix().astype(np.float32)  # shape (4,4)
        R = V[:3, :3].T  # invert world→camera rotation by transpose
        M = np.eye(4, dtype=np.float32)
        M[:3, :3] = R
        # OpenGL expects column-major; numpy is row-major, so transpose
        glMultMatrixf(M.T.flatten())

        # 5) Draw axes lines
        size = 0.1
        glLineWidth(2.0)
        glBegin(GL_LINES)
        # X (red)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0); glVertex3f(size, 0, 0)
        # Y (green)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0); glVertex3f(0, size, 0)
        # Z (blue)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0); glVertex3f(0, 0, size)
        glEnd()

        # 6) Draw endpoints
        glPointSize(6.0)
        glBegin(GL_POINTS)
        glColor3f(1, 0, 0); glVertex3f(size, 0, 0)
        glColor3f(0, 1, 0); glVertex3f(0, size, 0)
        glColor3f(0, 0, 1); glVertex3f(0, 0, size)
        glEnd()

        # 7) Restore state
        glDepthMask(GL_TRUE)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()                       # MODELVIEW
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()                       # PROJECTION
        glMatrixMode(GL_MODELVIEW)

    def draw(self, width, height):
        # --- 2D HUD setup ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix(); glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix(); glLoadIdentity()

        glDisable(GL_DEPTH_TEST)

        # Text info
        current_view = self.views.current or 'Custom'
        fps          = self.fps_callback()
        cmap_idx     = self.shader.current if hasattr(self.shader, 'current') else -1
        deform       = 'On' if getattr(self.scene, 'deformed_visible', False) else 'Off'

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
        if getattr(self.shader, 'tex_ids', None):
            sw = 20
            glBindTexture(GL_TEXTURE_1D, self.shader.tex_ids[cmap_idx])
            glBegin(GL_QUADS)
            glTexCoord1f(0.0); glVertex2f(width - margin - sw, height - margin - sw)
            glTexCoord1f(1.0); glVertex2f(width - margin,       height - margin - sw)
            glTexCoord1f(1.0); glVertex2f(width - margin,       height - margin)
            glTexCoord1f(0.0); glVertex2f(width - margin - sw, height - margin)
            glEnd()
            glBindTexture(GL_TEXTURE_1D, 0)

        # --- Draw the gizmo ---
        self._draw_gizmo()

        # --- restore 2D HUD state ---
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()                     # MODELVIEW
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()                     # PROJECTION
        glMatrixMode(GL_MODELVIEW)
