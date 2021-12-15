# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

import numpy as np

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
        faces.extend([[j+i1 for j in i]for i in yAxis.faces])
        faces.extend([[j+i2 for j in i]for i in zAxis.faces])

        Shape.__init__(self, vertices, faces)

    def colors_as_np_array(self):  # x kırmızı, z yeşil, y mavi
        r = [1.0, 0, 0, 1.0] * 24
        g = [0.0, 1.0, 0, 1.0] * 24
        b = [0.0, 0, 1.0, 1.0] * 24
        colors = r + g + b
        return np.array(colors, dtype='float32')
