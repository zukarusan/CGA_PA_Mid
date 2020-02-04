from pyglet.graphics import draw  # Using draw function
from pyglet.gl import GL_POINTS  # Using point variable in OpenGL library


class Color:
    # Class for defining colors
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


class Canvas:
    """
        This canvas class behaves abstractly under running window. Similar to Photoshop, it is aimed to
        allocate layers and maintaining objects to be drawn.
    """

    def __init__(self):
        self.layers = []  # Create layers upon instantiation

    def add_object(self, drawable_object):
        drawable_object.set_layer_id(len(self.layers))  # Set id to track in later use
        self.layers.append(drawable_object)  # Adding the 2D shape object into the last of the layer list

    def draw_layers(self):
        for layer in self.layers:  # Draw for each 2D shape objects in layer list
            draw(
                layer.buffer_size,
                GL_POINTS,
                ('v2i', layer.points),
                ('c3f', layer.colors)
            )

    def delete_object(self, id):  # Delete for the specified ID of the layer list
        try:
            self.layers.remove(self.layers[id])
        except:
            if id == -1:
                print("layer is empty")
            else:
                print("Object with id ", id, " doesn't exist in the layer list")


class DrawableObject:
    """
    This class is a parent class for any derived class which is in the manner of 2D shape.
    It is aimed to create object to be drawn in the canvas manner.
    """

    def __init__(self, color=Color(1.0, 1.0, 1.0)):
        self.id = None  # ID for layer in canvas
        self.type = "object"  # Type of object (circle/ellipse)
        self.colors = []  # Color buffers created to be specified when drawing
        self.points = []  # Point buffers created to be drawn in canvas
        self.buffer_size = None  # Number of buffers
        self.create_buffer()  # Draw to buffer, specified by derived class
        self.set_color(color)  # Default color, black

    def create_buffer(self):  # Drawing function by creating the points and color buffers instead and later
        pass                  # to be drawn in canvas. Specified in each derived class.

    def set_layer_id(self, id):  # Function to set the id in canvas layers
        self.id = id

    def set_color(self, color):
        if not self.buffer_size == 0:
            for b in range(self.buffer_size):
                self.colors += [color.red]
                self.colors += [color.green]
                self.colors += [color.blue]
        else:
            print("Buffer is empty")


class Circle(DrawableObject):
    def __init__(self, x_center, y_center, radius, **kwargs):
        self.type = "circle"  # doesn't seem to be working
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center
        super().__init__(**kwargs)

    def create_buffer(self):
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

        self.buffer_size = len(self.points) // 2


class Ellipse(DrawableObject):
    def __init__(self, x_center, y_center, v_radius, h_radius, **kwargs):
        self.type = "ellipse"
        self.v_radius = v_radius
        self.h_radius = h_radius
        self.x_center = x_center
        self.y_center = y_center
        super().__init__(**kwargs)

    def create_buffer(self):
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

        self.buffer_size = len(self.points) // 2