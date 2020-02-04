import pyglet
from OpenGL.GL import *
class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

class Canvas:
    def __init__(self, width, height, x=0, y=0, format="RGB"):
        self.width = width
        self.height = height
        self.x_offset = x
        self.y_offset = y
        self.layers = []

    def add_object(self, drawable_object):
        drawable_object.set_layer_id(len(self.layers))
        self.layers.append(drawable_object)

    def draw_layers(self):
        for layer in self.layers:
            pyglet.graphics.draw (
                len(layer.points) // 2,
                pyglet.gl.GL_POINTS,
                ('v2i', layer.points)
            )

    def delete_object(self, id):
        try:
            self.layers.remove(self.layers[id])
        except:
            print("Object with id ", id, " doesn't exist")

class DrawableObject:
    def __init__(self):
        self.id = None
        self.points = []

    def create_points(self):
        pass

    def set_layer_id(self, id):
        self.id = id

    def color(self, color):
        # buatin
        pass

class Circle(DrawableObject):
    def __init__(self, x_center, y_center, radius):
        super().__init__()
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center
        self.create_points()

    def create_points(self):
        # Drawing circle using Second-Order Midpoint Algorithm
        x = 0
        y = self.radius
        d = 1 - self.radius
        d_cont = 3
        d_shift = (-2 * self.radius) + 5
        while x < y:
            # quadrant 1
            # (x, y)
            self.points += [self.x_center + x, self.y_center + y]
            # (y, x)
            self.points += [self.x_center + y, self.y_center + x]

            # quadrant 2
            # (-x, y)
            self.points += [self.x_center - x, self.y_center + y]
            # (-y, x)
            self.points += [self.x_center - y, self.y_center + x]

            # quadrant 3
            # (-x, -y)
            self.points += [self.x_center - x, self.y_center - y]
            # (-y, -x)
            self.points += [self.x_center - y, self.y_center - x]

            # quadrant 4
            # (x, -y)
            self.points += [self.x_center + x, self.y_center - y]
            # (y, -x)
            self.points += [self.x_center + y, self.y_center - x]

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


class Ellipse(DrawableObject):
    def __init__(self, x_center, y_center, v_radius, h_radius):
        super().__init__()
        self.v_radius = v_radius
        self.h_radius = h_radius
        self.x_center = x_center
        self.y_center = y_center
        self.create_points()

    def create_points(self):
        x = 0
        y = self.h_radius

        # Store squared value
        v_sqr = self.v_radius * self.v_radius
        h_sqr = self.h_radius * self.h_radius

        # All the d's in region 1
        d = 4 * h_sqr - 4 * v_sqr * self.h_radius + v_sqr
        dr = h_sqr * 3
        ddr = dr + 2 * v_sqr * (1 - self.h_radius)

        self.points += [self.x_center + x, self.y_center + y]
        self.points += [self.x_center - x, self.y_center + y]
        self.points += [self.x_center - x, self.y_center - y]
        self.points += [self.x_center + x, self.y_center - y]

        # Region 1
        while 2 * h_sqr * (x + 1) < v_sqr * (2 * y - 1):
            if d > 0:
                y = y - 1
                d = d + 4 * ddr
                dr = dr + 2 * h_sqr
                ddr = ddr + 2 * (v_sqr + h_sqr)
            else:
                d = d + 4 * dr
                dr = dr + 2 * h_sqr
                ddr = ddr + 2 * h_sqr
            x = x + 1
            self.points += [self.x_center + x, self.y_center + y]
            self.points += [self.x_center - x, self.y_center + y]
            self.points += [self.x_center - x, self.y_center - y]
            self.points += [self.x_center + x, self.y_center - y]

        # All the d's in region 1
        dd = v_sqr * (3 - 2 * y)
        ddr = dd + 2 * h_sqr * (x + 1)
        d = h_sqr * (2 * x + 1) * (2 * x + 1) + 4 * v_sqr * (y - 1) * (y - 1) - 4 * v_sqr * h_sqr

        # Region 2
        while y > 0:
            if d < 0:
                x = x + 1
                d = d + 4 * ddr
                ddr = ddr + 2 * (v_sqr + h_sqr)
                dd = dd + 2 * v_sqr
            else:
                d = d + 4 * dd
                ddr = ddr + 2 * v_sqr
                dd = dd + 2 * v_sqr
            y = y - 1
            self.points += [self.x_center + x, self.y_center + y]
            self.points += [self.x_center - x, self.y_center + y]
            self.points += [self.x_center - x, self.y_center - y]
            self.points += [self.x_center + x, self.y_center - y]
        # buatin