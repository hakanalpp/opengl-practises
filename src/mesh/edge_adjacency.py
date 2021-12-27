# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from src.mesh.face_adjacency import FaceAdjacency
from src.mesh.vertex_adjacency import VertexAdjacency
from src.vector import Point3f


class EdgeAdjacency:
    def __init__(self, v1, v2, level):
        self.vertices: list[VertexAdjacency] = [v1, v2]
        self.faces: list[FaceAdjacency] = [None, None]
        self.edges: list[EdgeAdjacency] = [None, None, None, None]
        self.edgepoint = None
        self.level = level

    def add_face(self, f: FaceAdjacency) -> FaceAdjacency:
        for i in range(len(self.faces)):
            if(self.faces[i] == None):
                self.faces[i] = f
                return f
        return False

    def add_edge(self, e):
        if (self == e or e in self.edges):
            return False

        for i in range(len(self.edges)):
            if(self.edges[i] == None):
                self.edges[i] = e
                return e
        return False

    def add_vertex(self, x, y, z):
        for i in self.vertices:
            if (i.x == x and i.y == y and i.z == z):
                return i
        v = VertexAdjacency(x, y, z)
        self.vertices.append(v)
        return v

    def is_neighbour(self, e2) -> bool:
        if (self == e2 or self.level != e2.level):
            return False
        for i in self.vertices:
            if (i == e2.vertices[0] or i == e2.vertices[1]):
                return True
        return False

    def calculate_edgepoint(self):
        v = self.vertices
        f = self.faces
        self.edgepoint = Point3f.average_point(
            v[0].p, v[1].p, f[0].facepoint, f[1].facepoint)
        return self.edgepoint

    def __str__(self) -> str:
        return str(self.vertices[0]) + ", " + str(self.vertices[1])

    def get_midpoint(self):
        return Point3f.middle_point(self.vertices[0].p, self.vertices[1].p)

    def is_legit(self):
        for i in self.vertices:
            if (i == None):
                return False
        for f in self.faces:
            if (f == None):
                return False
        return True

    def check_level(self, lev):
        return self.level == lev
