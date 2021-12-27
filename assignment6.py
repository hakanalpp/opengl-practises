# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy

from src.app import App
from src.shape.object import Object3D
from src.utils.fileIO import *

app = App()

manifoldObj = Object3D("CornellManifold.obj")
manifoldObj.move(0, -24, 0)
manifoldObj.scale(0.065, 0.065, 0.065)
app.scene.add_object(manifoldObj)


def main():
    app.glutInit()


numpy.set_printoptions(precision=6)
numpy.set_printoptions(threshold=numpy.inf)
main()
