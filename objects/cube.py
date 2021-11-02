# CENG 487 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# October 2021

from mat3d import *
from objects.obj3d import *
from vec3d import *
import numpy as np

defaultCube = [[Vec3d([ 0.5, 0.5,-0.5,1]), Vec3d([-0.5, 0.5,-0.5,1]), Vec3d([-0.5, 0.5, 0.5,1]), Vec3d([ 0.5, 0.5, 0.5,1])], # Top
			   [Vec3d([ 0.5,-0.5, 0.5,1]), Vec3d([-0.5,-0.5, 0.5,1]), Vec3d([-0.5,-0.5,-0.5,1]), Vec3d([ 0.5,-0.5,-0.5,1])], # Bottom
			   [Vec3d([ 0.5, 0.5, 0.5,1]), Vec3d([-0.5, 0.5, 0.5,1]), Vec3d([-0.5,-0.5, 0.5,1]), Vec3d([ 0.5,-0.5, 0.5,1])], # Front
			   [Vec3d([ 0.5,-0.5,-0.5,1]), Vec3d([-0.5,-0.5,-0.5,1]), Vec3d([-0.5, 0.5,-0.5,1]), Vec3d([ 0.5, 0.5,-0.5,1])], # Back
			   [Vec3d([-0.5, 0.5, 0.5,1]), Vec3d([-0.5, 0.5,-0.5,1]), Vec3d([-0.5,-0.5,-0.5,1]), Vec3d([-0.5,-0.5, 0.5,1])], # Left
			   [Vec3d([ 0.5, 0.5,-0.5,1]), Vec3d([ 0.5, 0.5, 0.5,1]), Vec3d([ 0.5,-0.5, 0.5,1]), Vec3d([ 0.5,-0.5,-0.5,1])]] # Right

def generateColors(size):
    return [np.random.randint(256,size=3).tolist()*4 for i in range(size)]

class Cube3d(Object3d):
    centralPoint = Vec3d(0,0,0,1)
    def __init__(self, *args):
        if len(args) == 0:
            self.vertices = [[translateMatrix(i, centralPoint) for i in defaultCube[j]] for j in range(len(defaultCube))]
        if (len(args) == 1): # Set default as unit vector
            centralPoint = args[0]
            self.vertices = [[translateMatrix(i, centralPoint) for i in defaultCube[j]] for j in range(len(defaultCube))]
        self.colors = generateColors(6)
        self.transformations = []
        
