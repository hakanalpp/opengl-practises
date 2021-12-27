# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from ..mesh import VertexAdjacency, WingedEdge
from src.vector import Point3f, Vector3f


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


def generate_vertices_with_tn(filename):
    with open(filename) as file:
        lines = file.readlines()
        vertices = []
        faces = []
        UVs = []
        normals = []
        for line in lines:
            line = line.strip()
            if(line.startswith("v ")):
                l = line.split(" ")
                vertices.append(Point3f(float(l[1]), float(l[2]), float(l[3])))
            elif(line.startswith("vt ")):
                l = line.split(" ")
                UVs.append([float(l[1]), float(l[2])])
            elif(line.startswith("vn ")):
                l = line.split(" ")
                normals.append(Point3f(float(l[1]), float(l[2]), float(l[3])))
            elif(line.startswith("f ")):
                if ("//" in line):
                    faces.append(
                        [[int(j.split("//")[0])-1, -1, int(j.split("//")[1])-1] for j in line.split(" ")[1:]])
                else:
                    faces.append([[int(i)-1 for i in j.split("/")]
                                 for j in line.split(" ")[1:]])
    return [vertices, faces, UVs, normals]


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
