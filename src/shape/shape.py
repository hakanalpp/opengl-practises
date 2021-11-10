# CENG 487 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# November 2021

from abc import abstractmethod
from ..matrix3d import Mat3d


class Shape:
    def __init__(self, *args):
        if (len(args) == 0):  # Set default as unit vector3d
            self.vertices = []
            self.colors = []
        elif (len(args) == 2):
            self.vertices = args[0]
            self.colors = args[1]
        self.transformations = []

    def addVertice(self, vertice):
        self.vertices.append(vertice)

    def addTransformation(self, transformation):
        self.transformations.append(transformation)

    @abstractmethod
    def decrease_subdivision(self):
        pass

    @abstractmethod
    def increase_subdivision(self):
        pass

