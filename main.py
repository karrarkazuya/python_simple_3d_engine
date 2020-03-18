from Engine import *


def main():
    root = Engine()

    root.import_ply('monkey.ply')

    root.rotate_x(12)

    while True:
        root.rotate_y(0.4)
        root.render()


if __name__ == '__main__':
    main()