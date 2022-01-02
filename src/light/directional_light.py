# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from src.light.light import Light
from src.vector import RGBA, Vector3f


class DirectionalLight(Light):

    def __init__(self, dirX, dirY, dirZ, color: 'RGBA'):
        Light.__init__(self, color, 1)
        self.direction = Vector3f(dirX, dirY, dirZ)
