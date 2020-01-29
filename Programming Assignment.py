import pyglet
from pyglet.gl import *
from pyglet.window import key  # for key input, on_key_press
from pyglet.window import mouse  # for mouse input, on_mouse_press

window = pyglet.window.Window(800, 600)  # create a window object with the resolution of 800x600
window.set_caption('Programming Assignment')
glClear(GL_COLOR_BUFFER_BIT)  # clear window using PyOpenGL, alternatively use window.clear()
vectors = []  # list to store vectors


def setPixel(x, y, xoffset, yoffset):  # Used to draw pixels, do not directly use
    pyglet.graphics.draw(
        1, pyglet.gl.GL_POINTS,
        ('v2i', (x + xoffset, y + yoffset))
    )


def midpointCircle(radius, xoffset, yoffset):
    x = 0
    y = radius
    d = 1 - radius
    while x < y:
        # quadrant 1
        # (x, y)
        setPixel(x, y, xoffset, yoffset)
        # (y, x)
        setPixel(y, x, xoffset, yoffset)

        # quadrant 2
        # (-x, y)
        setPixel(-x, y, xoffset, yoffset)
        # (-y, x)
        setPixel(-y, x, xoffset, yoffset)

        # quadrant 3
        # (-x, -y)
        setPixel(-x, -y, xoffset, yoffset)
        # (-y, -x)
        setPixel(-y, -x, xoffset, yoffset)

        # quadrant 4
        # (x, -y)
        setPixel(x, -y, xoffset, yoffset)
        # (y, -x)
        setPixel(y, -x, xoffset, yoffset)

        if d < 0:
            d = d + (2 * x) + 3
        else:
            d = d + (2 * (x - y)) + 5
            y = y - 1
        x = x + 1


def circle(radius, xoffset, yoffset):
    x = 0
    y = radius
    d = 1 - radius
    d_cont = 3
    d_shift = (-2 * radius) + 5
    while x <= y:
        # quadrant 1
        # (x, y)
        setPixel(x, y, xoffset, yoffset)
        # (y, x)
        setPixel(y, x, xoffset, yoffset)

        # quadrant 2
        # (-x, y)
        setPixel(-x, y, xoffset, yoffset)
        # (-y, x)
        setPixel(-y, x, xoffset, yoffset)

        # quadrant 3
        # (-x, -y)
        setPixel(-x, -y, xoffset, yoffset)
        # (-y, -x)
        setPixel(-y, -x, xoffset, yoffset)

        # quadrant 4
        # (x, -y)
        setPixel(x, -y, xoffset, yoffset)
        # (y, -x)
        setPixel(y, -x, xoffset, yoffset)

        if d < 0:
            d = d + d_cont
            d_cont = d_cont + 2
            d_shift = d_shift + 2
        else:
            d = d + d_shift
            d_cont = d_cont + 2
            d_shift = d_shift + 4
            y = y - 1
        x = x + 1


def midpointEllipse(a, b, xoffset, yoffset):
    x = 0
    y = b
    d = (4 * b * b) - (4 * a * a * b) + (a * a)
    setPixel(x, y, xoffset, yoffset)
    setPixel(-x, y, xoffset, yoffset)
    setPixel(-x, -y, xoffset, yoffset)
    setPixel(x, -y, xoffset, yoffset)
    # xTraverse = (2 * b * b * (x * 1))
    # yTraverse = (a * a * (2 * y - 1))
    # region 1
    while 2 * b * b * (x + 1) < a * a * (2 * y - 1):
        if d > 0:
            y = y - 1
            d = d + b * b * (8 * x + 12) + a * a * (8 - 8 * y)
        else:
            d = d + b * b * (8 * x + 12)
        x = x + 1
        # xTraverse = (2 * b * b * (x * 1))
        # yTraverse = (a * a * (2 * y - 1))
        setPixel(x, y, xoffset, yoffset)
        setPixel(-x, y, xoffset, yoffset)
        setPixel(-x, -y, xoffset, yoffset)
        setPixel(x, -y, xoffset, yoffset)
    # region 2
    # print("region 1 end at:", x, y)
    d = b * b * (2 * x + 1) * (2 * x + 1) + 4 * a * a * (y - 1) * (y - 1) - 4 * a * a * b * b
    while y > 0:
        if d < 0:
            x = x + 1
            d = d + b * b * (8 * x + 8) + a * a * (12 - 8 * y)
        else:
            d = d + a * a * (12 - 8 * y)
        y = y - 1
        setPixel(x, y, xoffset, yoffset)
        setPixel(-x, y, xoffset, yoffset)
        setPixel(-x, -y, xoffset, yoffset)
        setPixel(x, -y, xoffset, yoffset)


def ellipse(a, b, xoffset, yoffset):
    x = 0
    y = b

    # Store squared value
    a2p = a * a
    b2p = b * b

    # All the d's in region 1
    d = 4 * b2p - 4 * a2p * b + a2p
    dr = b2p * 3
    ddr = dr + 2 * a2p * (1 - b)

    setPixel(x, y, xoffset, yoffset)
    setPixel(-x, y, xoffset, yoffset)
    setPixel(-x, -y, xoffset, yoffset)
    setPixel(x, -y, xoffset, yoffset)

    # Region 1
    while 2 * b2p * (x + 1) < a2p * (2 * y - 1):
        if d > 0:
            y = y - 1
            d = d + 4 * ddr
            dr = dr + 2 * b2p
            ddr = ddr + 2 * (a2p + b2p)
        else:
            d = d + 4 * dr
            dr = dr + 2 * b2p
            ddr = ddr + 2 * b2p
        x = x + 1
        setPixel(x, y, xoffset, yoffset)
        setPixel(-x, y, xoffset, yoffset)
        setPixel(-x, -y, xoffset, yoffset)
        setPixel(x, -y, xoffset, yoffset)

    # All the d's in region 1
    dd = a2p * (3 - 2 * y)
    ddr = dd + 2 * b2p * (x + 1)
    d = b2p * (2 * x + 1) * (2 * x + 1) + 4 * a2p * (y - 1) * (y - 1) - 4 * a2p * b2p

    # Region 2
    while y > 0:
        if d < 0:
            x = x + 1
            d = d + 4 * ddr
            ddr = ddr + 2 * (a2p + b2p)
            dd = dd + 2 * a2p
        else:
            d = d + 4 * dd
            ddr = ddr + 2 * a2p
            dd = dd + 2 * a2p
        y = y - 1
        setPixel(x, y, xoffset, yoffset)
        setPixel(-x, y, xoffset, yoffset)
        setPixel(-x, -y, xoffset, yoffset)
        setPixel(x, -y, xoffset, yoffset)


def render(objects):  # reads from specified list argument to render objects
    for obj in objects:
        if obj[0] == "c":  # object stored is a circle
            radius = obj[1]  # set parameters
            xoffset = obj[2]
            yoffset = obj[3]
            circle(radius, xoffset, yoffset)
        elif obj[0] == "e":  # object stored is an ellipse
            a = obj[1]  # set parameters
            b = obj[2]
            xoffset = obj[3]
            yoffset = obj[4]
            ellipse(a, b, xoffset, yoffset)


@window.event  # target window
def on_key_press(symbol, modifiers):  # keyboard input handler

    if symbol == key.X:  # nuke clear screen
        print("Clearing Screen")
        window.clear()

    elif symbol == key.C:  # circle
        print("Adding Circle Object at (400, 300) with radius = 25")
        # circle(25, 400, 300)
        vectors.append(["c", 25, 400, 300])
        render(vectors)

    elif symbol == key.E:  # ellipse
        print("Adding Ellipse Object at (400, 300) with a = 100, b = 50")
        # ellipse(100, 50, 400, 300)
        vectors.append(["e", 100, 50, 400, 300])
        render(vectors)

    elif symbol == key.R:  # re-render
        window.clear()
        print("(Re)rendering objects")
        render(vectors)

    elif symbol == key.M:
        print("Drawing Circle and Ellipse with Midpoint Algorithm")
        midpointCircle(40, 400, 300)
        midpointEllipse(120, 60, 400, 300)


'''
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        pass
'''


pyglet.app.run()
