# CENG 487 Assignment#4 by
# Hakan Alp
# StudentId: 250201056
# December 2021


from ..matrix3d import Mat3d


class Camera:
    position = None

    def __init__(self, *args):
        if len(args) == 0:
            self.position = Mat3d()

    def translate(self, m: 'Mat3d'):
        self.position = m @ self.position
