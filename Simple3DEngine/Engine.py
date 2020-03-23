from tkinter import Canvas, Frame, BOTH, Menu
from Simple3DEngine.Object import Object
import math
from Simple3DEngine.Poly import Poly

canvas = ""
height = 800
width = 1000

objects = []

mem_vertices = []

class Engine(Frame):
    def __init__(self):
        super().__init__()
        self.init_engine()
        self.camera = self.get_camera()

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

        camera = self.get_camera()
        option = Menu(menu_bar)
        option.add_command(label='Rotate <<', command=lambda: camera.rotate_y(-0.5))
        option.add_command(label='Rotate >>', command=lambda: camera.rotate_y(0.5))
        option.add_command(label='Rotate ^^', command=lambda: camera.rotate_x(-0.5))
        option.add_command(label='Rotate down', command=lambda: camera.rotate_x(0.5))
        menu_bar.add_cascade(label="Rotation", menu=option)

        option = Menu(menu_bar)
        option.add_command(label='Move >>', command=lambda: camera.move('x', 0.2))
        option.add_command(label='Move <<', command=lambda: camera.move('x', -0.2))
        option.add_command(label='Move ^^', command=lambda: camera.move('y', -0.2))
        option.add_command(label='Move down', command=lambda: camera.move('y', 0.2))
        menu_bar.add_cascade(label="Moving", menu=option)

        option = Menu(menu_bar)
        option.add_command(label='Scale ++', command=lambda: camera.scale(10))
        option.add_command(label='Scale --', command=lambda: camera.scale(-10))
        menu_bar.add_cascade(label="Scaling", menu=option)


    """
    to create a new object and append it
    """
    def add_object(self, file, title=""):
        global objects
        object_3d = Object()
        object_3d.import_ply(file, title)
        objects.append(object_3d)
        return object_3d


    '''
    used to redraw all the vertices
    '''
    def vertices_reset(self):
        global objects, mem_vertices

        for poly_0 in mem_vertices:
            if poly_0.visible:
                triangle = []
                for poly_1 in poly_0.vertices:
                    poly_1 = self.coordinator_3D(poly_1, poly_0)
                    triangle.append(poly_1[0])
                    triangle.append(poly_1[1])
                self.create_poly(triangle, poly_0.face_color, poly_0.edge_color)

    '''
    to sort arrays in a way to make the ones closer to the camera are the last to be rendered
    '''
    def sort_vertices(self):
        global objects, mem_vertices
        mem_vertices = []
        for object_3d in objects:
            mem_points = object_3d.mem_points
            mem_polies = object_3d.mem_polies
            count = 0
            while count < len(mem_polies):
                vertices = [mem_points[mem_polies[count][0]], mem_points[mem_polies[count][1]], mem_points[mem_polies[count][2]]]
                poly = Poly(object_3d.face_color, object_3d.edge_color, vertices, object_3d)
                if object_3d.sort_method == "avg":
                    poly.closest_to_camera = poly.get_close_of_camera_by_avg()
                elif object_3d.sort_method == "closer":
                    poly.closest_to_camera = poly.get_close_of_camera()
                else:
                    poly.closest_to_camera = 0
                mem_vertices.append(poly)
                count = count + 1
        mem_vertices.sort(key=lambda x: x.closest_to_camera, reverse=True)


    '''
    @param points: array of coordinates in the form of [(x, y), (x, y) , (x, y)] representing a polly
    to create a single poly
    '''
    def create_poly(self, points, face_color, edge_color):
        global canvas
        if canvas == "":
            canvas = Canvas(self)
        canvas.create_polygon(points, fill=face_color, outline=edge_color)


    '''
    @param points: array of coordinates in the form of [x, y, z]
    to convert from x, y ,z vector to a 2d vector of only x, y
    '''
    def coordinator_3D(self, points, poly):
        global height, width
        (x, y, z) = (points[0], points[1], points[2])
        y = int(height / 2 + ((y * poly.distance) / (z + poly.distance)) * poly.scale)
        x = int(width / 2 + ((x * poly.distance) / (z + poly.distance)) * poly.scale)
        return x, y


    '''
    @param geo: the size in the form of "WIDTHxHEIGHT"
    to set the geometry size of the window
    '''
    def geometry(self, geo):
        self.master.geometry(geo)


    '''
    to get an object of the camera class
    '''
    def get_camera(self):
        return Camera()


    '''
    the render function called for one frame
    '''
    def render(self):
        global canvas
        canvas.delete("all")
        self.sort_vertices()
        self.vertices_reset()
        self.camera = self.get_camera()
        self.master.update()


class Camera:
    def __init__(self):
        super().__init__()

    '''
    @param angle: the angle to rotate with
    to rotate around Y
    '''

    def rotate_y(self, angle=0.5):
        global objects
        angle = angle / 450 * 180 / math.pi
        for object_3d in objects:
            for i, point in enumerate(object_3d.mem_points):
                x = point[0] * math.cos(angle) - point[2] * math.sin(angle)
                y = point[1]
                z = point[2] * math.cos(angle) + point[0] * math.sin(angle)
                object_3d.mem_points[i] = (x, y, z)

    '''
    @param angle: the angle to rotate with
    to rotate around X
    '''

    def rotate_x(self, angle=0.5):
        global objects
        angle = angle / 450 * 180 / math.pi
        for object_3d in objects:
            for i, point in enumerate(object_3d.mem_points):
                x = point[0]
                y = point[1] * math.cos(angle) - point[2] * math.sin(angle)
                z = point[2] * math.cos(angle) + point[1] * math.sin(angle)
                object_3d.mem_points[i] = (x, y, z)

    '''
    @param angle: the angle to rotate with
    to rotate around Z
    '''

    def rotate_z(self, angle=0.5):
        global objects
        angle = angle / 450 * 180 / math.pi
        for object_3d in objects:
            for i, point in enumerate(object_3d.mem_points):
                x = point[0] * math.cos(angle) + point[1] * math.sin(angle)
                y = point[1] * math.cos(angle) - point[0] * math.sin(angle)
                z = point[2]
                object_3d.mem_points[i] = (x, y, z)



    '''
    @param direction: can be x, y or z
    to move the rendered object towards the direction
    '''

    def move(self, direction, amount):
        global objects
        for object_3d in objects:
            i = 0
            while i < len(object_3d.mem_points):
                point = object_3d.mem_points[i]
                x = point[0]
                y = point[1]
                z = point[2]
                if direction == "x":
                    x = x + amount
                if direction == "y":
                    y = y + amount
                if direction == "z":
                    z = z + amount
                object_3d.mem_points[i] = [x, y, z]
                i = i + 1

    '''
    @param amount: the amount to scale with
    to scale the rendered object
    '''

    def scale(self, amount):
        global objects
        for object_3d in objects:
            object_3d.scale = object_3d.scale + amount
