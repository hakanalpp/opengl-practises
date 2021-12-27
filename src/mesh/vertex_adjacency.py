# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from ..vector import Point3f


class VertexAdjacency:
    def __init__(self, x, y, z):
        self.edge = None
        self.p: Point3f = Point3f(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def add_edge(self, e):
        if(self.edge == None):
            self.edge = e
            return True
        return False

    def __str__(self) -> str:
        return "Vertex: " + str(self.p)
