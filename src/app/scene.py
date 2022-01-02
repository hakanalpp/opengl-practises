# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_9_BY_15
import numpy as np

from src.light import PointLight, SpotLight, DirectionalLight
from src.shape.box import Box
from src.vector import RGBA

from ..matrix import Matrix
from ..shader import Shader
from ..shape import Shape
from .camera import Camera


class Scene:

    def __init__(self):
        self.camera = Camera()
        self.objects: 'list[Shape]' = []

        self.width = 640
        self.height = 640
        self.subdivisons = 0
        self.should_animate = False

        # Thes Boxes are added to show lights' places.
        self.pointLightBox = Box(0.05, 0.05, 0.05)
        self.pointLightBox.move(1.3, 1.54, 0.0)
        self.spotLightBox = Box(0.05, 0.05, 0.05)
        self.spotLightBox.move(-1.45, 0, 0.0)
        self.add_object(self.pointLightBox)
        self.add_object(self.spotLightBox)

        # Lights
        self.pointLight = PointLight(1.3, 1.54, 0.0, RGBA(1, 1, 1, 1))
        self.directionalLight = DirectionalLight(
            0, 1, -1, RGBA(1, 0, 0, 1))
        self.spotLight = SpotLight(-1.45, 0, 0.0,
                                   1, -0.45, -0.1, 0.2, RGBA(0, 0, 1, 1))
        self.shader: 'Shader' = Shader(
            self.camera, self.pointLight, self.directionalLight, self.spotLight)

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

    def rotate_point_light_y(self, y):
        pos = self.pointLight.position
        self.pointLight.position = Matrix.rotateY(y) * pos
        self.pointLightBox.rotate(Matrix.rotateY(y))

    def rotate_spot_light(self, angle):
        self.spotLight.direction = Matrix.rotateX(
            angle) * self.spotLight.direction

    def point_light_on(self):
        return "On" if self.pointLight.lightIntensity == 1.0 else "Off"

    def directional_light_on(self):
        return "On" if self.directionalLight.lightIntensity == 1.0 else "Off"

    def spot_light_on(self):
        return "On" if self.spotLight.lightIntensity == 1.0 else "Off"

    def display_informative_text(self):
        self.draw_text("Blinn: {}".format(
            "On" if self.shader.blinn else "Off"), 20, 120)
        self.draw_text("Point Light (White): {}".format(
            self.point_light_on()), 20, 100)
        self.draw_text("Directional Light (Red, [0,1,1]): {}".format(
            self.directional_light_on()), 20, 80)
        self.draw_text("Spot Light (Blue, Left Wall, [1, -0.45, -0.1], 20°): {}".format(
            self.spot_light_on()), 20, 60)
        self.draw_text("Point Light Rotating: {}".format(
            "On" if self.should_animate else "Off"), 20, 40)
        self.draw_text("Texture 1: {:.2f}, Texture 2: {:.2f}".format(
            1-self.shader.texScale, self.shader.texScale), 20, 20)
