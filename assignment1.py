# CENG 487 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# November 2021

# I implemented 2 types of rotation.
# Rotation using your mouse with left click, and Rotation over time.
# Please do right click to change between them.
# I also implemented Zoom-in,Zoom-out option with your mouse wheel.
# Those features made me change the code and the objects a bit, sorry if this is not allowed.
# I also tested the transformation stack, but did not use for this assignment since I am not translating one by one.

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

from src.shape import Shape
from src import Point3f, Matrix

# Number of the glut window.
window = 0

colors = sum([[255, 0, 0] for i in range(4)] + [[0, 255, 0] for i in range(4)] + [[0, 0, 255] for i in range(4)] +
             [[255, 255, 0] for i in range(4)] + [[0, 255, 255] for i in range(4)] + [[255, 0, 255] for i in range(4)], [])
o1 = Shape([Point3f([1.0, 1.0, -1.0, 1]), Point3f([-1.0, 1.0, -1.0, 1]), Point3f([-1.0, 1.0, 1.0, 1]), Point3f([1.0, 1.0, 1.0, 1]),  # Top
            Point3f([1.0, -1.0, 1.0, 1]), Point3f([-1.0, -1.0, 1.0, 1]
                                                  ), Point3f([-1.0, -1.0, -1.0, 1]), Point3f([1.0, -1.0, -1.0, 1]),  # Bottom
            Point3f([1.0, 1.0, 1.0, 1]), Point3f([-1.0, 1.0, 1.0, 1]
                                                 ), Point3f([-1.0, -1.0, 1.0, 1]), Point3f([1.0, -1.0, 1.0, 1]),  # Front
            Point3f([1.0, -1.0, -1.0, 1]), Point3f([-1.0, -1.0, -1.0, 1]
                                                   ), Point3f([-1.0, 1.0, -1.0, 1]), Point3f([1.0, 1.0, -1.0, 1]),  # Back
            Point3f([-1.0, 1.0, 1.0, 1]), Point3f([-1.0, 1.0, -1.0, 1]
                                                  ), Point3f([-1.0, -1.0, -1.0, 1]), Point3f([-1.0, -1.0, 1.0, 1]),  # Left
            Point3f([1.0, 1.0, -1.0, 1]), Point3f([1.0, 1.0, 1.0, 1]), Point3f([1.0, -1.0, 1.0, 1]), Point3f([1.0, -1.0, -1.0, 1])], colors)  # Right
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


def drawObjects():
    for obj in objects:
        ind = [j for j in range(len(obj.vertices))]
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, colors)
        glVertexPointer(4, GL_FLOAT, 0, [o.v for o in obj.vertices])
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glDrawElementsui(
            GL_QUADS,
            ind
        )

# The main drawing function.


def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 0.0, 3.0)
    glTranslatef(0, 0.0, -10.0)
    drawObjects()
    glutSwapBuffers()


def animate():
    for obj in objects:
        for i in range(len(obj.vertices)):
            obj.vertices[i] *= Matrix.rotateX(-0.025)
            obj.vertices[i] *= Matrix.rotateY(0.030)
            obj.vertices[i] *= Matrix.rotateZ(0.028)

    glutPostRedisplay()


def keyPressed(key, x, y):
    if ord(key) == 27:
        glutLeaveMainLoop()
        return


def mouseMoved(key, x, y, z):
    if key != 3 and key != 4:
        return
    for obj in objects:
        for i in range(len(obj.vertices)):
            if key == 3:
                obj.vertices[i] *= Matrix.scale(1.05, 1.05, 1.05)
            elif key == 4:
                obj.vertices[i] *= Matrix.scale(0.95, 0.95, 0.95)
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
            for i in range(len(obj.vertices)):
                obj.vertices[i] *= Matrix.rotateX(yVec/150)
                obj.vertices[i] *= Matrix.rotateY(xVec/150)
        m.pop(0)
        glutPostRedisplay()


def SelectFromMenu(idCommand):
    if idCommand == 1:
        glutIdleFunc(None)
        glutMotionFunc(drag)
    else:
        glutIdleFunc(animate)
        glutMotionFunc(None)
    glutPostRedisplay()
    return idCommand


def main():
    global window
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Hakan Alp - Assignment 1")
    glutDisplayFunc(DrawGLScene)
    # glutFullScreen()	# Uncomment this line to get full screen.
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouseMoved)
    glutMotionFunc(drag)

    glutCreateMenu(SelectFromMenu)
    glutAddMenuEntry("Rotate using mouse", 1)
    glutAddMenuEntry("Rotate over time", 2)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

    InitGL(640, 480)  # Initialize our window.

    glutMainLoop()  # Start Event Processing Engine


print("Hit ESC key to quit.")
print("Dear sir, please read the comments on top of the main.py")
main()
