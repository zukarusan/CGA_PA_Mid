from __future__ import absolute_import

import pyglet
from pyglet import gl
from pyglet.gl import *
from pyglet.window import key  # for key input, on_key_press

import pickle
import imgui
from imgui.integrations.pyglet import PygletRenderer

from cga_lib import *


class Application:
    # ----Initializations----
    window = pyglet.window.Window(800, 600)  # window initialization
    # window.set_mouse_visible(False)  # Hides OS pointer when in window
    canvas = Canvas()  # canvas initialization, area that vectors are drawn
    imgui.create_context()
    renderer = PygletRenderer(window)
    impl = PygletRenderer(window)
    # ----Initializations----

    def __init__(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0)  # calls self.update every 1/60 seconds

        @self.window.event
        def on_draw():
            self.window.clear()
            glClear(GL_COLOR_BUFFER_BIT)
            self.update(1 / 60.0)
            imgui.render()
            self.impl.render(imgui.get_draw_data())

        # ----Input Handling----  Note: Boolean values are defined below (Drawing/Rendering Variables)
        # --Keyboard--
        @self.window.event
        def on_key_press(symbol, modifiers):
            if modifiers & key.MOD_SHIFT:  # Example of how to use modifiers
                if symbol == key.X:
                    print("test")
            elif symbol == key.L:
                if self.showLayers:
                    self.showLayers = False
                else:
                    self.showLayers = True
            elif symbol == key.D:
                if self.showDrawTools:
                    self.showDrawTools = False
                else:
                    self.showDrawTools = True

        # --Mouse Movement--  Note: Cursor position variables declared below (Drawing/Rendering Variables)
        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            print(x, y)
            self.crosshair(x, y)
            self.cursor_pos_y = y
            self.cursor_pos_x = x

        # --Mouse Click--
        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            pass

        # --Mouse Drag--
        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            pass
        # ----Input Handling----

    def clear(self):
        gl.glClearColor(1, 1, 1, 1)

    def dispatch(self):
        self.clear()
        pyglet.app.run()

    def shutdown(self):
        self.impl.shutdown()

    def crosshair(self, x, y):  # draws a green crosshair on pointer location
        for xc in range(x - 5, x + 5):
            draw(
                1, GL_POINTS,
                ('v2i', (xc, y)),
                ('c3f', (0.0, 1.0, 0.0))
            )
        for yc in range(y - 5, y + 5):
            draw(
                1, GL_POINTS,
                ('v2i', (x, yc)),
                ('c3f', (0.0, 1.0, 0.0))
            )

    # ----Window and Toolbar Booleans----
    showDrawTools = False
    showLayers = False
    showTests = False
    # ----Window and Toolbar Booleans----

    def update(self, dt):
        self.canvas.draw_layers()
        imgui.new_frame()

        # ----Call Windows----
        if self.showTests:  # show Tests
            self.tests()

        if self.showDrawTools:  # show Drawing Tools window
            self.drawTools()

        if self.showLayers:  # show Layers Window
            self.layers()
        # ----Call Windows----

        # ----Imgui Menu Bar Rendering----
        if imgui.begin_main_menu_bar():  # stat menu bar (top bar)

            if imgui.begin_menu("File", True):  # start menu bar entry: File
                clicked_quit, selected_quit = imgui.menu_item(  # start File menu entry: Quit
                    "Quit", 'Cmd+Q', False, True  # Name label, Shortcut label, Check bool, Enabled bool
                )
                if clicked_quit:  # event: if entry quit is clicked
                    exit(1)
                if selected_quit:
                    pass
                clicked_save, selected_save = imgui.menu_item(
                    "Save", 'Cmd+S', False, True
                )
                if clicked_save:
                    self.save('./', 'save')
                if selected_save:
                    pass
                imgui.end_menu()  # end File menu

            if imgui.begin_menu("Draw", True):
                clicked_draw, selected_draw = imgui.menu_item(
                    "Draw Tools", "", self.showDrawTools, True
                )
                if clicked_draw:
                    if self.showDrawTools:
                        self.showDrawTools = False
                    else:
                        self.showDrawTools = True

                clicked_layers, selected_layers = imgui.menu_item(
                    "Layers", "", self.showLayers, True
                )
                if clicked_layers:
                    if self.showLayers:
                        self.showLayers = False
                    else:
                        self.showLayers = True
                imgui.end_menu()

            if imgui.begin_menu("Test", True):  # start menu bar entry: Test
                clicked_test, selected_test = imgui.menu_item(
                    "Test", "Ctrl+Alt+Del", self.showTests, True
                )
                if clicked_test:
                    if self.showTests:
                        self.showTests = False
                    else:
                        self.showTests = True
                imgui.end_menu()  # end Test menu

            imgui.end_main_menu_bar()

        imgui.end_frame()
        # ----Imgui Menu Bar Rendering----

    # ----Drawing/Rendering Variables----
    cursor_pos_x = 0
    cursor_pos_y = 0
    draw_mode = ""  # used to specify what to draw
    color = [0., 0., 0.]  # color values in float, rgb
    vrad = 0  # store vertical radius for ellipse, radius for circle
    hrad = 0  # stores horizontal radius for ellipse, unused for circle
    x_center = 400  # see x_center in cga_lib.py
    y_center = 300  # see y_center in cga_lib.py
    # ----Drawing/Rendering Variables----

    # ----Only used for tests----
    checkbox = False
    testCircle = Circle(400, 300, 100, color=Color(1.0, 0.0, 0.0))
    testEllipse = Ellipse(400, 300, 120, 60, color=Color(0.0, 0.0, 1.0))
    # ----Only used for tests----

    def tests(self):
        imgui.begin("Test Window")
        imgui.text("Lorem ipsum")
        changed, checkbox = imgui.checkbox("Checkbox", self.checkbox)  # imgui.core.checkbox
        if imgui.button("Test Circle", 100, 20):
            self.canvas.add_object(self.testCircle)
        if imgui.button("Test Ellipse", 100, 20):
            self.canvas.add_object(self.testEllipse)
        imgui.end()

    def drawTools(self):
        imgui.begin("Drawing Tools")
        if imgui.button("Circle", 100, 20):  # imgui.core.button, https://github.com/ocornut/imgui/issues/2481
            self.draw_mode = 'c'
        imgui.same_line(115)
        if imgui.button("Ellipse", 100, 20):
            self.draw_mode = 'e'
        if self.draw_mode == 'c':
            changed, self.vrad = imgui.input_int("Radius", self.vrad, 1, 100)  # imgui.core.input_int
            changed, self.x_center = imgui.input_int("X-axis center", self.x_center, 1, 800)  # imgui.core.slider_int, set max to window size
            changed, self.y_center = imgui.input_int("Y-axis center", self.y_center, 1, 600)
            changed, self.color = imgui.color_edit3("Set Color", *self.color)  # asterisk used for tuple, I think...
        elif self.draw_mode == 'e':
            changed, self.vrad = imgui.input_int("Vertical Radius", self.vrad, 1, 100)  # imgui.core.input_int
            # changed, self.vrad = imgui.slider_int("", self.vrad, 0, 1000)
            changed, self.hrad = imgui.input_int("Horizontal Radius", self.hrad, 1, 100)
            # changed, self.hrad = imgui.slider_int("Horizontal Radius", self.hrad, 0, 1000)
            changed, self.x_center = imgui.input_int("X-axis center", self.x_center, 1, 800)  # imgui.core.slider_int, set max to window size
            changed, self.y_center = imgui.input_int("Y-axis center", self.y_center, 1, 600)
            changed, self.color = imgui.color_edit3("Set Color", *self.color)  # asterisk used for tuple, I think...
        imgui.new_line()
        imgui.begin_child("Current Settings", border=True)  # imgui.core.begin_child
        imgui.text("Currently Drawing: ")  # imgui.core.text
        if self.draw_mode == "c":
            imgui.same_line(200), imgui.text_colored("Circle", 0, 1, 0)  # imgui.core.same_line, imgui.core.text_colored
            imgui.text("Radius:"), imgui.same_line(200), imgui.text_colored(str(self.vrad), 0, 1, 0)
            imgui.text("X Position:"), imgui.same_line(200), imgui.text_colored(str(self.x_center), 0, 1, 0)
            imgui.text("Y Position:"), imgui.same_line(200), imgui.text_colored(str(self.y_center), 0, 1, 0)
        elif self.draw_mode == "e":
            imgui.same_line(200), imgui.text_colored("Ellipse", 0, 1, 0)
            imgui.text("V. Radius:"), imgui.same_line(200), imgui.text_colored(str(self.vrad), 0, 1, 0)
            imgui.text("H. Radius:"), imgui.same_line(200), imgui.text_colored(str(self.hrad), 0, 1, 0)
            imgui.text("X Position:"), imgui.same_line(200), imgui.text_colored(str(self.x_center), 0, 1, 0)
            imgui.text("Y Position:"), imgui.same_line(200), imgui.text_colored(str(self.y_center), 0, 1, 0)
        else:
            imgui.text("Nothing Selected")
        imgui.end_child()
        if imgui.button("Reset", 100, 20):
            self.color = [.0, .0, .0]
            self.draw_mode = ""
            self.vrad = 0
            self.hrad = 0
            self.x_center = 400
            self.y_center = 300
        imgui.same_line(115)
        if imgui.button("Enter", 100, 20):
            if self.draw_mode == "":
                pass
            elif self.draw_mode == "c":
                drawCircle = Circle(self.x_center, self.y_center, self.vrad, color=Color(self.color[0], self.color[1], self.color[2]))
                self.canvas.add_object(drawCircle)
            elif self.draw_mode == "e":
                drawEllipse = Ellipse(self.x_center, self.y_center, self.vrad, self.hrad, color=Color(self.color[0], self.color[1], self.color[2]))
                self.canvas.add_object(drawEllipse)
        imgui.end()

    delete_index = 1

    def layers(self):
        imgui.begin("Layers")
        if imgui.button("Delete All"):
            clear_index = self.canvas.get_length() - 1
            try:
                while clear_index >= 0:
                    self.canvas.delete_object(clear_index)
                    clear_index = clear_index - 1
            except clear_index == -1:
                print("No objects found!")
        if imgui.button("Refresh Screen", 176, 20):
            self.window.clear()
            self.canvas.draw_layers()
        changed, self.delete_index = imgui.input_int("Layer to delete", self.delete_index, 1, 100)
        if imgui.button("Delete", 100, 20):
            self.canvas.delete_object(self.delete_index-1)
        index = 0
        for layer in self.canvas.layers:
            layer_str = "Layer: {}, type: {}"
            imgui.text(layer_str.format(index + 1, layer.type))
            index = index + 1
        imgui.end()

    def save(self, path, file_name):
        try:
            with open(path + file_name + '.can', 'wb') as output:
                pickle.dump(self.canvas, output, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            pass

    def load(self, path, file_name):
        try:
            with open(path + file_name + '.can', 'rb') as input:
                self.canvas = pickle.load(input)
        except FileNotFoundError:
            pass  # Please make a file nor found error dialog

def main():
    app = Application()
    app.dispatch()
    app.shutdown()


if __name__ == "__main__":
    main()
