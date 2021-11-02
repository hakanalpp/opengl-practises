# CENG 487 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# October 2021

from mat3d import *

class Object3d:
    def __init__(self, *args):
        if(len(args) == 0): # Set default as unit vector
            self.vertices = []
            self.colors = []
        elif (len(args) == 2):
            self.vertices = args[0]
            self.colors = args[1]
        self.transformations = []
        
    def addVertice(self, vertice):
        self.vertices.append(vertice)
    
    def addTransformation(self, transformation):
        self.transformations.append(transformation)

def scaleObj(obj, sX, sY, sZ):
    k = obj.vertices
    for i in range(len(k)):
        for j in range(len(obj.vertices[i])):
            obj.vertices[i][j] = multiplyVector(scaleMatrix(sX, sY, sZ), obj.vertices[i][j])
    obj.addTransformation(scaleMatrix(sX, sY, sZ))
    obj.vertices = k

def rotateObj_x(obj, theta):
    for i in range(len(obj.vertices)):
        for j in range(len(obj.vertices[i])):
            obj.vertices[i][j] = multiplyVector(rotateMatrix_x(theta), obj.vertices[i][j])
    obj.addTransformation(rotateMatrix_x(theta))

def rotateObj_y(obj, theta):    
    for i in range(len(obj.vertices)):
        for j in range(len(obj.vertices[i])):
            obj.vertices[i][j] = multiplyVector(rotateMatrix_y(theta), obj.vertices[i][j])
    obj.addTransformation(rotateMatrix_y(theta))

def rotateObj_z(obj, theta):
    for i in range(len(obj.vertices)):
        for j in range(len(obj.vertices[i])):
            obj.vertices[i][j] = multiplyVector(rotateMatrix_z(theta), obj.vertices[i][j])
    obj.addTransformation(rotateMatrix_z(theta))
