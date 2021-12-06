from OpenGL.GLUT.fonts import GLUT_BITMAP_9_BY_15
from OpenGL.GLUT import *
from OpenGL.GL import glWindowPos2d

from src.vector3d import Vec3d


def generate_vertices(filename):
    with open(filename) as file:
        lines = file.readlines()
        vertices = []
        faces = []
        for line in lines:
            line = line.strip()
            if(line.startswith("v")):
                l = line.split(" ")
                vertices.append(Vec3d(float(l[1]), float(l[2]), float(l[3])))
            if(line.startswith("f")):
                f = line.split(" ")
                faces.append([Vec3d(vertices[int(i)-1]) for i in f[1:]])
    return faces
