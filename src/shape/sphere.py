# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

from .shape import Shape
from ..vector import Point3f
from ..matrix import Matrix


class Sphere(Shape):
    def __init__(self, circleCount=6, r=0.5):
        self.circleCount = circleCount
        self.circles = [[] for _ in range(circleCount*2)]
        self.r = r
        self.transformations = []

        circles = self.circles
        angle = 360 / circleCount
        for i in range(circleCount):
            tempR = (r*abs((circleCount) - i)) / (circleCount)
            for j in range(circleCount+1):
                k = math.radians(j*angle)
                circles[circleCount-i-1].append(
                    Point3f(math.cos(k)*tempR, (0.01) + r*(i/circleCount), math.sin(k)*tempR))
                circles[circleCount+i].append(Point3f(math.cos(k)
                                                      * tempR, -(0.01) - r*(i/circleCount), math.sin(k)*tempR))

    def draw(self, camera_matrix: "Matrix"):
        glLineWidth(1)
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, [120 for _ in range(1000)])
        glEnableClientState(GL_COLOR_ARRAY)

        circles = self.circles
        for i in range(len(circles)-1):
            for j in range(self.circleCount):
                ind = [j for j in range(4)]
                k = [circles[i][j+1], circles[i][j],
                     circles[i+1][j], circles[i+1][j+1]]
                glVertexPointer(4, GL_FLOAT, 0, [
                                (camera_matrix * o).v for o in k])
                glDrawElementsui(
                    GL_QUADS,  # GL_POLYGON or GL_LINE_LOOP
                    ind
                )
                self.draw_border(k, camera_matrix)

    def draw_border(self, arr, camera_matrix: "Matrix"):
        glDisableClientState(GL_COLOR_ARRAY)
        glVertexPointer(4, GL_FLOAT, 0, [(camera_matrix * o).v for o in arr])
        glDrawElementsui(
            GL_LINE_LOOP,  # GL_POLYGON or GL_LINE_LOOP
            [i for i in range(len(arr))]
        )
        glEnableClientState(GL_COLOR_ARRAY)

    def increase_subdivision(self):
        k = Sphere(self.circleCount+1, self.r)
        for i in self.transformations:
            k.rotate(i)
        self.__dict__.update(k.__dict__)

    def decrease_subdivision(self):
        k = Sphere(self.circleCount-1, self.r)
        for i in self.transformations:
            k.rotate(i)
        self.__dict__.update(k.__dict__)

    def apply_transformation(self, matrix):
        for i in range(len(self.circles)):
            for j in range(len(self.circles[i])):
                self.circles[i][j] *= matrix
        self.addTransformation(matrix)
