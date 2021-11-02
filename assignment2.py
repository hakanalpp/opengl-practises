# CENG 487 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# November 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from vec3d import *
from mat3d import *
from objects.obj3d import *
from objects.cube import *

# Number of the glut window.
window = 0

# colors = sum([[255, 0, 0] for i in range(4)] + [[0, 255, 0] for i in range(4)] + [[0, 0, 255] for i in range(4)] +
# 			 [[255, 255, 0] for i in range(4)] + [[0, 255, 255] for i in range(4)] + [[255, 0, 255] for i in range(4)],[])
# vertices = [[Vec3d([ 1.0, 1.0,-1.0,1]), Vec3d([-1.0, 1.0,-1.0,1]), Vec3d([-1.0, 1.0, 1.0,1]), Vec3d([ 1.0, 1.0, 1.0,1])], # Top
# 			[Vec3d([ 1.0,-1.0, 1.0,1]), Vec3d([-1.0,-1.0, 1.0,1]), Vec3d([-1.0,-1.0,-1.0,1]), Vec3d([ 1.0,-1.0,-1.0,1])], # Bottom
# 			[Vec3d([ 1.0, 1.0, 1.0,1]), Vec3d([-1.0, 1.0, 1.0,1]), Vec3d([-1.0,-1.0, 1.0,1]), Vec3d([ 1.0,-1.0, 1.0,1])], # Front
# 			[Vec3d([ 1.0,-1.0,-1.0,1]), Vec3d([-1.0,-1.0,-1.0,1]), Vec3d([-1.0, 1.0,-1.0,1]), Vec3d([ 1.0, 1.0,-1.0,1])], # Back
# 			[Vec3d([-1.0, 1.0, 1.0,1]), Vec3d([-1.0, 1.0,-1.0,1]), Vec3d([-1.0,-1.0,-1.0,1]), Vec3d([-1.0,-1.0, 1.0,1])], # Left
# 			[Vec3d([ 1.0, 1.0,-1.0,1]), Vec3d([ 1.0, 1.0, 1.0,1]), Vec3d([ 1.0,-1.0, 1.0,1]), Vec3d([ 1.0,-1.0,-1.0,1])]]  # Right
o1 = Cube3d(Vec3d(0,0,0,1))
objects = [o1]

# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
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

	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

def drawObjects():
	for obj in objects:
		for i in range(len(obj.vertices)):
			ind = [j for j in range(len(obj.vertices[i]))]
			glColorPointer( 3, GL_UNSIGNED_BYTE, 0, obj.colors[i] )
			glVertexPointer(4,GL_FLOAT, 0, [o.v for o in obj.vertices[i]])
			glEnableClientState(GL_VERTEX_ARRAY)
			glEnableClientState(GL_COLOR_ARRAY)
			glDrawElementsui(
				GL_LINE_LOOP,  # GL_QUADS or GL_LINE_LOOP
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
			obj.vertices[i] = rotateMatrix_x(obj.vertices[i],-0.025)
			obj.vertices[i] = rotateMatrix_y(obj.vertices[i],0.030)
			obj.vertices[i] = rotateMatrix_z(obj.vertices[i],0.028)

	glutPostRedisplay()

def keyPressed(key, x, y):
	if ord(key) == 27:
		glutLeaveMainLoop()
		return

def mouseMoved(key, x, y, z):
	if key != 3 and key != 4:
		return
	for obj in objects:
		if key == 3:
			scaleObj(obj,1.05, 1.05, 1.05)
		elif key == 4:
			scaleObj(obj,0.95, 0.95, 0.95)
	glutPostRedisplay()

m = []
def drag(x, y):
	m.append((x,y))
	if(len(m) == 2):
		xVec = m[1][0] - m[0][0]
		yVec = m[1][1]- m[0][1]

		if(xVec > 10): xVec = 10
		elif(xVec < -10): xVec = -10
		if(yVec > 10): yVec = 10
		if(yVec < -10): yVec = -10

		for obj in objects:
			rotateObj_x(obj, yVec/150)
			rotateObj_y(obj, xVec/150)
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
	glutReshapeFunc(ReSizeGLScene)	# Register the function called when our window is resized.
	glutKeyboardFunc(keyPressed) # Register the function called when the keyboard is pressed.
	glutMouseFunc(mouseMoved)
	glutMotionFunc(drag)	

	glutCreateMenu(SelectFromMenu)
	glutAddMenuEntry("Rotate using mouse", 1)
	glutAddMenuEntry("Rotate over time", 2)
	glutAttachMenu(GLUT_RIGHT_BUTTON)

	InitGL(640, 480) # Initialize our window.

	glutMainLoop()	# Start Event Processing Engine

print ("Hit ESC key to quit.")
main()