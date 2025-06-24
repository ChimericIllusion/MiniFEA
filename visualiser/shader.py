"""
shader.py

ShaderManager for MiniFEA renderer: compiles GLSL shaders, links program,
manages 1D colormap textures, and handles shader use with uniform updates.
"""
from OpenGL.GL import *
import numpy as np
from PIL import Image

class ShaderManager:
    """
    Handles GLSL shader compilation, program linking, and colormap textures.
    """
    def __init__(self, vert_path, frag_path, colormaps=None):
        """
        Compile and link the vertex and fragment shaders.

        Args:
            vert_path (str): path to vertex shader source file.
            frag_path (str): path to fragment shader source file.
            colormaps (list[str], optional): list of file paths to colormap images.
        """
        # Load shader sources
        with open(vert_path, 'r') as f:
            vert_src = f.read()
        with open(frag_path, 'r') as f:
            frag_src = f.read()

        # Compile & link program
        self.program = glCreateProgram()
        vert = self._compile_shader(GL_VERTEX_SHADER, vert_src)
        frag = self._compile_shader(GL_FRAGMENT_SHADER, frag_src)
        glAttachShader(self.program, vert)
        glAttachShader(self.program, frag)
        glLinkProgram(self.program)

        # Check link status
        status = glGetProgramiv(self.program, GL_LINK_STATUS)
        if not status:
            msg = glGetProgramInfoLog(self.program).decode()
            raise RuntimeError(f"Shader link failed: {msg}")

        # Clean up shaders
        glDeleteShader(vert)
        glDeleteShader(frag)

        # Get attribute/uniform locations
        self.attrib_pos     = glGetAttribLocation(self.program, 'a_position')
        self.unif_mvp       = glGetUniformLocation(self.program, 'uMVP')
        self.unif_colormap  = glGetUniformLocation(self.program, 'uColormap')

        # Colormap textures
        self.colormaps = colormaps or []
        self.tex_ids    = []
        self.current    = 0
        for path in self.colormaps:
            self._load_colormap(path)

    def _compile_shader(self, shader_type, src):
        sh = glCreateShader(shader_type)
        glShaderSource(sh, src)
        glCompileShader(sh)

        # Check compile status
        ok = glGetShaderiv(sh, GL_COMPILE_STATUS)
        if not ok:
            msg = glGetShaderInfoLog(sh).decode()
            raise RuntimeError(f"Shader compile failed ({shader_type}): {msg}")
        return sh

    def _load_colormap(self, image_path):
        """
        Load a colormap PNG as a 1D texture.
        """
        img = Image.open(image_path).convert('RGB')
        data = np.array(img, dtype=np.uint8)
        h, w, _ = data.shape
        length = max(w, h)
        tex_data = data.reshape(length, 3)

        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_1D, tex)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGB, length, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_data)
        glBindTexture(GL_TEXTURE_1D, 0)

        self.tex_ids.append(tex)

    def cycle_colormap(self):
        """
        Advance to next colormap in the list.
        """
        if not self.tex_ids:
            return
        self.current = (self.current + 1) % len(self.tex_ids)

    def use(self, mvp_matrix):
        """
        Bind program, set uniforms (MVP & colormap), and activate texture.

        Args:
            mvp_matrix (np.ndarray): 4x4 float32 MVP matrix.
        """
        glUseProgram(self.program)
        # Upload MVP
        glUniformMatrix4fv(self.unif_mvp, 1, GL_FALSE, mvp_matrix)
        # Bind colormap texture if available
        if self.tex_ids:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_1D, self.tex_ids[self.current])
            glUniform1i(self.unif_colormap, 0)
