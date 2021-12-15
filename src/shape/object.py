# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from ..utils.fileIO import generate_vertices
from .shape import Shape


class Object3D(Shape):
    def __init__(self, filename):
        c = generate_vertices(filename)
        Shape.__init__(self, c[0], c[1])
