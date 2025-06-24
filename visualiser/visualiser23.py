import sys, numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Visualiser23:
    """
    Combined 2D (orthographic) & 3D (perspective) FEA viewer.
    Controls:
      m : toggle 2D/3D mode
      + / - : zoom in/out
      d / r : deform / reset
      Esc   : exit
    """
    def __init__(self, nodes, elements, displacements=None, field=None, scale=1.0):
        self.nodes0 = np.asarray(nodes, float)
        self.els    = np.asarray(elements, int)
        self.u      = np.zeros_like(self.nodes0) if displacements is None else displacements
        self.field  = np.asarray(field, float) if field is not None else None
        self.scale  = scale
        self.mode3d = True
        self.rot    = [20, 30, 0]

    def start(self, w=800, h=600):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(w, h)
        glutCreateWindow(b"MiniFEA 2D/3D Viewer")
        glEnable(GL_DEPTH_TEST)
        glClearColor(0,0,0,1)
        glutDisplayFunc(self._draw)
        glutReshapeFunc(self._reshape)
        glutKeyboardFunc(self._key)
        glutIdleFunc(glutPostRedisplay)
        glutMainLoop()

    def _reshape(self, w, h):
        self.w, self.h = w, h
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.mode3d:
            gluPerspective(45, w/h, 0.1, 1000.0)
        else:
            # orthographic XY
            asp = w/h
            L = 2 * self.scale
            glOrtho(-L*asp, L*asp, -L, L, -10, 10)
        glMatrixMode(GL_MODELVIEW)

    def _key(self, key, x, y):
        if key == b'm':
            self.mode3d = not self.mode3d
            self._reshape(self.w, self.h)
        elif key == b'+':
            self.scale *= 1.1
        elif key == b'-':
            self.scale /= 1.1
        elif key == b'd':
            self.u *= 1.1
        elif key == b'r':
            self.u[:] = 0
        elif key == b'\x1b':
            sys.exit(0)
        glutPostRedisplay()

    def _draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if self.mode3d:
            glTranslatef(0, 0, -3.0)
            glScalef(self.scale, self.scale, self.scale)
            glRotatef(self.rot[0], 1, 0, 0)
            glRotatef(self.rot[1], 0, 1, 0)
            glRotatef(self.rot[2], 0, 0, 1)
        else:
            # flat 2D: ignore Z, center and scale
            glScalef(self.scale, self.scale, 1)

        glBegin(GL_LINES)
        for i, (n1, n2) in enumerate(self.els):
            p1 = self.nodes0[n1] + self.u[n1]
            p2 = self.nodes0[n2] + self.u[n2]
            if not self.mode3d:
                p1 = p1[:2]
                p2 = p2[:2]
            if self.field is not None:
                t = (self.field[i] - self.field.min()) / (self.field.ptp() + 1e-8)
                glColor3f(t, 0, 1 - t)
            else:
                glColor3f(1, 1, 1)
            if self.mode3d:
                glVertex3fv(p1)
                glVertex3fv(p2)
            else:
                glVertex3f(p1[0], p1[1], 0)
                glVertex3f(p2[0], p2[1], 0)
        glEnd()
        glutSwapBuffers()
