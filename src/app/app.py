# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

from .scene import Scene


class App:
    def __init__(self):
        self.scene = Scene()
        self.m = None
        self.frameCount = 0
        self.second = 0
        self.undisplayedFrames = 0

    def glutInit(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

        glutInitWindowSize(640, 640)
        glutInitWindowPosition(200, 200)

        glutCreateWindow("Hakan Alp - Assignment 6")
        self.scene.shader.init()
        self.scene.update_vertex_buffer()

        glEnable(GL_DEPTH_TEST)

        glutDisplayFunc(self.draw)
        glutIdleFunc(self.idleFunc)
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
        self.scene.draw_text("[+/-] Blend textures", 20, -80)
        self.scene.draw_text("[a] Animate Point Light", 20, -100)
        self.scene.draw_text("[b] Toggle Blinn", 20, -120)
        self.scene.draw_text("[1/3] Toggle lights", 20, -140)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.scene.draw_text("FPS: {}".format(
            self.frameCount if self.frameCount < 300 else 300), -80, -20)
        self.draw_instructions()
        self.scene.draw()

        t = int(time.time() % 60)
        self.undisplayedFrames += 1
        if(self.second != t):
            self.second = t
            self.frameCount = self.undisplayedFrames
            self.undisplayedFrames = 0
        glutSwapBuffers()

    def ReSizeGLScene(self, Width, Height):
        self.scene.set_size(Width, Height)

    def keyPressed(self, key, x, y):
        if ord(key) == 27:
            glutLeaveMainLoop()
            return
        elif key == b'+':
            self.scene.increase_scale()
        elif key == b'-':
            self.scene.decrease_scale()
        elif key == b'a':
            self.scene.should_animate = not self.scene.should_animate
        elif key == b'1':
            self.scene.shader.pointLight.lightIntensity = 0.0 if self.scene.shader.pointLight.lightIntensity == 1.0 else 1.0
            self.scene.shader.initLightParams()
        elif key == b'2':
            self.scene.shader.directionalLight.lightIntensity = 0.0 if self.scene.shader.directionalLight.lightIntensity == 1.0 else 1.0
            self.scene.shader.initLightParams()
        elif key == b'3':
            self.scene.shader.spotLight.lightIntensity = 0.0 if self.scene.shader.spotLight.lightIntensity == 1.0 else 1.0
            self.scene.shader.initLightParams()
        elif key == b'b':
            self.scene.shader.blinn = not self.scene.shader.blinn
            self.scene.shader.initLightParams()

    def specialKeyPressed(self, key, x, y):
        pass
        # if key == GLUT_KEY_LEFT:
        #     self.scene.transform_objects(Matrix.rotateY(-0.06))
        # elif key == GLUT_KEY_RIGHT:
        #     self.scene.transform_objects(Matrix.rotateY(0.06))
        # elif key == GLUT_KEY_UP:
        #     self.scene.transform_objects(Matrix.rotateX(-0.06))
        # elif key == GLUT_KEY_DOWN:
        #     self.scene.transform_objects(Matrix.rotateX(0.06))

    def mousePressed(self, key, x, y, z):
        if key != 3 and key != 4:
            return
        if key == 3:
            self.scene.camera.zoom(0.15)
        elif key == 4:
            self.scene.camera.zoom(-0.15)

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
            self.scene.shader.initLightParams()
        self.m = (x, y)

    def idleFunc(self):
        if(self.scene.should_animate):
            self.scene.rotate_point_light_y(0.035)
            self.scene.rotate_spot_light(0.025)

            self.scene.shader.initLightParams()
            self.scene.update_vertex_buffer()
        self.draw()
