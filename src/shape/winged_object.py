# CENG 487 Assignment#4 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from src.mesh.edge_adjacency import EdgeAdjacency

from src.mesh.face_adjacency import FaceAdjacency
from src.mesh.vertex_adjacency import VertexAdjacency
from src.mesh.winged_edge import WingedEdge


from .shape import Shape
from ..vector3d import Vec3d
from ..matrix3d import Mat3d


class WingedObject3D(Shape):

    def __init__(self, winged_edge):
        self.winged_edge = winged_edge
        self.transformations = []
        self.subdivision = 0
        self.subdivision_max_level = 0

    def draw(self, camera_matrix: 'Mat3d'):
        glEnableClientState(GL_COLOR_ARRAY)
        for face in self.winged_edge.faces:
            if(face.level != self.subdivision):
                continue
            vertices = [camera_matrix * j.p for j in face.vertices]
            glColor3f(0.4, 0.4, 0.4)
            glBegin(GL_POLYGON)
            for i in vertices:
                glVertex3f(i.x, i.y, i.z)
            glEnd()
            self.drawBorder(vertices)

        glDisableClientState(GL_COLOR_ARRAY)

    def drawBorder(self, vertices):
        glColor3f(1.0, 0.6, 0.0)
        glPointSize(5.0)
        glBegin(GL_LINE_LOOP)
        for i in vertices:
            glVertex3f(i.x, i.y, i.z)
        glEnd()

    def change_color(self):
        pass

    def increase_subdivision(self):
        if(self.subdivision < self.subdivision_max_level):
            self.subdivision += 1
            return
        faces: list[FaceAdjacency] = self.winged_edge.faces
        edges: list[EdgeAdjacency] = self.winged_edge.edges
        vertices: list[VertexAdjacency] = self.winged_edge.vertices
        we: WingedEdge = self.winged_edge

        we.level += 1
        for f in faces:
            if (not f.check_level(self.subdivision)):
                continue
            f.calculate_facepoint()
        for e in edges:
            if (not e.check_level(self.subdivision)):
                continue
            e.calculate_edgepoint()
        for v in vertices:
            F = None
            R = None
            connected_faces = []
            connected_edges = []

            for f in faces:
                if (not f.check_level(self.subdivision)):
                    continue
                if v in f.vertices and f not in connected_faces:
                    connected_faces.append(f)

            F = Vec3d.average_point(
                *[i.facepoint for i in connected_faces])
            for e in edges:
                if (not e.check_level(self.subdivision)):
                    continue
                if v in e.vertices and e not in connected_edges:
                    connected_edges.append(e)
            R = Vec3d.average_point(
                *[i.get_midpoint() for i in connected_edges])

            v.p = (F + (2*R) + ((len(connected_faces)-3)
                   * v.p)) * (1/(len(connected_faces)))

        index = 0
        flen = len(faces)
        while index < flen:
            f = faces[index]
            if (not f.check_level(self.subdivision)):
                index += 1
                continue
            if(len(we.get_all_edges(f)) != 4):
                print("Face'nin 4 edge'i yok!")
                break
            vIndex = [None, None, None, None]
            fp = we.add_vertex(f.facepoint.x, f.facepoint.y, f.facepoint.z)

            for i in we.get_all_edges(f):
                ep = we.add_vertex(i.edgepoint.x, i.edgepoint.y, i.edgepoint.z)
                if (f.is_edge_correct(0, 1, i)):
                    vIndex[0] = ep
                elif (f.is_edge_correct(1, 2, i)):
                    vIndex[1] = ep
                elif (f.is_edge_correct(2, 3, i)):
                    vIndex[2] = ep
                elif (f.is_edge_correct(3, 0, i)):
                    vIndex[3] = ep

            we.create_face_from_points(
                [f.vertices[0], vIndex[0], fp, vIndex[3]])

            we.create_face_from_points(
                [vIndex[0], f.vertices[1], vIndex[1], fp])

            we.create_face_from_points(
                [fp, vIndex[1], f.vertices[2], vIndex[2]])

            we.create_face_from_points(
                [vIndex[3], fp, vIndex[2], f.vertices[3]])
            index += 1

        we.set_edge_neighbours()
        self.subdivision += 1
        self.subdivision_max_level += 1

    def decrease_subdivision(self):
        if(self.subdivision == 0):
            print("Divison count can not be less than 0.")
            return
        self.subdivision -= 1

    def apply_transformation(self, matrix):
        for edge in self.winged_edge.edges:
            edge.vertices[0].p *= matrix
            edge.vertices[1].p *= matrix
