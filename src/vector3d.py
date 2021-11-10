# CENG 487 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# November 2021

import sys

from math import acos, pi


class Vec3d:
    def __init__(self, *args):
        if(len(args) == 1):
            if isinstance(args[0], self.__class__):  # Copy constructor
                self.v = args[0].v
            else:
                self.v = args[0]
        elif(len(args) == 3):  # Full argument constructor with a point
            self.v = [args[0], args[1], args[2], 1]
        elif(len(args) == 4):  # Full argument constructor for a point or vector
            self.v = [i for i in args]
        else:
            print("There should be either 1, 3 or 4 args for creating Vector.")
            sys.exit()
        self.x = self.v[0]
        self.y = self.v[1]
        self.z = self.v[2]
        self.w = self.v[3]

    def clone(self) -> 'Vec3d':
        return Vec3d(self)

    def normalize(self) -> 'Vec3d':
        l = self.length()
        return Vec3d(self.x/l, self.y/l, self.z/l, self.w)

    def length(self) -> 'float':
        return (self.x**2+self.y**2+self.z**2)**0.5

    def __str__(self) -> 'str':
        return "[{:.2f}, {:.2f}, {:.2f}, {:.2f}]".format(self.x, self.y, self.z, self.w)

    def __add__(self, v2) -> 'Vec3d':
        return Vec3d(self.x+v2.x, self.y+v2.y, self.z+v2.z, self.w)

    def __sub__(self, v2) -> 'Vec3d':
        return self + (-v2)

    def __neg__(self) -> 'Vec3d':
        return Vec3d(-self.x, -self.y, -self.z, self.w)

    def __mul__(self, i2):
        if isinstance(i2, self.__class__):  # dot product
            return self.x*i2.x + self.y*i2.y + self.z*i2.z
        elif isinstance(i2, int) or isinstance(i2, float):  # vector multiplication
            return Vec3d(self.x*i2, self.y*i2, self.z*i2, self.w)
        else:  # Matrix with Vector
            return i2 * self

    def __rmul__(self, i2) -> 'Vec3d':
        return Vec3d(self.x*i2, self.y*i2, self.z*i2, self.w)

    def crossProduct(self, v2) -> 'Vec3d':
        return self.crossProduct(self, v2)

    def projectionVec3(self, v2) -> 'Vec3d':  # Have not tested yet
        return self.projectionVec3(self, v2)

    def angleBetweenVectors(self, v2) -> 'float':  # Have not tested yet
        return self.angleBetweenVectors(self, v2)

    def middlePoint(self, v2) -> 'Vec3d':
        return self.middlePoint(self, v2)

    @staticmethod
    def crossProduct(v1, v2):
        return Vec3d(v1.y*v2.z-v1.z*v2.y,
                     v1.z*v2.x-v1.x*v2.z,
                     v1.x*v2.y-v1.y*v2.x,
                     v1.w)

    @staticmethod
    def projectionVec3(v1, v2):
        return v1*((v1*v2)/(v1.length()**2))

    @staticmethod
    def angleBetweenVectors(v1, v2):
        angle = acos((v1*v2)/(v1.length()*v2.length()))
        return (angle*180)/pi

    @staticmethod
    def middlePoint(v1, v2):
        return Vec3d((v1+v2)*0.5)
