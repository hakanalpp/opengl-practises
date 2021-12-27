# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from .shape import Shape
from ..vector import Point3f


class Plane(Shape):
    def __init__(self, xSize, zSize):
        vertices = []
        vertices.append(Point3f(-xSize, -0.52, zSize))
        vertices.append(Point3f(xSize, -0.52, zSize))
        vertices.append(Point3f(xSize, -0.52, -zSize))
        vertices.append(Point3f(-xSize, -0.52, -zSize))

        self.vertices = vertices
        self.faces = [[0, 1, 2, 3]]
        Shape.__init__(self, vertices, self.faces)
