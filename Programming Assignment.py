import pyglet
from pyglet.gl import *
from pyglet.window import key  # for key input, on_key_press
from cga_lib import Circle, Ellipse, Canvas #include file cga_lib
from pyglet.window import mouse  # for mouse input, on_mouse_press

window = pyglet.window.Window(800, 600)  # create a window object with the resolution of 800x600
canvas = Canvas(800, 600)
window.set_caption('Programming Assignment')
glClear(GL_COLOR_BUFFER_BIT)  # clear window using PyOpenGL, alternatively use window.clear()
c1 = Circle(400, 300, 25)
e1 = Ellipse(400, 300, 100, 50)

def render(object):  # reads from specified list argument to render objects
    if object == "c":
        canvas.add_object(c1)
    elif object == "e":
        canvas.add_object(e1)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    canvas.draw_layers()

@window.event  # target window
def on_key_press(symbol, modifiers):  # keyboard input handler
    if symbol == key.X:  # delete last object
        print("Delete Last object")
        window.clear()
        canvas.delete_object(len(canvas.layers)-1)

    elif symbol == key.C:  # circle
        print("Adding Circle Object at (400, 300) with radius = 25")
        # circle(25, 400, 300)
        render("c")

    elif symbol == key.E:  # ellipse
        print("Adding Ellipse Object at (400, 300) with a = 100, b = 50")
        # ellipse(100, 50, 400, 300)
        render("e")

'''
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        pass
'''


pyglet.app.run()
