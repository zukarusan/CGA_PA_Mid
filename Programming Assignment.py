import pyglet
from pyglet.gl import *
from pyglet.window import key  # for key input, on_key_press
from cga_lib import Circle, Ellipse #include file cga_lib
from pyglet.window import mouse  # for mouse input, on_mouse_press

window = pyglet.window.Window(800, 600)  # create a window object with the resolution of 800x600
window.set_caption('Programming Assignment')
glClear(GL_COLOR_BUFFER_BIT)  # clear window using PyOpenGL, alternatively use window.clear()
vectors = []  # list to store vectors


def setPixel(x, y):  # Used to draw pixels, do not directly use
    pyglet.graphics.draw(
        1, pyglet.gl.GL_POINTS,
        ('v2i', (x, y))
    )

def render(objects):  # reads from specified list argument to render objects
    for obj in objects:
        if obj[0] == "c":  # object stored is a circle
            radius = obj[1]  # set parameters
            xoffset = obj[2]
            yoffset = obj[3]
            c1 = Circle(xoffset, yoffset, radius)
            c1.draw(setPixel)
        elif obj[0] == "e":  # object stored is an ellipse
            a = obj[1]  # set parameters
            b = obj[2]
            xoffset = obj[3]
            yoffset = obj[4]
            e1 = Ellipse(xoffset, yoffset, a, b)
            e1.draw(setPixel)


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

'''
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        pass
'''


pyglet.app.run()
