# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021


import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from src.app import App
from src.shape import Object3D
from src import Matrix
from src.utils.fileIO import *

app = App()
o1 = Object3D("./ecube.obj")
o2 = Object3D("./tori.obj")


def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    global app
    app.scene.set_size(Width, Height)


def drawObjects():
    global app
    app.draw_instructions()
    app.scene.draw()


def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 0.0, 3.0)
    glTranslatef(0.0, 0.0, -4.0)
    drawObjects()
    glutSwapBuffers()


def keyPressed(key, x, y):
    if ord(key) == 27:
        glutLeaveMainLoop()
        return
    elif key == b'+':
        app.scene.increase_subdivision()
    elif key == b'-':
        app.scene.decrease_subdivision()
    elif key == b'1':
        app.scene.objects.pop()
        app.scene.add_object(o1)
    elif key == b'2':
        app.scene.objects.pop()
        app.scene.add_object(o2)
    glutPostRedisplay()


def mouseMoved(key, x, y, z):
    global app

    if key != 3 and key != 4:
        return
    if key == 3:
        app.scene.translate_camera(Matrix.scale(1.05, 1.05, 1.05))
    elif key == 4:
        app.scene.translate_camera(Matrix.scale(0.95, 0.95, 0.95))
    glutPostRedisplay()


m = []


def drag(x, y):
    global app

    m.append((x, y))
    if(len(m) == 2):
        xVec = m[1][0] - m[0][0]
        yVec = m[1][1] - m[0][1]

        if(xVec > 10):
            xVec = 10
        elif(xVec < -10):
            xVec = -10
        if(yVec > 10):
            yVec = 10
        if(yVec < -10):
            yVec = -10

        app.scene.translate_camera(Matrix.rotateX(
            yVec/250) @ Matrix.rotateY(xVec/250))
        m.pop(0)
        glutPostRedisplay()


def initGlut():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Hakan Alp - Assignment 3")
    glutDisplayFunc(DrawGLScene)

    glutReshapeFunc(ReSizeGLScene)
    glutIdleFunc(drawObjects)

    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouseMoved)
    glutMotionFunc(drag)

    InitGL(640, 480)
    glutMainLoop()


def main():
    global app
    app.scene.add_object(o1)
    app.scene.translate_camera(Matrix.scale(0.5, 0.5, 0.5))
    initGlut()


print("Improvements since last submission:")
print("\t- App, Camera, and Scene classes created.")
print("\t- Instructions are printed to the screen.")
main()
