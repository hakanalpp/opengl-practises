# CENG 487 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# November 2021

from .scene import Scene


class App:
    scene: 'Scene' = Scene()

    def draw_instructions(self):
        self.scene.draw_text("Hit ESC key to quit.", 20, -20)
        self.scene.draw_text("[1,2] Change objects", 20, -40)
        self.scene.draw_text("[Mouse Wheel] Zoom in/out", 20, -60)
        self.scene.draw_text("[Mouse Drag/Drop] Camera movements", 20, -80)
        self.scene.draw_text("[+/-] Increase/Decrease subdivisions", 20, -100)
