from Simple3DEngine.Engine import Engine


def main():
    root = Engine()

    object_1 = root.add_object('coords/monkey.ply', 'a monkey!')
    object_1.face_color = "green"
    object_1.edge_color = "black"
    object_1.rotate_x(12)
    camera = root.get_camera()
    while True:
        camera.rotate_y(1)
        root.render()


if __name__ == '__main__':
    main()