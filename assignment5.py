# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy

from src.app import App
from src.matrix import Matrix
from src.shape import Box
from src.shape.object import Object3D
from src.utils.fileIO import *

app = App()
box1 = Box(0.5, 0.5, 0.5)
box2 = Box(0.5, 1, 0.5)
box2.move(-2, 1, -1)

toriobj = Object3D("tori.obj")
toriobj.rotate(Matrix.rotateX(250))
toriobj.rotate(Matrix.rotateY(210))
toriobj.scale(0.25, 0.25, 0.25)
toriobj.move(1.5, 1.75, 2)

sphereobj = Object3D("sphere.obj")
sphereobj.move(2, 1.5, -2)

app.scene.add_object(box1)
app.scene.add_object(box2)
app.scene.add_object(toriobj)
app.scene.add_object(sphereobj)


def main():
    app.glutInit()


numpy.set_printoptions(precision=3)
main()
