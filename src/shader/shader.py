from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np

from src.light.directional_light import DirectionalLight
from src.light.point_light import PointLight
from src.shader.texture import Texture
from src.vector import RGBA


class Shader:
    def __init__(self, camera):
        self.VBO = None
        self.programID = None
        self.vertexDim = 4
        self.nVertices = 4
        self.camera = camera
        self.texture = None
        self.texScale = 0.0
        self.pointLight = PointLight(1.3, 1.54, 0.0, RGBA(1, 1, 1, 1))
        self.directionalLight = DirectionalLight(1, 1, 0, RGBA(1, 0, 0, 1))
        self.blinn = False

    def init(self):
        self.initProgram()
        self.initVertexBuffer(np.array([], dtype="float32"), 0)
        self.texture = Texture(self.programID)
        self.initLightParams()
        self.texture.initTexture("texture1.png", "tex1")
        self.texture.initTexture("texture2.png", "tex2")

    def initProgram(self):
        shaderList = []

        shaderList.append(self.createShader(
            GL_VERTEX_SHADER, self.readShader("src/shader/model.vert")))
        shaderList.append(self.createShader(
            GL_FRAGMENT_SHADER, self.readShader("src/shader/model.frag")))

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

    def initVertexBuffer(self, vertexArr, faceCount):
        self.VBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        elementSize = np.dtype(np.float32).itemsize
        self.nVertices = faceCount * 4

        glBufferData(
            GL_ARRAY_BUFFER,
            len(vertexArr)*elementSize,
            vertexArr,
            GL_STATIC_DRAW
        )

        offset = 0

        glVertexAttribPointer(0, self.vertexDim, GL_FLOAT, GL_FALSE,
                              elementSize * self.vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)  # Vertices

        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(1, self.vertexDim, GL_FLOAT, GL_FALSE,
                              elementSize * self.vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)  # Colors

        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(2, self.vertexDim, GL_FLOAT, GL_FALSE,
                              elementSize * 2, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(2)  # UVs

        offset += elementSize * 2 * self.nVertices
        glVertexAttribPointer(3, self.vertexDim, GL_FLOAT, GL_FALSE,
                              elementSize * self.vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(3)  # Normals

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def display(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)

        glUseProgram(self.programID)

        viewLocation = glGetUniformLocation(self.programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE,
                           self.camera.getViewMatrix())

        projLocation = glGetUniformLocation(self.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE,
                           self.camera.getProjMatrix())

        texScaleLocation = glGetUniformLocation(self.programID, "texScale")
        glUniform1fv(texScaleLocation, 1, self.texScale)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        glDrawArrays(GL_QUADS, 0, self.nVertices)

        glBindVertexArray(0)
        glUseProgram(0)

    def initLightParams(self):
        programID = self.programID

        glUseProgram(programID)

        viewPosLocation = glGetUniformLocation(programID, "viewPos")
        glUniform3f(viewPosLocation, *self.camera.eye.asList()[:3])

        blinnLocation = glGetUniformLocation(programID, "blinn")
        glUniform1i(blinnLocation, self.blinn)

        pLightPosLocation = glGetUniformLocation(programID, "pointLightPos")
        glUniform3f(pLightPosLocation, *self.pointLight.lightPos.asList()[:3])
        pLightColorLocation = glGetUniformLocation(
            programID, "pointLightColor")
        glUniform4f(pLightColorLocation, *self.pointLight.color_as_list())
        pLightIntensityLocation = glGetUniformLocation(
            programID, "pointLightIntensity")
        glUniform1f(pLightIntensityLocation, self.pointLight.lightIntensity)

        dLightPosDirection = glGetUniformLocation(
            programID, "directionalLightDir")
        glUniform3f(dLightPosDirection, self.directionalLight.direction[0],
                    self.directionalLight.direction[1], self.directionalLight.direction[2])
        dLightColorLocation = glGetUniformLocation(
            programID, "directionalLightColor")
        glUniform4f(dLightColorLocation, *
                    self.directionalLight.color_as_list())
        dLightIntensityLocation = glGetUniformLocation(
            programID, "directionalLightIntensity")
        glUniform1f(dLightIntensityLocation,
                    self.directionalLight.lightIntensity)

        glUseProgram(0)

    def readShader(self, filename):
        with open(filename, 'r') as file:
            return file.read()
