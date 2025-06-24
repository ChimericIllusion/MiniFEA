# scene.py

"""
scene.py

Uploads MeshData into GPU buffers and issues draw calls for undeformed
and deformed meshes.
"""
from OpenGL.GL import *
import numpy as np

class Scene:
    """
    Wraps MeshData for rendering: creates VBO/EBOs, updates buffers, and draws.
    """
    def __init__(self, mesh_data):
        """
        Args:
            mesh_data: instance of MeshData containing node_buffer,
                       disp_buffer (optional), index_buffer.
        """
        self.mesh_data = mesh_data
        self.deformed_visible = False

        # Buffer handles (will be created in initialize_gl)
        self.vbo_nodes = None
        self.vbo_disp  = None
        self.ebo       = None

    def initialize_gl(self):
        """
        Generate and upload all VBO/EBO buffers to the GPU.
        Must be called after an OpenGL context is active.
        """
        # Generate buffers
        self.vbo_nodes = glGenBuffers(1)
        if self.mesh_data.disp_buffer is not None:
            self.vbo_disp = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        # Upload static node positions
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_nodes)
        glBufferData(GL_ARRAY_BUFFER,
                     self.mesh_data.node_buffer.nbytes,
                     self.mesh_data.node_buffer,
                     GL_STATIC_DRAW)

        # Upload dynamic displacements (if present)
        if self.vbo_disp is not None:
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_disp)
            glBufferData(GL_ARRAY_BUFFER,
                         self.mesh_data.disp_buffer.nbytes,
                         self.mesh_data.disp_buffer,
                         GL_DYNAMIC_DRAW)

        # Upload element indices
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     self.mesh_data.index_buffer.nbytes,
                     self.mesh_data.index_buffer,
                     GL_STATIC_DRAW)

        # Unbind for cleanliness
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def update_displacements(self, new_disp_buffer):
        """
        Re-upload the disp_buffer to GPU (for dynamic draws).

        Args:
            new_disp_buffer (np.ndarray): flattened float32 displacement array.
        """
        if self.vbo_disp is None:
            raise RuntimeError("Displacement buffer not initialized")
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_disp)
        # Orphan the old buffer
        glBufferData(GL_ARRAY_BUFFER,
                     new_disp_buffer.nbytes,
                     None,
                     GL_DYNAMIC_DRAW)
        # Upload new data
        glBufferSubData(GL_ARRAY_BUFFER,
                        0,
                        new_disp_buffer.nbytes,
                        new_disp_buffer)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def toggle_deformed_visibility(self):
        """Flip visibility state for deformed mesh overlay."""
        self.deformed_visible = not self.deformed_visible

    def draw(self, shader):
        """
        Draw undeformed mesh lines and, if enabled, deformed overlay.

        Args:
            shader: active line shader with known attribute locations.
                    Must have `attrib_pos` for vertex position.
        """
        # Bind shader and any uniforms outside
        # Draw undeformed
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_nodes)
        glEnableVertexAttribArray(shader.attrib_pos)
        glVertexAttribPointer(shader.attrib_pos, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_LINES,
                       self.mesh_data.index_buffer.size,
                       GL_UNSIGNED_INT,
                       None)

        # Draw deformed overlay if toggled
        if self.deformed_visible and self.vbo_disp is not None:
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_disp)
            glEnableVertexAttribArray(shader.attrib_pos)
            glVertexAttribPointer(shader.attrib_pos, 3, GL_FLOAT, GL_FALSE, 0, None)

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glDrawElements(GL_LINES,
                           self.mesh_data.index_buffer.size,
                           GL_UNSIGNED_INT,
                           None)

        # Clean up
        glDisableVertexAttribArray(shader.attrib_pos)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
