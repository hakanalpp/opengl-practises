# CENG 487 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# November 2021

from .camera import Camera
from ..shape import Shape

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_9_BY_15


class Scene:
    camera = None
    width = 0
    height = 0
    objects: 'list[Shape]' = []
    subdivisons = 0

    def __init__(self, *args):
        self.camera = Camera()

    def set_size(self, w: 'int', h: 'int'):
        if h == 0:
            h = 1
        self.width = w
        self.height = h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def add_object(self, o: 'Shape'):
        self.objects.append(o)

    def remove_object(self, o: 'Shape'):
        self.objects.remove(o)

    def translate_camera(self, matrix):
        self.camera.translate(matrix)

    def increase_subdivision(self):
        for obj in self.objects:
            obj.increase_subdivision()

    def decrease_subdivision(self):
        for obj in self.objects:
            obj.decrease_subdivision()

    def draw(self):
        self.draw_text("Subdivision Count: {}".format(
            self.objects[0].subdivision), 20, 20)
        glEnableClientState(GL_VERTEX_ARRAY)
        for obj in self.objects:
            obj.draw(self.camera.position)
        glDisableClientState(GL_VERTEX_ARRAY)

    def draw_text(self, text, w, h):
        width = w if w > 0 else self.width + w
        height = h if h > 0 else self.height + h
        glColor3f(1, 1, 1)
        glWindowPos2d(width, height)
        for i in range(len(text)):
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(text[i]))
