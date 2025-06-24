# file: miniFEA/visualiser3d.py

import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Visualiser3D:
    def __init__(self, nodes, elements, displacements=None, field=None):
        """
        nodes: (N,3) array of XYZ coords
        elements: (M,2) array of node indices
        displacements: (N,3) array or None
        field: (M,) element scalar field (e.g. axial stress) or None
        """
        self.nodes0 = np.asarray(nodes, float)
        self.els = np.asarray(elements, int)
        self.u = np.zeros_like(self.nodes0) if displacements is None else displacements
        self.field = field
        self.scale = 1.0
        self.rot = [20, 30, 0]  # Euler angles

    def start(self, w=800, h=600):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(w, h)
        glutCreateWindow(b"MiniFEA 3D Viewer")
        glEnable(GL_DEPTH_TEST)
        glClearColor(0,0,0,1)
        glutDisplayFunc(self._draw)
        glutReshapeFunc(self._reshape)
        glutKeyboardFunc(self._key)
        glutIdleFunc(glutPostRedisplay)
        glutMainLoop()

    def _reshape(self, w, h):
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def _key(self, key, x, y):
        if key == b'+':       self.scale *= 1.1
        elif key == b'-':     self.scale /= 1.1
        elif key == b'd':     self.u *= 1.1
        elif key == b'r':     self.u[:] = 0
        elif key == b'\x1b':  sys.exit(0)
        glutPostRedisplay()

    def _draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # camera back and rotate
        glTranslatef(0, 0, -3.0)
        glScalef(self.scale, self.scale, self.scale)
        glRotatef(self.rot[0],1,0,0)
        glRotatef(self.rot[1],0,1,0)
        glRotatef(self.rot[2],0,0,1)

        # draw elements
        glBegin(GL_LINES)
        for i,(n1,n2) in enumerate(self.els):
            p1 = self.nodes0[n1] + self.u[n1]
            p2 = self.nodes0[n2] + self.u[n2]
            if self.field is not None:
                # map scalar to colour (blue→red)
                t = (self.field[i] - self.field.min())/(self.field.ptp()+1e-8)
                glColor3f(t, 0, 1-t)
            else:
                glColor3f(1,1,1)
            glVertex3fv(p1)
            glVertex3fv(p2)
        glEnd()
        glutSwapBuffers()

