# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from ..vector import Point3f


class FaceAdjacency:
    def __init__(self, level):
        self.edge = None
        self.vertices = [None, None, None, None]
        self.facepoint = None
        self.level = level

    def add_edge(self, e):
        if(self.edge == None):
            self.edge = e
            return True
        return False

    def add_vertex(self, v):
        for i in range(len(self.vertices)):
            if(self.vertices[i] == None):
                self.vertices[i] = v
                return True
        return False

    def __str__(self) -> str:
        return str(self.edge)

    def calculate_facepoint(self):
        v = self.vertices
        self.facepoint = Point3f((v[0].x + v[1].x + v[2].x + v[3].x)/4,
                                 (v[0].y + v[1].y + v[2].y + v[3].y)/4,
                                 (v[0].z + v[1].z + v[2].z + v[3].z)/4)
        return self.facepoint

    def get_all_edges(self):
        neighbours = []
        for neighbour in self.edge.edges:
            if self in neighbour.faces:
                neighbours.append(neighbour)
        flag = 0
        for n in neighbours:
            for n2 in n.edges:
                if self in n2.faces:
                    neighbours.append(n2)
                    flag = 1
                    break
            if flag == 1:
                break

        neighbours.append(self.edge)
        return neighbours

    def is_edge_correct(self, i1, i2, edge):
        if ((self.vertices[i1] == edge.vertices[0] and self.vertices[i2] == edge.vertices[1]) or
                (self.vertices[i1] == edge.vertices[1] and self.vertices[i2] == edge.vertices[0])):
            return True
        return False

    def is_legit(self):
        for i in self.vertices:
            if (i == None):
                return False
        return True

    def check_level(self, lev):
        return self.level == lev
