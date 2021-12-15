# CENG 487 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ..matrix import Matrix
from .scene import Scene


class App:
    def __init__(self):
        self.scene = Scene()
        self.m = None

    def glutInit(self):
        glutInit(sys.argv)

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

        glutInitWindowSize(640, 640)
        glutInitWindowPosition(200, 200)

        glutCreateWindow("Hakan Alp - Assignment 5")
        self.scene.shader.init()
        self.scene.add_vertex_buffer()

        glEnable(GL_DEPTH_TEST)

        glutDisplayFunc(self.draw)
        glutReshapeFunc(self.ReSizeGLScene)
        glutKeyboardFunc(self.keyPressed)
        glutSpecialFunc(self.specialKeyPressed)
        glutMouseFunc(self.mousePressed)
        glutMotionFunc(self.mouseMove)

        glutMainLoop()

    def draw_instructions(self):
        self.scene.draw_text("Hit ESC key to quit.", 20, -20)
        self.scene.draw_text("[Mouse Wheel] Zoom in/out", 20, -40)
        self.scene.draw_text("[Mouse Drag/Drop] Camera movements", 20, -60)
        self.scene.draw_text("[+/-] Increase/Decrease subdivisions", 20, -80)
        self.scene.draw_text(
            "[Arrow Keys] Rotate objects around origin", 20, -100)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_instructions()
        self.scene.draw()
        glutSwapBuffers()

    def ReSizeGLScene(self, Width, Height):
        self.scene.set_size(Width, Height)

    def keyPressed(self, key, x, y):
        if ord(key) == 27:
            glutLeaveMainLoop()
            return
        elif key == b'+':
            self.scene.increase_subdivision()
        elif key == b'-':
            self.scene.decrease_subdivision()
        glutPostRedisplay()

    def specialKeyPressed(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.scene.transform_objects(Matrix.rotateY(-0.06))
        elif key == GLUT_KEY_RIGHT:
            self.scene.transform_objects(Matrix.rotateY(0.06))
        elif key == GLUT_KEY_UP:
            self.scene.transform_objects(Matrix.rotateX(-0.06))
        elif key == GLUT_KEY_DOWN:
            self.scene.transform_objects(Matrix.rotateX(0.06))
        glutPostRedisplay()

    def mousePressed(self, key, x, y, z):
        if key != 3 and key != 4:
            return
        if key == 3:
            self.scene.camera.zoom(0.15)
        elif key == 4:
            self.scene.camera.zoom(-0.15)
        glutPostRedisplay()

    def mouseMove(self, x, y):
        m = self.m
        if(m != None):
            xVec = m[0] - x
            yVec = m[1] - y

            if(xVec > 10):
                xVec = 10
            elif(xVec < -10):
                xVec = -10
            if(yVec > 10):
                yVec = 10
            if(yVec < -10):
                yVec = -10

            self.scene.camera.yaw(-xVec/250)
            self.scene.camera.pitch(-yVec/250)

            glutPostRedisplay()
        self.m = (x, y)
