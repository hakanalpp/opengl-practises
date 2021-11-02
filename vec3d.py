# CENG 487 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# October 2021

from numpy import arccos, pi, cos

class Vec3d:
    def __init__(self, *args):
        if(len(args) == 0): # Set default as unit vector
            self.v = [1,1,1,0]
        elif(len(args) == 1):
            self.v = args[0]
        elif(len(args) == 4):
            self.v = [i for i in args]
        else:
            print("There should be either 0, 1 or 4 args for creating Vector.")
            sys.exit()
        self.x = self.v[0]
        self.y = self.v[1]
        self.z = self.v[2]
        self.w = self.v[3]

    def normalize(self):
        l = self.length()
        return Vec3d(self.x/l, self.y/l, self.z/l, self.w)

    def length(self): 
        return (self.x**2+self.y**2+self.z**2)**0.5

    def __str__(self):
        res = ""
        for i in self.v:
            res += "[{:.2f}]\n".format(i)
        return res
        
    def __add__(self, v2):
        return Vec3d(self.x+v2.x, self.y+v2.y, self.z+v2.z, self.w)

    def __sub__(self, v2):
        return self + (-v2)

    def __neg__(self):
        return Vec3d(-self.x, -self.y, -self.z, self.w)

    def __mul__(self, i2):
        if isinstance(i2, self.__class__):
            return self.x*i2.x+ self.y*i2.y + self.z*i2.z
        elif isinstance(i2, int) or isinstance(i2, float):
            return Vec3d(self.x*i2, self.y*i2, self.z*i2, self.w) 
    
def crossProduct(v1, v2):
    return Vec3d(v1.y*v2.z-v1.z*v2.y,
                    v1.z*v2.x-v1.x*v2.z,
                    v1.x*v2.y-v1.y*v2.x,
                    v1.w)

def projectionVec3(v1, v2):
    return v1*((v1*v2)/(v1.length()**2))

def angleBetweenVectors(v1, v2):
    angle=arccos((v1*v2)/(v1.length()*v2.length()))
    return (angle*180)/pi