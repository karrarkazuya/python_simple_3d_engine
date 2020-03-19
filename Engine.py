from tkinter import Canvas, Frame, BOTH, Menu
import math

canvas = ""
height = 800
width = 1000
distance = 8
scale = 250

mem_points = []
mem_polies = []
mem_vertices = []

# colud be "avg", "closer" or "none", this is used to sort which vertices to render above which
method = "avg"

# can be green, yellow, blue or any color you want. you can even hex colors. "" for no color
face_color = ""
edge_color = "black"


class Engine(Frame):

    def __init__(self):
        super().__init__()

        self.init_engine()

    '''
    to initiate the engine
    '''
    def init_engine(self):
        global height, width, canvas

        self.master.title("3D simple engine")
        self.master.attributes("-topmost", True)
        self.master.resizable(False, False)
        self.pack(fill=BOTH, expand=1)

        self.geometry(str(width) + 'x' + str(height))  # for the size of the window

        self.set_ui()  # feel free to disable the ui

        # convas to hold the 3d renders
        if canvas == "":
            canvas = Canvas(self)
        canvas.pack(fill=BOTH, expand=1)

    '''
    to add simple control options
    '''
    def set_ui(self):
        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)

        option = Menu(menu_bar)
        option.add_command(label='Rotate <<', command=lambda: self.rotate_y(-0.5))
        option.add_command(label='Rotate >>', command=lambda: self.rotate_y(0.5))
        option.add_command(label='Rotate ^^', command=lambda: self.rotate_x(-0.5))
        option.add_command(label='Rotate down', command=lambda: self.rotate_x(0.5))
        menu_bar.add_cascade(label="Rotation", menu=option)

        option = Menu(menu_bar)
        option.add_command(label='Move >>', command=lambda: self.move('x', 0.2))
        option.add_command(label='Move <<', command=lambda: self.move('x', -0.2))
        option.add_command(label='Move ^^', command=lambda: self.move('y', -0.2))
        option.add_command(label='Move down', command=lambda: self.move('y', 0.2))
        menu_bar.add_cascade(label="Moving", menu=option)

        option = Menu(menu_bar)
        option.add_command(label='Scale ++', command=lambda: self.scale(1))
        option.add_command(label='Scale --', command=lambda: self.scale(-1))
        menu_bar.add_cascade(label="Scaling", menu=option)

    '''
    @param file: the ply file to import, should be in same project folder, example "monkey.ply"
    used to read the ply and set the coordinates and the polies
    '''
    def import_ply(self, file):
        global mem_points, mem_polies
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

        mem_points = points
        mem_polies = polies

    '''
    used to redraw all the vertices
    '''
    def vertices_reset(self):
        global mem_vertices

        for poly_0 in mem_vertices:
            triangle = []
            for poly_1 in poly_0:
                poly_1 = self.coordinator_3D(poly_1)
                triangle.append(poly_1[0])
                triangle.append(poly_1[1])
            self.create_poly(triangle)

    '''
    to sort arrays in a way to make the ones closer to the camera are the last to be rendered
    '''
    def sort_vertices(self):
        global mem_points, mem_polies, mem_vertices, method
        mem_vertices = []
        count = 0
        while count < len(mem_polies):
            if method == "none":
                mem_vertices.append([mem_points[mem_polies[count][0]], mem_points[mem_polies[count][1]], mem_points[mem_polies[count][2]]])
            if method == "avg":
                avg = mem_points[mem_polies[count][0]][2] + mem_points[mem_polies[count][1]][2] + mem_points[mem_polies[count][2]][2]
                avg = avg / 3
                mem_vertices.append([mem_points[mem_polies[count][0]], mem_points[mem_polies[count][1]], mem_points[mem_polies[count][2]], avg])
            if method == "closer":
                closer = mem_points[mem_polies[count][0]][2]
                if mem_points[mem_polies[count][1]][2] > closer:
                    closer = mem_points[mem_polies[count][1]][2]
                if mem_points[mem_polies[count][2]][2] > closer:
                    closer = mem_points[mem_polies[count][2]][2]

                mem_vertices.append([mem_points[mem_polies[count][0]], mem_points[mem_polies[count][1]],mem_points[mem_polies[count][2]], closer])
            count = count + 1
        if method != "none":
            mem_vertices.sort(key=lambda x: x[3], reverse = True)
            for higher in mem_vertices:
                higher.pop(3)



    '''
    @param points: array of coordinates in the form of [(x, y), (x, y) , (x, y)] representing a polly
    to create a single poly
    '''
    def create_poly(self, points):
        global canvas, face_color, edge_color
        if canvas == "":
            canvas = Canvas(self)
        canvas.create_polygon(points, fill=face_color, outline=edge_color)

    '''
    @param points: array of coordinates in the form of [x, y, z]
    to convert from x, y ,z vector to a 2d vector of only x, y
    '''
    def coordinator_3D(self, points):
        global height, width, distance, scale
        (x, y, z) = (points[0], points[1], points[2])
        y = int(height / 2 + ((y * distance) / (z + distance)) * scale)
        x = int(width / 2 + ((x * distance) / (z + distance)) * scale)
        return x, y

    '''
    @param geo: the size in the form of "WIDTHxHEIGHT"
    to set the geometry size of the window
    '''
    def geometry(self, geo):
        self.master.geometry(geo)

    '''
    @param angle: the angle to rotate with
    to rotate around Y
    '''
    def rotate_y(self, angle=0.5):
        global mem_points
        angle = angle / 450 * 180 / math.pi
        for i, point in enumerate(mem_points):
            x = point[0] * math.cos(angle) - point[2] * math.sin(angle)
            y = point[1]
            z = point[2] * math.cos(angle) + point[0] * math.sin(angle)
            mem_points[i] = (x, y, z)

    '''
    @param angle: the angle to rotate with
    to rotate around X
    '''
    def rotate_x(self, angle=0.5):
        global mem_points
        angle = angle / 450 * 180 / math.pi
        for i, point in enumerate(mem_points):
            x = point[0]
            y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
            z = point[2] * math.cos(angle) + point[1] * math.sin(angle)
            mem_points[i] = (x, y, z)

    '''
    @param angle: the angle to rotate with
    to rotate around Z
    '''
    def rotate_z(self, angle=0.5):
        global mem_points
        angle = angle / 450 * 180 / math.pi
        for i, point in enumerate(mem_points):
            x = point[0] * math.cos(angle) + point[1] * math.sin(angle)
            y = point[1] * math.cos(angle) - point[0] * math.sin(angle)
            z = point[2]
            mem_points[i] = (x, y, z)

    '''
    @param amount: the amount to scale with
    to scale the rendered object
    '''
    def scale(self, amount):
        global scale
        scale = scale + amount

    '''
    @param direction: can be x, y or z
    to move the rendered object towards the direction
    '''
    def move(self, direction,  amount):
        global mem_points
        i = 0
        while i < len(mem_points):
            point = mem_points[i]
            x = point[0]
            y = point[1]
            z = point[2]
            if direction == "x":
                x = x + amount
            if direction == "y":
                y = y + amount
            if direction == "z":
                z = z + amount
            mem_points[i] = [x, y, z]
            i = i + 1

    '''
    the render function called for one frame
    '''
    def render(self):
        global canvas
        canvas.delete("all")
        self.sort_vertices()
        self.vertices_reset()
        self.master.update()
