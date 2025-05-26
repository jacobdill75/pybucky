import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import numpy as np
import math
import glm

class View:
    def __init__(self, controller):
        if not glfw.init():
            raise RuntimeError("Could not initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        self.window = glfw.create_window(800, 600, "Conway Polyhedra", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Could not create window")

        glfw.make_context_current(self.window)
        glEnable(GL_DEPTH_TEST)

        self.shader = self.create_shader("vertex_shader.glsl", "fragment_shader.glsl")
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        self.controller = controller
        self.controller.install_callbacks(self.window)

    def create_shader(self, vs_path, fs_path):
        def compile_shader(source, shader_type):
            shader = glCreateShader(shader_type)
            glShaderSource(shader, source)
            glCompileShader(shader)
            if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
                raise RuntimeError(glGetShaderInfoLog(shader).decode())
            return shader

        with open(vs_path) as f: vs_src = f.read()
        with open(fs_path) as f: fs_src = f.read()

        vs = compile_shader(vs_src, GL_VERTEX_SHADER)
        fs = compile_shader(fs_src, GL_FRAGMENT_SHADER)

        shader = glCreateProgram()
        glAttachShader(shader, vs)
        glAttachShader(shader, fs)
        glLinkProgram(shader)

        glDeleteShader(vs)
        glDeleteShader(fs)

        return shader

    def render_polyhedron(self, poly):
        line_verts = poly.to_line_vertex_buffer()
        tri_verts = poly.to_triangle_vertex_buffer()

        # Clear screen
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glUseProgram(self.shader)

        # Setup transform matrices
        yaw, pitch = self.controller.rotate
        zoom = self.controller.zoom

        eye = glm.vec3(3, 3, 3)
        eye = glm.vec3(
            zoom * glm.cos(pitch) * glm.sin(yaw),
            zoom * glm.sin(pitch),
            zoom * glm.cos(pitch) * glm.cos(yaw)
        )
        center = glm.vec3(0)
        up = glm.vec3(0, 1, 0)

        # Matrices
        model = glm.rotate(glm.mat4(1), glfw.get_time() / 10, glm.vec3(0, 1, 0))
        view = glm.lookAt(eye, center, up)
        proj = glm.perspective(glm.radians(45.0), 800/600, 0.1, 100.0)

        glUniformMatrix4fv(glGetUniformLocation(self.shader, "model"), 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "view"), 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, glm.value_ptr(proj))

        # Draw filled faces
        glBufferData(GL_ARRAY_BUFFER, tri_verts.nbytes, tri_verts, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glUniform3f(glGetUniformLocation(self.shader, "color"), 0.2, 0.6, 1.0)
        glDrawArrays(GL_TRIANGLES, 0, len(tri_verts) // 3)

        # Draw edges
        glEnable(GL_POLYGON_OFFSET_LINE)
        glPolygonOffset(-1, -1)

        glBufferData(GL_ARRAY_BUFFER, line_verts.nbytes, line_verts, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glUniform3f(glGetUniformLocation(self.shader, "color"), 1.0, 1.0, 1.0)
        glDrawArrays(GL_LINES, 0, len(line_verts) // 3)

        # Swap buffer
        glfw.swap_buffers(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def update(self):
        glfw.poll_events()

    def terminate(self):
        glfw.terminate()
