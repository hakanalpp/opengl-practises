# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from ..mesh import VertexAdjacency, WingedEdge
from src.vector import Point3f


def generate_vertices(filename):
    with open(filename) as file:
        lines = file.readlines()
        vertices = []
        faces = []
        for line in lines:
            line = line.strip()
            if(line.startswith("v")):
                l = line.split(" ")
                vertices.append(Point3f(float(l[1]), float(l[2]), float(l[3])))
            if(line.startswith("f")):
                f = line.split(" ")
                faces.append([int(f[1])-1, int(f[2])-1,
                             int(f[3])-1, int(f[4])-1])
    return [vertices, faces]


def generate_winged_edge(filename):
    k = get_triangluated_faces_and_vertices(filename)
    we = WingedEdge()
    we.vertices = k[0]
    faces = k[1]
    for face in faces:
        we.create_face_from_points([we.vertices[i-1] for i in face[0:4]])
    we.set_edge_neighbours()
    return we


def get_triangluated_faces_and_vertices(filename):
    with open(filename) as file:
        lines = file.readlines()
        vertices = []
        faces = []
        for line in lines:
            line = line.strip()
            if(line.startswith("v")):
                l = line.split(" ")
                vertices.append(VertexAdjacency(
                    float(l[1]), float(l[2]), float(l[3])))
            if(line.startswith("f")):
                f = line.split(" ")
                faces.append([int(f[1]), int(f[2]), int(f[3]), int(f[4])])
    return [vertices, faces]
