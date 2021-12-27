from src.light.light import Light
from src.vector import RGBA


class DirectionalLight(Light):

    def __init__(self, dirX, dirY, dirZ, color: 'RGBA'):
        Light.__init__(self, color, 1)
        self.direction = [dirX, dirY, dirZ]
