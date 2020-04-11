# python simple 3D engine
A simple python tinker 3D engine that renders ply files


#### Fast how to

A simple and fast way to get started is by loading your object and render it as follows
First we import the engine

    from Simple3DEngine.Engine import Engine
Then create a new object call it root for example

    root = Engine()
Load up your ply file and give it a name

    object_1 = root.add_object('monkey.ply', 'a monkey!')
You can easily change the colors of the surface of the edges of an object, you can also use hexa colors

    object_1.face_color = "green"
    object_1.edge_color = "black"
Render it 

    while True:
        root.render()
You can control each object by functions for Rotation, Scaling or moving
You can also control the entire camera this way but first you need to create a new camera object

    camera = root.get_camera()
Then you can easily use the control functions for example

    camera.rotate_y(1)


#### Screenshots
![](https://github.com/karrarkazuya/python_simple_3d_engine/blob/master/screenshot.png)
and here an example of using the camera to rotate on two objects and moving one object and ghosting at the same time
![](https://github.com/karrarkazuya/python_simple_3d_engine/blob/master/screenshot.gif)
