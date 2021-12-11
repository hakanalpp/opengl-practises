# CENG 487 Assignment#4 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from src.vector3d import Vec3d


class VertexAdjacency:
    def __init__(self, x, y, z):
        self.edge = None
        self.p: Vec3d = Vec3d(x, y, z)
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
