# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from ..utils.fileIO import generate_vertices_with_tn
from .shape import Shape


class Object3D(Shape):
    def __init__(self, filename):
        c = generate_vertices_with_tn(filename)
        Shape.__init__(self, c[0], c[1], c[2], c[3])
