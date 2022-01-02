# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from src.light.light import Light
from src.vector import RGBA, Point3f, Vector3f


class SpotLight(Light):

    def __init__(self, x, y, z, dirX, dirY, dirZ, angle, color: 'RGBA'):
        Light.__init__(self, color, 1)
        self.position = Point3f(x, y, z)
        self.direction = Vector3f(dirX, dirY, dirZ)
        self.angle = angle
