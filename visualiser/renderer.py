"""
renderer.py

Core render loop: initializes GL context, sets up callbacks, and drives continuous rendering.
"""
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

class Renderer:
    """
    Ties together Scene, Camera, ProjectionManager, InputController, HUDOverlay,
    and defers ShaderManager creation until after the GL context exists.
    """
    def __init__(self,
                 scene,
                 vert_path,
                 frag_path,
                 colormaps,
                 camera,
                 proj_mgr,
                 hud,
                 input_ctrl,
                 width=800,
                 height=600,
                 title="MiniFEA Viewer"):
        self.scene       = scene
        # Shader parameters (deferred)
        self.vert_path   = vert_path
        self.frag_path   = frag_path
        self.colormaps   = colormaps
        self.shader      = None
        self.camera      = camera
        self.proj_mgr    = proj_mgr
        self.hud         = hud
        self.input       = input_ctrl
        self.width       = width
        self.height      = height
        self.title       = title.encode('utf-8')
        self._mouse_btn  = None
        self._last_x     = 0
        self._last_y     = 0

    def _reshape(self, w, h):
        self.width  = w
        self.height = max(1, h)
        glViewport(0, 0, self.width, self.height)

    def _display(self):
        # 0) Clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        aspect = self.width / self.height

        # 1) Compute matrices
        P   = self.proj_mgr.get_proj_matrix(self.camera, aspect)
        V   = self.camera.get_view_matrix()
        MVP = P @ V

        # 2) Draw wireframe via shader
        self.shader.use(MVP.astype(np.float32))
        # ensure fixed-function matrices are identity so shader MVP is only source
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.scene.draw(self.shader)

        # 3) Draw debug spheres at nodes under the same P & V
        glUseProgram(0)
        # Projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadMatrixf(P.T)
        # View
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(V.T)

        from OpenGL.GLUT import glutSolidSphere
        glDisable(GL_DEPTH_TEST)
        glColor3f(1.0, 0.0, 0.0)
        radius = 0.02
        for v in self.scene.mesh_data._nodes3d:
            glPushMatrix()
            glTranslatef(v[0], v[1], v[2])
            glutSolidSphere(radius, 12, 12)
            glPopMatrix()
        glEnable(GL_DEPTH_TEST)

        # Restore matrices
        glPopMatrix()                     # MODELVIEW
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()                     # PROJECTION
        glMatrixMode(GL_MODELVIEW)

        # 4) Re-bind shader & draw HUD (which now also draws the 3-axis gizmo)
        self.shader.use(MVP.astype(np.float32))
        self.hud.draw(self.width, self.height)

        # 5) Swap
        glutSwapBuffers()

    def _on_keyboard(self, key, x, y):
        k = key.decode('utf-8')
        self.input.on_key(k)

    def _on_mouse(self, button, state, x, y):
        if state == GLUT_DOWN:
            self._mouse_btn = button
        else:
            self._mouse_btn = None
        self._last_x, self._last_y = x, y

    def _on_motion(self, x, y):
        dx = x - self._last_x
        dy = y - self._last_y
        btn = 'left' if self._mouse_btn == GLUT_LEFT_BUTTON else 'right'
        self.input.on_mouse_drag(dx, dy, btn)
        self._last_x, self._last_y = x, y

    def _on_wheel(self, wheel, direction, x, y):
        self.input.on_scroll(direction)

    def start(self):
        # 1) Initialize GLUT window & context
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(self.title)
        glutFullScreen() 
        # 2) Now that the context exists, compile the shaders
        from visualiser.shader import ShaderManager
        self.shader = ShaderManager(
            vert_path=self.vert_path,
            frag_path=self.frag_path,
            colormaps=self.colormaps
        )

        # 2b) Inject the real shader into HUD and InputController
        self.hud.shader = self.shader
        self.input.shader = self.shader

        # 3) Upload scene buffers
        self.scene.initialize_gl()

        # 4) Set GL state
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)

        # 5) Register callbacks
        glutReshapeFunc(self._reshape)
        glutDisplayFunc(self._display)
        glutIdleFunc(self._display)
        glutKeyboardFunc(self._on_keyboard)
        glutMouseFunc(self._on_mouse)
        glutMotionFunc(self._on_motion)
        try:
            glutMouseWheelFunc(self._on_wheel)
        except AttributeError:
            pass

        # 6) Enter the main loop
        glutMainLoop()
