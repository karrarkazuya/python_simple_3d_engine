import random
from Simple3DEngine.Maths import Maths

class Poly:
    def __init__(self, face_color, edge_color, vertices, parent):
        super().__init__()
        self.id = random.randint(1, 10000000000)
        # can be green, yellow, blue or any color you want. you can even hex colors. "" for no color
        self.face_color = face_color
        self.edge_color = edge_color
        self.visible = True  # viability of a poly
        self.vertices = vertices
        self.scale = parent.scale
        self.distance = parent.distance

    """
    to check if this poly contains another poly
    """
    def contains_poly(self, poly):
        return Maths().poly_inside_poly(self.vertices, poly.vertices)

    """
    used in sorting method
    """
    def get_close_of_camera(self):
        closer = self.vertices[0][2]
        if self.vertices[1][2] > closer:
            closer = self.vertices[1][2]
        if self.vertices[2][2] > closer:
            closer = self.vertices[2][2]
        return closer

    def get_close_of_camera_by_avg(self):
        return (self.vertices[0][2] + self.vertices[1][2] + self.vertices[2][2]) / 3
