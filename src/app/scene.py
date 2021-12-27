# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_9_BY_15
import numpy as np

from src.shape.box import Box

from ..matrix import Matrix
from ..shader import Shader
from ..shape import Shape
from .camera import Camera


class Scene:
    def __init__(self):
        self.camera = Camera()
        self.shader: 'Shader' = Shader(self.camera)
        self.width = 640
        self.height = 640
        self.objects: 'list[Shape]' = []
        self.subdivisons = 0
        # This object is added to show light's place.
        self.light1Obj = Box(0.05, 0.05, 0.05)
        self.light1Obj.move(1.3, 1.54, 0.0)
        self.add_object(self.light1Obj)
        self.should_rotate = False

    def draw(self):
        if(len(self.objects) == 0):
            return
        self.display_informative_text()
        self.shader.display()

    def update_vertex_buffer(self):
        finalVertexPositions = []
        finalVertexUvs = []
        finalVertexNormals = []
        colors = []
        faceCount = 0
        for obj in self.objects:
            for face in obj.faces:
                for vertex in face:
                    finalVertexPositions.extend(
                        obj.vertices[vertex[0]].asList())
                    if vertex[1] != -1:
                        finalVertexUvs.extend(obj.UVs[vertex[1]])
                    else:
                        finalVertexUvs.extend([-1, -1])
                    finalVertexNormals.extend(obj.normals[vertex[2]].asList())
            colors.extend(obj.colors_as_list())
            faceCount += len(obj.faces)
        self.shader.initVertexBuffer(np.array(
            finalVertexPositions + colors + finalVertexUvs + finalVertexNormals, dtype="float32"), faceCount)

    def rotate_point_light_y(self, y):
        pos = self.shader.pointLight.lightPos
        self.shader.pointLight.lightPos = Matrix.rotateY(y) * pos
        self.light1Obj.rotate(Matrix.rotateY(y))

        self.shader.initLightParams()
        self.update_vertex_buffer()

    def draw_text(self, text, w, h):
        width = w if w > 0 else self.width + w
        height = h if h > 0 else self.height + h
        glColor3f(1, 1, 1)
        glWindowPos2d(width, height)
        for i in range(len(text)):
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(text[i]))

    def add_object(self, o: 'Shape'):
        self.objects.append(o)

    def remove_object(self, o: 'Shape'):
        self.objects.remove(o)
        self.update_vertex_buffer()

    def transform_objects(self, matrix: 'Matrix'):
        for obj in self.objects:
            obj.rotate(matrix)
        self.update_vertex_buffer()

    def increase_scale(self):
        if(self.shader.texScale < 1.0):
            self.shader.texScale += 0.05
        else:  # Doing this to get rid of floating point issues
            self.shader.texScale = 1.0

    def decrease_scale(self):
        if(self.shader.texScale > 0.0):
            self.shader.texScale -= 0.05
        else:  # Doing this to get rid of floating point issues
            self.shader.texScale = 0.0

    def increase_subdivision(self):
        for obj in self.objects:
            obj.increase_subdivision()
        self.update_vertex_buffer()

    def decrease_subdivision(self):
        for obj in self.objects:
            obj.decrease_subdivision()
        self.update_vertex_buffer()

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

    def point_light_open(self):
        return "Open" if self.shader.pointLight.lightIntensity == 1.0 else "Closed"

    def directional_light_open(self):
        return "Open" if self.shader.directionalLight.lightIntensity == 1.0 else "Closed"

    def display_informative_text(self):
        self.draw_text("Blinn: {}".format(self.shader.blinn), 20, 100)
        self.draw_text("Point Light (White): {}".format(
            self.point_light_open()), 20, 80)
        self.draw_text("Directional Light (Red, [1,1,0]): {}".format(
            self.directional_light_open()), 20, 60)
        self.draw_text("Point Light Rotating: {}".format(
            self.should_rotate), 20, 40)
        self.draw_text("Texture 1: {:.2f}, Texture 2: {:.2f}".format(
            1-self.shader.texScale, self.shader.texScale), 20, 20)
