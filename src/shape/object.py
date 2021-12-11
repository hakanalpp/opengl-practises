# CENG 487 Assignment#4 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


from .shape import Shape
from ..vector3d import Vec3d
from ..matrix3d import Mat3d


class Object3D(Shape):
    center = Vec3d(0, 0, 0, 1)
    subdivision = 0

    def __init__(self, *args):
        c = self.center
        if (len(args) == 1):  # Set default as unit vector3d
            self.vertices = args[0]
        # self.colors = generate_colors(6, self.subdivision)
        self.transformations = []

    def draw(self, camera_matrix: 'Mat3d'):
        glEnableClientState(GL_COLOR_ARRAY)
        for i in range(len(self.vertices)):
            ind = [j for j in range(len(self.vertices[i]))]
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, [
                           160 for _ in range(len(self.vertices)*len(self.vertices[0])*3)])
            glVertexPointer(4, GL_FLOAT, 0, [
                            (camera_matrix * o).v for o in self.vertices[i]])
            glLineWidth(2)
            glDrawElementsui(
                GL_QUADS,  # GL_QUADS or GL_LINE_LOOP
                ind
            )
            self.drawBorder(ind, self.vertices[i], camera_matrix)
        glDisableClientState(GL_COLOR_ARRAY)

    def drawBorder(self, ind, arr, camera_matrix: 'Mat3d'):
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, [
                       255 for _ in range(len(arr)*3)])
        glVertexPointer(4, GL_FLOAT, 0, [(camera_matrix * o).v for o in arr])
        glDrawElementsui(
            GL_LINE_LOOP,  # GL_POLYGON or GL_LINE_LOOP
            ind
        )

    def change_color(self):
        self.colors = generate_colors(6)

    def increase_subdivision(self):
        v = self.vertices
        for i in range(len(v)):
            tempV = v[i]
            j = 0
            while(len(tempV)-j >= 4):
                tempK = tempV.copy()
                c1 = Vec3d.middlePoint(tempV[j], tempV[j+2])
                c2 = Vec3d.middlePoint(tempV[j+1], tempV[j+3])
                centerPoint = Vec3d.middlePoint(c1, c2)

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
        self.rotate(Mat3d.rotateX(0.004))  # Rotate a bit to show subsurfaces
        self.rotate(Mat3d.rotateY(0.004))
        self.subdivision += 1
        # self.colors = generate_colors(6, self.subdivision)

    def decrease_subdivision(self):
        if(self.subdivision == 0):
            print("You can not decrease more than that.")
            return
        v = self.vertices
        for i in range(len(v)):
            tempV = v[i]
            temp = []
            j = 0
            while(len(tempV) > j):
                if(j % 4 == 0):
                    temp.append(tempV[j])
                j += 1
            self.vertices[i] = temp
        self.subdivision -= 1
        self.rotate(Mat3d.rotateX(-0.004))  # Rotate a bit to show subsurfaces
        self.rotate(Mat3d.rotateY(-0.004))
        # self.colors = generate_colors(6, self.subdivision)

    def apply_transformation(self, matrix):
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices[i])):
                self.vertices[i][j] *= matrix
        self.addTransformation(matrix)


def generate_colors(size, subdivision=0):
    res = [[random.randint(0, 256) for _ in range(3)]*4 for __ in range(size)]
    for ___ in range(int(4**subdivision)):
        k = [[random.randint(0, 256) for _ in range(3)]
             * 4 for __ in range(size)]
        res = [k[c] + res[c] for c in range(len(k))]
    return res
