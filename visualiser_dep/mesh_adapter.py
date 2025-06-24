"""
mesh_adapter.py

Scene adapter for MiniFEA renderer: uploads MeshData buffers to GPU (VBO/EBO),
handles attribute binding, and issues draw calls for both undeformed and deformed meshes.
"""
from OpenGL.GL import *
import numpy as np

class Scene:
    """
    Wraps MeshData for rendering: creates VBO/EBOs, updates buffers, and draws.
    """
    def __init__(self, mesh_data):
        """
        Initialize GPU buffers from MeshData.

        Args:
            mesh_data (MeshData): instance containing node, disp, index buffers.
        """
        self.mesh_data = mesh_data
        self.deformed_visible = False

        # Generate buffer objects
        self.vbo_nodes = glGenBuffers(1)
        self.vbo_disp = glGenBuffers(1) if mesh_data.disp_buffer is not None else None
        self.ebo = glGenBuffers(1)

        # Upload static data
        self._upload_node_positions()
        self._upload_indices()

        if self.vbo_disp:
            self._upload_displacements()

    def _upload_node_positions(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_nodes)
        glBufferData(GL_ARRAY_BUFFER,
                     self.mesh_data.node_buffer.nbytes,
                     self.mesh_data.node_buffer,
                     GL_STATIC_DRAW)

    def _upload_displacements(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_disp)
        glBufferData(GL_ARRAY_BUFFER,
                     self.mesh_data.disp_buffer.nbytes,
                     self.mesh_data.disp_buffer,
                     GL_DYNAMIC_DRAW)

    def _upload_indices(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     self.mesh_data.index_buffer.nbytes,
                     self.mesh_data.index_buffer,
                     GL_STATIC_DRAW)

    def update_displacements(self, new_disp_buffer):
        """
        Replace GPU displacement buffer with updated values.

        Args:
            new_disp_buffer (np.ndarray): flattened float32 displacement array.
        """
        if not self.vbo_disp:
            raise RuntimeError("No displacement buffer allocated")
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_disp)
        # orphan and refill buffer
        glBufferData(GL_ARRAY_BUFFER,
                     new_disp_buffer.nbytes,
                     None,
                     GL_DYNAMIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER,
                        0,
                        new_disp_buffer.nbytes,
                        new_disp_buffer)

    def toggle_deformed_visibility(self):
        """Flip visibility state for deformed mesh overlay."""
        self.deformed_visible = not self.deformed_visible

    def draw(self, shader):
        """
        Draw undeformed mesh lines and, if enabled, deformed overlay.

        Args:
            shader: active line shader with known attribute locations.
        """
        # Bind undeformed positions
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_nodes)
        glEnableVertexAttribArray(shader.attrib_pos)
        glVertexAttribPointer(shader.attrib_pos, 3, GL_FLOAT, GL_FALSE, 0, None)

        # No color attribute -> use shader uniform or per-vertex lookup
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_LINES,
                       self.mesh_data.index_buffer.size,
                       GL_UNSIGNED_INT,
                       None)

        if self.deformed_visible and self.vbo_disp:
            # Overlay deformed mesh (using displacement buffer as positions)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_disp)
            glEnableVertexAttribArray(shader.attrib_pos)
            glVertexAttribPointer(shader.attrib_pos, 3, GL_FLOAT, GL_FALSE, 0, None)
            glDrawElements(GL_LINES,
                           self.mesh_data.index_buffer.size,
                           GL_UNSIGNED_INT,
                           None)

        # Cleanup
        glDisableVertexAttribArray(shader.attrib_pos)
