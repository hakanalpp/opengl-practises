# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

import numpy as np

from ..vector import HCoord, Point3f, Vector3f
from ..matrix import Matrix


class Camera:
    def __init__(self):
        self.eye = Point3f(0.0, 0.0, 0.0)
        self.center = Vector3f(0.0, 0.0, 0.0)
        self.up = Vector3f(0.0, 0.0, 0.0)

        self.fov = 45.0
        self.near = 0.1
        self.far = 10000.0
        self.aspect = 1.0
        self.cameraX = Vector3f(0.0, 0.0, 0.0)
        self.cameraY = Vector3f(0.0, 0.0, 0.0)
        self.cameraZ = Vector3f(0.0, 0.0, 0.0)

        self.createView(Point3f(0.0, 0.0, 10.0),
                        Point3f(0.0, 0.0, 0.0),
                        Vector3f(0.0, 1.0, 0.0))

    def createView(self, eyePoint, centerPoint, upVector):
        self.eye = eyePoint
        self.orgEye = eyePoint

        self.center = centerPoint
        self.orgCenter = centerPoint

        self.up = upVector
        self.orgUp = upVector

        self.computeCamSpace()

    def camDistance(self):
        view = self.eye - self.center
        return view.len()

    def preDolly(self, x, y, z):
        unCam = self.unRotateCam()
        traCam = Matrix.translation(x, y, z)
        toCam = self.rotateCam()
        return Matrix.product3(unCam, traCam, toCam)

    def dolly(self, x, y, z):
        tx = self.preDolly(x, y, z)
        self.center = tx * self.center
        self.eye = tx * self.eye

    def zoom(self, z):
        tx = self.preDolly(0, 0, z)
        self.center = tx * self.center
        self.eye = tx * self.eye

    def dollyCamera(self, x, y, z):
        preViewVec = self.center - self.eye
        preViewVec = preViewVec.normalize()

        tx = self.preDolly(x, y, z)
        self.eye = tx * self.eye

        postViewVec: 'HCoord' = self.center - self.eye
        postViewVec = postViewVec.normalize()

        preViewVecYZ = Vector3f(0, preViewVec.y, preViewVec.z)
        preViewVecXZ = Vector3f(preViewVec.x, 0, preViewVec.z)
        postViewVecYZ = Vector3f(0, postViewVec.y, postViewVec.z)
        postViewVecXZ = Vector3f(postViewVec.x, 0, postViewVec.z)

        angleX = Vector3f.angleBetweenVectors(postViewVecYZ, preViewVecYZ)
        angleY = Vector3f.angleBetweenVectors(postViewVecXZ, preViewVecXZ)

        rot1 = Matrix.rotateX(-angleX)
        rot2 = Matrix.rotateY(-angleY)
        tmp1 = rot1 @ rot2
        self.up = tmp1 * self.up
        self.computeCamSpace()

    def dollyCenter(self, x, y, z):
        tx = self.preDolly(x, y, z)
        self.center = tx * self.center
        self.computeCamSpace()

    def pan(self, d):
        moveBack = Matrix.translation(self.eye.x, self.eye.y, self.eye.z)
        rot = self.rotCamY(d)
        move = Matrix.translation(-self.eye.x, -self.eye.y, -self.eye.z)

        tmp1 = Matrix.product3(moveBack, rot, move)

        self.center = tmp1 * self.center
        self.up = tmp1 * self.up

        self.computeCamSpace()

    def tilt(self, d):
        moveBack = Matrix.translation(self.eye.x, self.eye.y, self.eye.z)
        rot = self.rotCamX(d)
        move = Matrix.translation(-self.eye.x, -self.eye.y, -self.eye.z)

        tmp1 = Matrix.product3(moveBack, rot, move)

        self.center = tmp1 * self.center
        self.up = tmp1 * self.up

        self.computeCamSpace()

    def roll(self, d):
        moveBack = Matrix.translation(self.eye.x, self.eye.y, self.eye.z)
        rot = self.rotCamZ(d)
        move = Matrix.translation(-self.eye.x, -self.eye.y, -self.eye.z)

        tmp1 = Matrix.product3(moveBack, rot, move)

        self.center = tmp1 * self.center
        self.up = tmp1 * self.up

        self.computeCamSpace()

    def yaw(self, d):
        moveBack = Matrix.translation(
            self.center.x, self.center.y, self.center.z)
        rot = self.rotCamY(d)
        move = Matrix.translation(-self.center.x, -
                                  self.center.y, -self.center.z)

        tmp1 = Matrix.product3(moveBack, rot, move)

        self.eye = tmp1 * self.eye
        self.up = tmp1 * self.up

        self.computeCamSpace()

    def pitch(self, d):
        moveBack = Matrix.translation(
            self.center.x, self.center.y, self.center.z)
        rot = self.rotCamX(d)
        move = Matrix.translation(-self.center.x, -
                                  self.center.y, -self.center.z)

        tmp1 = Matrix.product3(moveBack, rot, move)

        self.eye = tmp1 * self.eye
        self.up = tmp1 * self.up

        self.computeCamSpace()

    def rotateCam(self):
        return Matrix([[self.cameraX.x, self.cameraX.y, self.cameraX.z, 0.0],
                       [self.cameraY.x, self.cameraY.y, self.cameraY.z, 0.0],
                       [self.cameraZ.x, self.cameraZ.y, self.cameraZ.z, 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

    def unRotateCam(self):
        return Matrix([[self.cameraX.x, self.cameraY.x, self.cameraZ.x, 0.0],
                       [self.cameraX.y, self.cameraY.y, self.cameraZ.y, 0.0],
                       [self.cameraX.z, self.cameraY.z, self.cameraZ.z, 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

    def rotCamX(self, a):
        unCam = self.unRotateCam()
        rotCam = Matrix.rotateX(a)
        toCam = self.rotateCam()

        return Matrix.product3(unCam, rotCam, toCam)

    def rotCamY(self, a):
        unCam = self.unRotateCam()
        rotCam = Matrix.rotateY(a)
        toCam = self.rotateCam()

        return Matrix.product3(unCam, rotCam, toCam)

    def rotCamZ(self, a):
        unCam = self.unRotateCam()
        rotCam = Matrix.rotateZ(a)
        toCam = self.rotateCam()

        return Matrix.product3(unCam, rotCam, toCam)

    def computeCamSpace(self):
        self.cameraZ = self.center - self.eye
        self.cameraZ = self.cameraZ.normalize()

        self.cameraX = self.cameraZ.crossProduct(self.up)
        self.cameraX = self.cameraX.normalize()

        self.cameraY = self.cameraX.crossProduct(self.cameraZ)

    def reset(self):
        self.eye = self.orgEye
        self.center = self.orgCenter
        self.up = self.orgUp
        self.computeCamSpace()

    def getViewMatrix(self):
        camZAxis = HCoord.normalize(
            HCoord(-self.eye.x, -self.eye.y, -self.eye.z, 0.0))
        camXAxis = camZAxis.crossProduct(self.up)
        camYAxis = camXAxis.crossProduct(camZAxis)

        rotMat = Matrix([[camXAxis.x, camYAxis.x, -camZAxis.x, 0.0],
                         [camXAxis.y, camYAxis.y, -camZAxis.y, 0.0],
                         [camXAxis.z, camYAxis.z, -camZAxis.z, 0.0],
                         [0.0, 0.0, 0.0, 1.0]])

        traMat = Matrix([[1.0, 0.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 1.0, 0.0],
                         [-self.eye.x, -self.eye.y, -self.eye.z, 1.0]])
        return (traMat @ rotMat).as_np()

    def getProjMatrix(self) -> 'Matrix':
        f = np.reciprocal(
            np.tan(np.divide(np.deg2rad(self.fov), 2.0)))
        base = self.near - self.far
        term_0_0 = np.divide(f, self.aspect)
        term_2_2 = np.divide(self.far + self.near, base)
        term_2_3 = np.divide(np.multiply(
            np.multiply(2, self.near), self.far), base)

        return Matrix([[term_0_0, 0.0, 0.0, 0.0],
                       [0.0, f, 0.0, 0.0],
                       [0.0, 0.0, term_2_2, -1],
                       [0.0, 0.0, term_2_3, 0.0]]).as_np()
