# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_9_BY_15
import numpy as np

from ..matrix import Matrix
from ..shader import Shader
from ..shape import Grid, Shape
from .camera import Camera


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.shader: 'Shader' = Shader(self.camera)
        self.width = 640
        self.height = 640
        self.objects: 'list[Shape]' = []
        self.subdivisons = 0
        self.grid = Grid(3, 3, 3, 0.009)

    def draw(self):
        if(len(self.objects) == 0):
            return
        self.draw_text("Subdivision Count: {}".format(
            self.objects[0].subdivision), 20, 20)
        self.shader.display()

    def add_vertex_buffer(self):
        arr = np.array([], dtype='float32')
        color = np.array([], dtype='float32')
        for obj in self.objects:
            arr = np.append(arr, obj.as_np_array())
            color = np.append(
                color, obj.colors_as_np_array())
        arr = np.append(arr, self.grid.as_np_array())
        color = np.append(color, self.grid.colors_as_np_array())
        self.shader.initVertexBuffer(arr, color)

    def draw_text(self, text, w, h):
        width = w if w > 0 else self.width + w
        height = h if h > 0 else self.height + h
        glColor3f(1, 1, 1)
        glWindowPos2d(width, height)
        for i in range(len(text)):
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(text[i]))

    def add_object(self, o: 'Shape'):
        self.objects.append(o)
        self.add_vertex_buffer()

    def remove_object(self, o: 'Shape'):
        self.objects.remove(o)
        self.add_vertex_buffer()

    def transform_objects(self, matrix: 'Matrix'):
        for obj in self.objects:
            obj.rotate(matrix)
        self.add_vertex_buffer()

    def increase_subdivision(self):
        for obj in self.objects:
            obj.increase_subdivision()
        self.add_vertex_buffer()

    def decrease_subdivision(self):
        for obj in self.objects:
            obj.decrease_subdivision()
        self.add_vertex_buffer()

    def set_size(self, w: 'int', h: 'int'):
        if h == 0:
            h = 1
        self.width = w
        self.height = h

        # Reset The Current Viewport And Perspective Transformation
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
