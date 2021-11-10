# CENG 487 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# November 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

from .shape import Shape
from ..matrix3d import Mat3d
from ..vector3d import Vec3d


class Plane(Shape):
    center = Vec3d(0, 0, 0, 1)
    vertices = []
    transformations = []
    subdivision = 0
    colors = []

    def __init__(self, *args):
        if (len(args) == 0):
            self.vertices = [Vec3d(2, -0.52, 2), Vec3d(-2, -0.52, 2),
                             Vec3d(-2, -0.52, -2), Vec3d(2, -0.52, -2)]
        self.colors = generate_colors(self.subdivision)

    def draw(self):
        ind = [j for j in range(len(self.vertices))]
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, self.colors)
        glVertexPointer(4, GL_FLOAT, 0, [o.v for o in self.vertices])
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glLineWidth(4)
        glDrawElementsui(
            GL_QUADS,  # GL_QUADS or GL_LINE_LOOP
            ind
        )

    def scale(self, sX, sY, sZ):
        for i in range(len(self.vertices)):
            self.vertices[i] *= Mat3d.scale(sX, sY, sZ)
        self.addTransformation(Mat3d.scale(sX, sY, sZ))

    def rotate(self, matrix):
        for i in range(len(self.vertices)):
            self.vertices[i] *= matrix
        self.addTransformation(matrix)

    def increase_subdivision(self):
        tempV = self.vertices
        j = 0
        while(len(tempV)-j >= 4):
            tempK = tempV.copy()
            centerPoint = Vec3d.middlePoint(tempV[j], tempV[j+2])
            tempV.insert(j+1, Vec3d.middlePoint(tempK[j], tempK[j+1]))
            tempV.insert(j+1, Vec3d(centerPoint))
            tempV.insert(j+1, Vec3d.middlePoint(tempK[j], tempK[j+3]))

            tempV.insert(j+5, Vec3d.middlePoint(tempK[j+1], tempK[j+2]))
            tempV.insert(j+5, Vec3d(centerPoint))
            tempV.insert(j+5, Vec3d.middlePoint(tempK[j+1], tempK[j]))

            tempV.insert(j+9, Vec3d.middlePoint(tempK[j+2], tempK[j+3]))
            tempV.insert(j+9, Vec3d(centerPoint))
            tempV.insert(j+9, Vec3d.middlePoint(tempK[j+1], tempK[j+2]))

            tempV.insert(j+13, Vec3d.middlePoint(tempK[j], tempK[j+3]))
            tempV.insert(j+13, Vec3d(centerPoint))
            tempV.insert(j+13, Vec3d.middlePoint(tempK[j+2], tempK[j+3]))

            j += 16

        self.subdivision += 1
        self.colors = generate_colors(self.subdivision)

    def decrease_subdivision(self):
        if(self.subdivision == 0):
            print("You can not decrease more than that.")
            return
        tempV = self.vertices
        temp = []
        j = 0
        while(len(tempV) > j):
            if(j % 4 == 0):
                temp.append(tempV[j])
            j += 1
        self.vertices = temp
        self.subdivision -= 1
        self.colors = generate_colors(self.subdivision)


def generate_colors(subdivision=0):
    return sum([[random.randint(0, 256) for _ in range(3)]*4 for __ in range(4**(subdivision+1))], [])
