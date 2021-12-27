from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from PIL import Image
import numpy


class Texture:
    def __init__(self, programId):
        self.programId = programId
        self.texId = 0
        self.id = 0

    def initTexture(self, texFileName, bufferName):
        self.initUVs(texFileName, bufferName)

    def initUVs(self, texFilename, bufferName):
        # we need to bind to the program to set texture related params
        glUseProgram(self.programId)

        # load texture
        self.texId = self.loadTexture(texFilename)

        # set shader stuff
        tex1Location = glGetUniformLocation(self.programId, bufferName)
        glUniform1i(tex1Location, self.id)
        self.id += 1

        # now activate texture units
        glActiveTexture(GL_TEXTURE0 + self.texId)
        glBindTexture(GL_TEXTURE_2D, self.texId)

        # reset program
        glUseProgram(0)

    def loadTexture(self, texFilename):
        # load texture - flip int verticallt to convert from pillow to OpenGL orientation
        image = Image.open(texFilename).transpose(Image.FLIP_TOP_BOTTOM)

        # create a new id
        texID = glGenTextures(1)
        # bind to the new id for state

        glBindTexture(GL_TEXTURE_2D, texID)

        # set texture params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # copy texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                     numpy.frombuffer(image.tobytes(), dtype=numpy.uint8))
        glGenerateMipmap(GL_TEXTURE_2D)

        return texID
