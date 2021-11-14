# CENG 487 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# November 2021

import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from src.shape import Object3D
from src import Mat3d
from src.utils.fileIO import *

# Number of the glut window.
window = 0

o1 = Object3D(generate_vertices("./src/objects/ecube.obj"))
o2 = Object3D(generate_vertices("./src/objects/tori.obj"))
objects = [o1]

# A general OpenGL initialization function.  Sets all of the initial parameters.


# We call this right after our OpenGL window is created.
def InitGL(Width, Height):
    # This Will Clear The Background Color To Black
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    # Reset The Current Viewport And Perspective Transformation
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def drawObjects():
    draw_text("Subdivision Count: {}".format(objects[0].subdivision))
    glEnableClientState(GL_VERTEX_ARRAY)
    for obj in objects:
        obj.draw()
    glDisableClientState(GL_VERTEX_ARRAY)


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
        for obj in objects:
            obj.increase_subdivision()
    elif key == b'-':
        for obj in objects:
            obj.decrease_subdivision()
    elif key == b'1':
        objects[0] = o1
    elif key == b'2':
        objects[0] = o2
    glutPostRedisplay()


def mouseMoved(key, x, y, z):
    if key != 3 and key != 4:
        return
    for obj in objects:
        if key == 3:
            obj.scale(1.05, 1.05, 1.05)
        elif key == 4:
            obj.scale(0.95, 0.95, 0.95)
    glutPostRedisplay()


m = []


def drag(x, y):
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

        for obj in objects:
            obj.rotate(Mat3d.rotateX(yVec/250))
            obj.rotate(Mat3d.rotateY(xVec/250))
        m.pop(0)
        glutPostRedisplay()


def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Hakan Alp - Assignment 3")
    glutDisplayFunc(DrawGLScene)
    # glutFullScreen()	# Uncomment this line to get full screen.
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    glutIdleFunc(drawObjects)
    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouseMoved)
    glutMotionFunc(drag)

    InitGL(640, 480)  # Initialize our window.

    glutMainLoop()  # Start Event Processing Engine


print("Hit ESC key to quit.\n")
print("[1,2] Change objects")
print("[Mouse Wheel] Zoom in/out")
print("[Mouse Drag/Drop] Camera movements")
print("[+/-] Increase/Decrease subdivisions")
main()
