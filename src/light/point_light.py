# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from src.light.light import Light
from src.vector import RGBA, Point3f


class PointLight(Light):

    def __init__(self, x, y, z, color: 'RGBA'):
        Light.__init__(self, color, 1)
        self.position = Point3f(x, y, z)
