# CENG 487 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# November 2021

import sys

from .vector3d import Vec3d
from math import sin, cos


# My matrix3d is in row major format which looks like this [[row1],[row2],[row3],[row4]]
class Mat3d:
    def __init__(self, *args):
        if len(args) == 4:
            self.m = [i for i in args]
        elif len(args) == 1:
            self.m = args[0]
        elif len(args) == 0:
            self.m = [[1.0, 0, 0, 0],
                      [0, 1.0, 0, 0],
                      [0, 0, 1.0, 0],
                      [0, 0, 0, 1.0]]
        else:
            print("There should be either 0, 1 or 4 args for creating Matrix.")
            sys.exit()

    def __str__(self) -> 'str':
        res = ""
        for i in self.m:
            res += "[{:.2f} {:.2f} {:.2f} {:.2f}]\n".format(*i)
        return res

    def invert(self) -> 'Mat3d':  # TODO
        return

    def __matmul__(self, m2) -> 'Mat3d':
        m1 = self.m
        m2 = m2.m
        temp = [[0 for i in range(4)] for j in range(4)]
        for i1 in range(len(m1)):
            for i2 in range(len(m2)):
                for i2_2 in range(len(m2)):
                    temp[i1][i2] += m1[i1][i2_2] * m2[i2_2][i2]
        return Mat3d(temp)

    def transpose(self) -> 'Mat3d':
        matrix3d = self.m
        tempMatrix = []
        for j in range(4):
            row = []
            for i in range(4):
                row.append(matrix3d[i][j])
            tempMatrix.append(row)

        return Mat3d(tempMatrix)

    def __mul__(self, v3d: 'Vec3d') -> 'Vec3d':
        m1 = self.m
        v1 = v3d.v
        tempV = [0 for i in range(4)]
        for i in range(len(m1)):
            res = 0
            for j in range(len(v1)):
                res += v1[j] * m1[i][j]
            tempV[i] = res
        return Vec3d(tempV)

    @staticmethod
    def translation(x, y, z) -> 'Mat3d':
        return Mat3d([[1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1]])

    @staticmethod
    def scale(sX, sY, sZ) -> 'Mat3d':
        return Mat3d([[sX, 0, 0, 0],
                      [0, sY, 0, 0],
                      [0, 0, sZ, 0],
                      [0, 0, 0, 1]])

    @staticmethod
    def rotateX(theta) -> 'Mat3d':
        return Mat3d([[1, 0, 0, 0],
                      [0, cos(theta), -sin(theta), 0],
                      [0, sin(theta), cos(theta), 0],
                      [0, 0, 0, 1]])

    @staticmethod
    def rotateY(theta) -> 'Mat3d':
        return Mat3d([[cos(theta), 0, sin(theta), 0],
                      [0, 1, 0, 0],
                      [-sin(theta), 0, cos(theta), 0],
                      [0, 0, 0, 1]])

    @staticmethod
    def rotateZ(theta) -> 'Mat3d':
        return Mat3d([[cos(theta), -sin(theta), 0, 0],
                      [sin(theta), cos(theta), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
