# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from src.vector import Point3f, RGBA, Vector3f
from ..matrix import Matrix

import numpy


class Shape:
    def __init__(self, vertices, faces, UVs, normals, colors=[]):
        self.vertices: 'list[Point3f]' = vertices
        # Formed as [Vertex, Texture, Normal]
        self.faces: 'list[list[list[int]]]' = faces
        self.UVs: 'list[list[float]]' = UVs if len(
            UVs) > 0 else self.generate_empty_uvs()
        self.normals: 'list[Vector3f]' = normals if len(
            normals) > 0 else self.generate_empty_normals()
        self.subdivision = 0
        self.transformations = []
        if len(colors) > 0:
            self.colors = colors
        else:
            self.generate_color()

    def addTransformation(self, transformation):
        self.transformations.append(transformation)

    def as_np_array(self):
        v = []
        for f in self.faces:
            v += [self.vertices[i].asList() for i in f]
        return numpy.array(v, dtype='float32').flatten()

    def colors_as_np_array(self):
        colors = []
        for c in self.colors:
            colors += c.asList(4)
        return numpy.array(colors, dtype='float32')

    def colors_as_list(self):
        colors = []
        for c in self.colors:
            colors += c.asList(4)
        return colors

    def white_colors_as_list(self):
        return [1.0 for i in range(len(self.colors)*16)]

    def generate_empty_uvs(self):
        return [-1 for i in range(len(self.faces)*2)]

    def generate_empty_normals(self):
        return [Point3f(0.73, 0.73, 0.73)] * len(self.faces)

    def generate_color(self):
        self.colors = [RGBA(*[random.uniform(0, 1) for _ in range(3)], 1.0)
                       for __ in range(len(self.faces))]

    def vertices_asList(self) -> 'list[Point3f]':
        v = []
        for f in self.faces:
            for p in f:
                v.append(self.vertices[p])
        return v

    def increase_subdivision(self):
        v = self.vertices
        tempFaces = []
        for f in self.faces:
            iCenter = len(v)
            v.append(Point3f.average_point(*[v[i] for i in f]))

            i01 = len(v)
            v.append(Point3f.middle_point(v[f[0]], v[f[1]]))

            i12 = len(v)
            v.append(Point3f.middle_point(v[f[1]], v[f[2]]))

            i23 = len(v)
            v.append(Point3f.middle_point(v[f[2]], v[f[3]]))

            i30 = len(v)
            v.append(Point3f.middle_point(v[f[3]], v[f[0]]))

            tempFaces.append([f[0], i30, iCenter, i01])
            tempFaces.append([f[1], i01, iCenter, i12])
            tempFaces.append([f[2], i12, iCenter, i23])
            tempFaces.append([f[3], i23, iCenter, i30])

        self.faces = tempFaces
        self.vertices = v
        self.generate_color()
        self.subdivision += 1

    def decrease_subdivision(self):
        if(self.subdivision == 0):
            print("You can not decrease more than that.")
            return
        tempFaces = []
        faces = self.faces
        for i in range(0, len(self.faces), 4):
            tempFaces.append([faces[i][0], faces[i+1][0],
                             faces[i+2][0], faces[i+3][0]])
        self.faces = tempFaces
        self.generate_color()
        self.subdivision -= 1

    def apply_transformation(self, matrix):
        for i in range(len(self.vertices)):
            self.vertices[i] = matrix * self.vertices[i]
        self.addTransformation(matrix)

    def move(self, x, y, z):
        self.apply_transformation(Matrix.translation(x, y, z))

    def scale(self, sX, sY, sZ):
        self.apply_transformation(Matrix.scale(sX, sY, sZ))

    def rotate(self, matrix):
        self.apply_transformation(matrix)
