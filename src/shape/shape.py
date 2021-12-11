# CENG 487 Assignment#4 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from abc import abstractmethod
from ..matrix3d import Mat3d


class Shape:
    def __init__(self, *args):
        if (len(args) == 0):
            self.vertices = []
        elif (len(args) == 1):
            self.vertices = args[0]
        self.subdivisions = 0
        self.transformations = []

    def addVertice(self, vertice):
        self.vertices.append(vertice)

    def addTransformation(self, transformation):
        self.transformations.append(transformation)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def decrease_subdivision(self):
        pass

    @abstractmethod
    def increase_subdivision(self):
        pass

    @abstractmethod
    def apply_transformation(self, matrix):
        pass

    def move(self, x, y, z):
        self.apply_transformation(Mat3d.translation(x, y, z))

    def scale(self, sX, sY, sZ):
        self.apply_transformation(Mat3d.scale(sX, sY, sZ))

    def rotate(self, matrix):
        self.apply_transformation(matrix)
