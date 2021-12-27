# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from src.light.light import Light
from src.vector import RGBA, Point3f


class PointLight(Light):

    def __init__(self, x, y, z, color: 'RGBA'):
        Light.__init__(self, color, 1)
        self.lightPos = Point3f(x, y, z)
