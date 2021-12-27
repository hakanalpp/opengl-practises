# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from .shape import Shape
from ..vector import Point3f


class Box(Shape):
    subdivision = 0

    def __init__(self, xSize, ySize, zSize):
        vertices = []
        vertices.append(Point3f(xSize, -ySize, -zSize))
        vertices.append(Point3f(xSize, -ySize, zSize))
        vertices.append(Point3f(-xSize, -ySize, zSize))
        vertices.append(Point3f(-xSize, -ySize, -zSize))
        vertices.append(Point3f(xSize, ySize, -zSize))
        vertices.append(Point3f(xSize, ySize, zSize))
        vertices.append(Point3f(-xSize, ySize, zSize))
        vertices.append(Point3f(-xSize, ySize, -zSize))

        faces = []
        faces.append([0, 1, 2, 3])
        faces.append([4, 7, 6, 5])
        faces.append([0, 4, 5, 1])
        faces.append([1, 5, 6, 2])
        faces.append([2, 6, 7, 3])
        faces.append([4, 0, 3, 7])

        faces = [[[j, -1, -1] for j in i] for i in faces]

        Shape.__init__(self, vertices, faces, [], [])
