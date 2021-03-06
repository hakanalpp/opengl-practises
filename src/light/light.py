# CENG 487 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# January 2022

from src.vector import RGBA


class Light:
    def __init__(self, lightColor: 'RGBA', lightIntensity):
        self.lightColor = lightColor
        self.lightIntensity = lightIntensity

    def color_as_list(self):
        return self.lightColor.asList(1)
