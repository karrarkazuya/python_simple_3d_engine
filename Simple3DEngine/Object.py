import math
import random

class Object:
    def __init__(self):
        super().__init__()
        # can be green, yellow, blue or any color you want. you can even hex colors. "" for no color
        self.id = random.randint(1, 10000000000)
        self.face_color = ""
        self.edge_color = "black"
        self.title = ""
        self.scale = 250
        self.distance = 8
        self.mem_vertices = []
        self.mem_points = []
        self.mem_polies = []
        self.mem_vertices = []
        self.force_show = False
        # could be "avg", "closer" or "none", this is used to sort which vertices to render above which
        self.sort_method = "avg"

    '''
    @param file: the ply file to import, should be in same project folder, example "monkey.ply"
    used to read the ply and set the coordinates and the polies
    '''
    def import_ply(self, file, xtitle=""):
        self.title = xtitle
        points = []
        polies = []

        with open(file, 'r') as f:
            lines = f.readlines()
            points_start = False
            polies_start = False
            for line in lines:

                if "end_header" in line:
                    points_start = True
                    continue

                if points_start:
                    coordinates = line.split(' ')
                    if len(coordinates) == 4:
                        points_start = False
                        polies_start = True
                        new_coordinates = []
                        for coord in coordinates[1:4]:
                            new_coordinates.append(int(coord))
                        polies.append(new_coordinates)
                        continue
                    points.append([float(coordinates[0]), float(coordinates[1]), float(coordinates[2])])

                if polies_start:
                    coordinates = line.split(' ')
                    new_coordinates = []
                    for coord in coordinates[1:4]:
                        new_coordinates.append(int(coord))
                    polies.append(new_coordinates)
            f.close()

        self.mem_points = points
        self.mem_polies = polies

    '''
    @param angle: the angle to rotate with
    to rotate around Y
    '''

    def rotate_y(self, angle=0.5):
        angle = angle / 450 * 180 / math.pi
        for i, point in enumerate(self.mem_points):
            x = point[0] * math.cos(angle) - point[2] * math.sin(angle)
            y = point[1]
            z = point[2] * math.cos(angle) + point[0] * math.sin(angle)
            self.mem_points[i] = (x, y, z)

    '''
    @param angle: the angle to rotate with
    to rotate around X
    '''

    def rotate_x(self, angle=0.5):
        angle = angle / 450 * 180 / math.pi
        for i, point in enumerate(self.mem_points):
            x = point[0]
            y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
            z = point[2] * math.cos(angle) + point[1] * math.sin(angle)
            self.mem_points[i] = (x, y, z)

    '''
    @param angle: the angle to rotate with
    to rotate around Z
    '''

    def rotate_z(self, angle=0.5):
        angle = angle / 450 * 180 / math.pi
        for i, point in enumerate(self.mem_points):
            x = point[0] * math.cos(angle) + point[1] * math.sin(angle)
            y = point[1] * math.cos(angle) - point[0] * math.sin(angle)
            z = point[2]
            self.mem_points[i] = (x, y, z)

    '''
    @param amount: the amount to scale with
    to scale the rendered object
    '''

    def scale(self, amount):
        self.scale = self.scale + amount

    '''
    @param direction: can be x, y or z
    to move the rendered object towards the direction
    '''

    def move(self, direction, amount):
        i = 0
        while i < len(self.mem_points):
            point = self.mem_points[i]
            x = point[0]
            y = point[1]
            z = point[2]
            if direction == "x":
                x = x + amount
            if direction == "y":
                y = y + amount
            if direction == "z":
                z = z + amount
            self.mem_points[i] = [x, y, z]
            i = i + 1