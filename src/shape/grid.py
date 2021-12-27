# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from src.vector import RGBA
from ..shape import Box, Shape


class Grid(Shape):
    def __init__(self, xSize, ySize, zSize, width):
        vertices = []
        faces = []

        xAxis = Box(xSize, width, width)
        yAxis = Box(width, ySize, width)
        zAxis = Box(width, width, zSize)

        vertices.extend(xAxis.vertices)
        i1 = len(vertices)

        vertices.extend(yAxis.vertices)
        i2 = len(vertices)

        vertices.extend(zAxis.vertices)

        faces.extend(xAxis.faces)

        i1*i2

        for i in yAxis.faces:
            for j in i:
                j[0] += i1

        for i in zAxis.faces:
            for j in i:
                j[0] += i2

        faces.extend(yAxis.faces)
        faces.extend(zAxis.faces)

        Shape.__init__(self, vertices, faces, [],
                       [], self.colors_as_np_array())

    def colors_as_np_array(self):  # x red, z green, y blue
        r = [RGBA(1.0, 0, 0, 1.0)] * 6
        g = [RGBA(0.0, 1.0, 0, 1.0)] * 6
        b = [RGBA(0.0, 0, 1.0, 1.0)] * 6
        colors = r + g + b
        return colors
