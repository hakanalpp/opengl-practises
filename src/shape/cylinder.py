# CENG 487 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# November 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

from .shape import Shape
from ..vector3d import Vec3d


class Cylinder(Shape):
    def __init__(self, polygonCount=8, r=0.5, h=1):
        self.polygonCount = polygonCount
        self.r = r
        self.h = h
        self.transformations = []

        topCircle = []
        bottomCircle = []
        angle = 360 / polygonCount
        for i in range(polygonCount+1):
            k = math.radians(i*angle)
            topCircle.append(Vec3d(math.cos(k)*r+1, h/2, math.sin(k)*r))
            bottomCircle.append(Vec3d(math.cos(k)*r+1, -h/2, math.sin(k)*r))

        self.topCircle = topCircle
        self.bottomCircle = bottomCircle

        side = []
        for i in range(len(topCircle)-1):
            side.append([Vec3d(topCircle[i+1].x, topCircle[i+1].y, topCircle[i+1].z), Vec3d(topCircle[i].x, topCircle[i].y, topCircle[i].z),
                         Vec3d(bottomCircle[i].x, bottomCircle[i].y, bottomCircle[i].z), Vec3d(bottomCircle[i+1].x, bottomCircle[i+1].y, bottomCircle[i+1].z)])
        self.side = side

    def draw(self):
        glLineWidth(2)
        glEnableClientState(GL_COLOR_ARRAY)
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, [120 for i in range(1000)])

        ind = [j for j in range(len(self.topCircle))]

        glVertexPointer(4, GL_FLOAT, 0, [o.v for o in self.topCircle])
        glDrawElementsui(
            GL_POLYGON,  # GL_POLYGON or GL_LINE_LOOP
            ind
        )
        self.drawBorder(ind, self.topCircle)

        glVertexPointer(4, GL_FLOAT, 0, [o.v for o in self.bottomCircle])
        glDrawElementsui(
            GL_POLYGON,  # GL_POLYGON or GL_LINE_LOOP
            ind
        )
        self.drawBorder(ind, self.bottomCircle)

        for i in self.side:
            ind2 = [j for j in range(len(i))]
            glVertexPointer(4, GL_FLOAT, 0, [o.v for o in i])
            glDrawElementsui(
                GL_QUADS,  # GL_QUADS or GL_LINE_LOOP
                ind2
            )
            self.drawBorder(ind2, i)
        glDisableClientState(GL_COLOR_ARRAY)

    def drawBorder(self, ind, arr):
        glDisableClientState(GL_COLOR_ARRAY)
        glVertexPointer(4, GL_FLOAT, 0, [o.v for o in arr])
        glDrawElementsui(
            GL_LINE_LOOP,  # GL_POLYGON or GL_LINE_LOOP
            ind
        )
        glEnableClientState(GL_COLOR_ARRAY)

    def increase_subdivision(self):
        k = Cylinder(self.polygonCount*2, 0.5, 1)
        for i in self.transformations:
            k.rotate(i)
        self.__dict__.update(k.__dict__)

    def decrease_subdivision(self):
        if(self.polygonCount <= 8):
            return
        k = Cylinder(int(self.polygonCount/2), 0.5, 1)
        for i in self.transformations:
            k.rotate(i)
        self.__dict__.update(k.__dict__)

    def apply_transformation(self, matrix):
        k = self.side
        for i in range(len(k)):
            for j in range(len(self.side[i])):
                self.side[i][j] *= matrix
        for i in range(len(self.topCircle)):
            self.topCircle[i] *= matrix
            self.bottomCircle[i] *= matrix
        self.addTransformation(matrix)
