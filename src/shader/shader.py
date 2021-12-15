from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

# from src.app import Camera


class Shader:
    def __init__(self, camera):
        self.VBO = None
        self.programID = None
        self.vertexDim = 4
        self.nVertices = 4
        self.camera = camera

    def init(self):
        self.initProgram()
        self.initVertexBuffer(np.array(
            [],
            dtype='float32'
        ), np.array(
            [],
            dtype='float32'
        ))

    def initProgram(self):
        shaderList = []

        shaderList.append(self.createShader(
            GL_VERTEX_SHADER, self.readShader("src/shader/vertex.txt")))
        shaderList.append(self.createShader(
            GL_FRAGMENT_SHADER, self.readShader("src/shader/fragment.txt")))

        self.programID = self.createProgram(shaderList)
        for shader in shaderList:
            glDeleteShader(shader)

    def createShader(self, shaderType, shaderCode):
        shaderID = glCreateShader(shaderType)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)

        status = None
        glGetShaderiv(shaderID, GL_COMPILE_STATUS, status)
        if status == GL_FALSE:
            # Note that getting the error log is much simpler in Python than in C/C++
            # and does not require explicit handling of the string buffer
            strInfoLog = glGetShaderInfoLog(shaderID)
            strShaderType = ""
            if shaderType is GL_VERTEX_SHADER:
                strShaderType = "vertex"
            elif shaderType is GL_GEOMETRY_SHADER:
                strShaderType = "geometry"
            elif shaderType is GL_FRAGMENT_SHADER:
                strShaderType = "fragment"
            print(b"Compilation failure for " +
                  strShaderType + b" shader:\n" + strInfoLog)
        return shaderID

    def createProgram(self, shaderList):
        programID = glCreateProgram()
        for shader in shaderList:
            glAttachShader(programID, shader)

        glLinkProgram(programID)

        status = glGetProgramiv(programID, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(programID)
            print(b"Linker failure: \n" + strInfoLog)

        for shaderID in shaderList:
            glDetachShader(programID, shaderID)

        return programID

    def initVertexBuffer(self, vertexArr, colorArr):
        self.VBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        bufferData = np.concatenate((vertexArr, colorArr))
        elementSize = np.dtype(np.float32).itemsize
        self.nVertices = int(len(vertexArr)/4)

        glBufferData(
            GL_ARRAY_BUFFER,
            len(bufferData)*elementSize,
            bufferData,
            GL_STATIC_DRAW
        )

        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def display(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)

        glUseProgram(self.programID)

        viewLocation = glGetUniformLocation(self.programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE,
                           self.camera.getViewMatrix())

        projLocation = glGetUniformLocation(self.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE,
                           self.camera.getProjMatrix())

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        elementSize = np.dtype(np.float32).itemsize

        offset = 0
        glVertexAttribPointer(0, self.vertexDim, GL_FLOAT, GL_FALSE,
                              elementSize * self.vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(1, self.vertexDim, GL_FLOAT, GL_FALSE,
                              elementSize * self.vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)

        glDrawArrays(GL_QUADS, 0, self.nVertices)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glUseProgram(0)

    def readShader(self, filename):
        with open(filename, 'r') as file:
            return file.read()
