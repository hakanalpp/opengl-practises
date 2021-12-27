from src.vector import RGBA


class Light:
    def __init__(self, lightColor: 'RGBA', lightIntensity):
        self.lightColor = lightColor
        self.lightIntensity = lightIntensity

    def color_as_list(self):
        return self.lightColor.asList(1)
