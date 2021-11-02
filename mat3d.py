# CENG 487 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# October 2021

from vec3d import *
from numpy import sin, cos
import numpy as np

# My matrix is in row major format which looks like this [[row1],[row2],[row3],[row4]]
class Mat3d:
    def __init__(self, *args):
        if len(args) == 4:
            self.m = [i for i in args]
        elif len(args) == 1:
            self.m = args[0]
        elif len(args) == 0:
            self.m = [[1.0,0,0,0],
                    [0,1.0,0,0],
                    [0,0,1.0,0],
                    [0,0,0,1.0]]
        else:
            print("There should be either 0, 1 or 4 args for creating Matrix.")
            sys.exit()
    
    def __str__(self):
        res = ""
        for i in self.m:
            res += "[{:.2f} {:.2f} {:.2f} {:.2f}]\n".format(*i)
        return res
    
    def __neg__(self):
        return Mat3d(np.linalg.inv(self.m))

    def __mul__(self, m2):
        m1 = self.m
        m2 = m2.m
        temp = [[0 for i in range(4)] for j in range(4)]
        for i1 in range(len(m1)):
            for i2 in range(len(m2)):
                for i2_2 in range(len(m2)):
                    temp[i1][i2] += m1[i1][i2_2] * m2[i2_2][i2]
        return Mat3d(temp)
  
    def transpose(self):
        matrix = self.m
        tempMatrix = []
        for j in range(4):
            row = []
            for i in range(4):
                row.append(matrix[i][j])
            tempMatrix.append(row)

        return Mat3d(tempMatrix)

def multiplyVector(matrix1, vector1):
    m1 = matrix1.m
    v1 = vector1.v
    tempV = [0 for i in range(4)]
    for i in range(len(m1)):
        res = 0
        for j in range(len(v1)):
            res += v1[j] * m1[i][j]
        tempV[i] = res
    return Vec3d(tempV)

def scaleMatrix(sX, sY, sZ):
    return Mat3d([[sX, 0, 0, 0],
                [0, sY, 0, 0],
                [0, 0, sZ, 0],
                [0, 0, 0, 1]])

def rotateMatrix_x(theta):
    return Mat3d([[1, 0, 0, 0],
                [0, cos(theta), -sin(theta), 0],
                [0, sin(theta), cos(theta), 0],
                [0, 0, 0, 1]])

def rotateMatrix_y(theta):
    return Mat3d([[cos(theta), 0, sin(theta), 0],
                [0, 1, 0, 0],
                [-sin(theta), 0, cos(theta), 0],
                [0, 0, 0, 1]])

def rotateMatrix_z(theta):
    return Mat3d([[cos(theta), -sin(theta), 0, 0],
            [sin(theta), cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

def translateMatrix(*args):
    if len(args) == 4:
        translationMatrix = Mat3d([[1, 0, 0, args[1]],
                    [0, 1, 0, args[2]],
                    [0, 0, 1, args[3]],
                    [0, 0, 0, 1]])
        return multiplyVector(translationMatrix, args[0])
    if len(args) == 2:
        translationMatrix = Mat3d([[1, 0, 0, args[1].x],
            [0, 1, 0, args[1].y],
            [0, 0, 1, args[1].z],
            [0, 0, 0, 1]])
        return multiplyVector(translationMatrix, args[0])