# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022


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
    print(" - I did not use the objects you gave in the assignment.")
    print(" - Because I did the Homework before you edited, and did 2 homeworks at once.")
    print(" - So, next week's homework will be the same code unless I update it.")
    print("\n - 1st Resubmission changes (02-01-2022):")
    print("   - Turko-English language UI fixed.")
    print("   - Blinn fixed.")
    print("   - Camera significantly improved.")
    print("   - Spotlight added.")
    app.glutInit()


numpy.set_printoptions(precision=2)
numpy.set_printoptions(threshold=numpy.inf)
main()
