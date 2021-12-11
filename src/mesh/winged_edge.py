# CENG 487 Assignment#4 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from . import VertexAdjacency, FaceAdjacency, EdgeAdjacency


class WingedEdge:
    def __init__(self):
        self.edges: "list[EdgeAdjacency]" = []
        self.faces: "list[FaceAdjacency]" = []
        self.vertices: "list[VertexAdjacency]" = []
        self.level = 0

    def __str__(self) -> str:
        s = ""
        for edge in self.edges:
            s += str(edge) + "\n"
        for face in self.faces:
            s += str(face) + "\n"
        for vertice in self.vertices:
            s += str(vertice) + "\n"
        return s

    def add_edge(self, v1: VertexAdjacency, v2: VertexAdjacency):
        for e in self.edges:
            if (e.vertices[0] == v1 and e.vertices[1] == v2) or \
                    (e.vertices[1] == v1 and e.vertices[0] == v2):
                return None
        e = EdgeAdjacency(v1, v2, self.level)
        v1.add_edge(e)
        self.edges.append(e)

        if(e.is_legit() and e.edgepoint == None):
            e.calculate_edgepoint()
        return e

    def get_vertex(self, x, y, z):
        i = 0
        for v in self.vertices:
            if(x == v.x and y == v.y and z == v.z):
                return i
            i += 1
        return None

    def add_vertex(self, x, y, z):
        for i in self.vertices:
            if (i.x == x and i.y == y and i.z == z):
                return i
        v = VertexAdjacency(x, y, z)
        self.vertices.append(v)
        return v

    def get_all_edges(self, f1):
        tempEdges = []
        for e in self.edges:
            if (f1 in e.faces and f1.level == e.level):
                tempEdges.append(e)
        return tempEdges

    def add_face(self, face: FaceAdjacency):
        if (face not in self.faces):
            self.faces.append(face)
        if(face.is_legit()):
            face.calculate_facepoint()
        return face

    def create_face_from_points(self, points):
        self.add_edge(points[0], points[1])
        self.add_edge(points[1], points[2])
        self.add_edge(points[2], points[3])
        self.add_edge(points[3], points[0])

        f = FaceAdjacency(self.level)
        f.add_edge(self.edges[-1])
        f.add_vertex(points[0])
        f.add_vertex(points[1])
        f.add_vertex(points[2])
        f.add_vertex(points[3])
        self.add_face(f)
        return f

    def renew_edges(self):
        k = []
        for e in self.new_edges:
            if (e != None):
                k.append(e)
        self.edges = k

    def set_edge_neighbours(self):
        for e1 in self.edges:
            for e2 in self.edges:
                if e1.is_neighbour(e2) and e1.level == self.level:
                    e1.add_edge(e2)
                    e2.add_edge(e1)
            for fa in self.faces:
                if e1.vertices[0] in fa.vertices and e1.vertices[1] in fa.vertices and fa.level == e1.level == self.level:
                    e1.add_face(fa)
