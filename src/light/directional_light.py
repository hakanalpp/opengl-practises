# CENG 487 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# December 2021

from src.light.light import Light
from src.vector import RGBA


class DirectionalLight(Light):

    def __init__(self, dirX, dirY, dirZ, color: 'RGBA'):
        Light.__init__(self, color, 1)
        self.direction = [dirX, dirY, dirZ]
