# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pyglet
from pyglet.gl import *

import imgui
from imgui.integrations.pyglet import PygletRenderer


class Application:

    def __init__(self):
        self.window = pyglet.window.Window(800, 600)
        imgui.create_context()
        self.renderer = PygletRenderer(self.window)
        self.impl = PygletRenderer(self.window)

    def clear(self):
        glClearColor(1, 1, 1, 1)

    def dispatch(self):
        self.clear()

        @self.window.event
        def on_draw():
            self.window.clear()
            glClear(GL_COLOR_BUFFER_BIT)
            self.update(1 / 60.0)
            imgui.render()
            self.impl.render(imgui.get_draw_data())

        pyglet.app.run()

    def crosshair(self):
        y = 300
        for x in range(390, 410):
            pyglet.graphics.draw(
                1, pyglet.gl.GL_POINTS,
                ('v2i', (x, y)),
                ('c3B', (255, 0, 0))
            )

        x = 400
        for y in range(290, 310):
            pyglet.graphics.draw(
                1, pyglet.gl.GL_POINTS,
                ('v2i', (x, y)),
                ('c3B', (255, 0, 0))
            )

    showDrawTools = True
    showLayers = True
    showTestWindow = False

    def update(self, dt):
        imgui.new_frame()

        self.crosshair()

        if self.showTestWindow:
            self.testWindow()

        if self.showDrawTools:  # show Drawing Tools window
            self.drawTools()

        if self.showLayers:
            self.layers()

        if imgui.begin_main_menu_bar():  # stat menu bar (top bar)

            if imgui.begin_menu("File", True):  # start menu bar entry: File
                clicked_quit, selected_quit = imgui.menu_item(  # start File menu entry: Quit
                    "Quit", 'Cmd+Q', False, True  # Name label, Shortcut label, Check bool, Enabled bool
                )
                if clicked_quit:  # event: if entry quit is clicked
                    exit(1)
                if selected_quit:
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

            # Example of a window, check line 59
            if imgui.begin_menu("Test", True):  # start menu bar entry: Test
                clicked_test, selected_test = imgui.menu_item(
                    "Test", "Ctrl+Alt+Del", self.showTestWindow, True
                )
                if clicked_test:
                    if self.showTestWindow:
                        self.showTestWindow = False
                    else:
                        self.showTestWindow = True
                imgui.end_menu()  # end Test menu

            imgui.end_main_menu_bar()

        # imgui.show_test_window()  # Built in test thing

    def shutdown(self):
        self.impl.shutdown()

    def testWindow(self):
        imgui.begin("Custom window", False)  # start new window: Custom Window
        imgui.text("Bar")  # text label
        imgui.text_colored("Eggs", 0.2, 1., 0.)  # colored text label (text, r, g , b)
        imgui.button("Test Button", 100, 20)
        imgui.end()  # End window def: Custom Window

    # consider moving these to global scope
    color = .0, .0, .0  # used for drawing color, set data type for pyglet.graphics.draw to c3f
    drawMode = ""  # used to specify what to draw
    vrad = 0  # store vertical radius for ellipse, radius for circle
    hrad = 0  # stores horizontal radius for ellipse, unused for circle
    x_center = 400  # see x_center in cga_lib.py
    y_center = 300  # see y_center in cga_lib.py

    def drawTools(self):
        imgui.begin("Drawing Tools")
        if imgui.button("Reset", 207, 20):
            self.color = .0, .0, .0
            self.drawMode = ""
            self.vrad = 0
            self.hrad = 0
            self.x_center = 400
            self.y_center = 300
        if imgui.button("Circle", 100, 20):  # imgui.core.button, https://github.com/ocornut/imgui/issues/2481
            self.drawMode = "c"
        imgui.same_line(115)
        if imgui.button("Ellipse", 100, 20):
            self.drawMode = "e"
        imgui.new_line()
        if self.drawMode == "c":
            changed, self.vrad = imgui.input_int("Radius", self.vrad, 1, 100)  # imgui.core.input_int
            changed, self.x_center = imgui.slider_int("X-axis center", self.x_center, 0, 800)  # imgui.core.slider_int, set max to window size
            changed, self.y_center = imgui.slider_int("Y-axis center", self.y_center, 0, 600)
            changed, self.color = imgui.color_edit3("Set Color", *self.color)  # asterisk used for tuple, I think...
        elif self.drawMode == "e":
            changed, self.vrad = imgui.input_int("Vertical Radius", self.vrad, 1, 100)  # imgui.core.input_int
            # changed, self.vrad = imgui.slider_int("", self.vrad, 0, 1000)
            changed, self.hrad = imgui.input_int("Horizontal Radius", self.hrad, 1, 100)
            # changed, self.hrad = imgui.slider_int("Horizontal Radius", self.hrad, 0, 1000)
            changed, self.x_center = imgui.slider_int("X-axis center", self.x_center, 0, 800)  # imgui.core.slider_int, set max to window size
            changed, self.y_center = imgui.slider_int("Y-axis center", self.y_center, 0, 600)
            changed, self.color = imgui.color_edit3("Set Color", *self.color)  # asterisk used for tuple, I think...

        imgui.new_line
        imgui.begin_child("Current Settings", border=True)  # imgui.core.begin_child
        imgui.text("Currently Drawing: ")  # imgui.core.text
        if self.drawMode == "c":
            imgui.same_line(200), imgui.text_colored("Circle", 0, 1, 0)  # imgui.core.same_line, imgui.core.text_colored
            imgui.text("Radius:"), imgui.same_line(200), imgui.text_colored(str(self.vrad), 0, 1, 0)
            imgui.text("X Position:"), imgui.same_line(200), imgui.text_colored(str(self.x_center), 0, 1, 0)
            imgui.text("Y Position:"), imgui.same_line(200), imgui.text_colored(str(self.y_center), 0, 1, 0)
        elif self.drawMode == "e":
            imgui.same_line(200), imgui.text_colored("Ellipse", 0, 1, 0)
            imgui.text("V. Radius:"), imgui.same_line(200), imgui.text_colored(str(self.vrad), 0, 1, 0)
            imgui.text("H. Radius:"), imgui.same_line(200), imgui.text_colored(str(self.hrad), 0, 1, 0)
            imgui.text("X Position:"), imgui.same_line(200), imgui.text_colored(str(self.x_center), 0, 1, 0)
            imgui.text("Y Position:"), imgui.same_line(200), imgui.text_colored(str(self.y_center), 0, 1, 0)
        else:
            imgui.text("Nothing Selected")
        imgui.end_child()
        imgui.end()

    def layers(self):
        imgui.begin("Layers")
        # display layers here...
        imgui.end()

def main():
    app = Application()
    app.dispatch()
    app.shutdown()


if __name__ == "__main__":
    main()
