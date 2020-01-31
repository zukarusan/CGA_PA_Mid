# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pyglet
from pyglet import gl

import imgui
from imgui.integrations.pyglet import PygletRenderer


class Application:

    def __init__(self):
        self.window = pyglet.window.Window(800, 600)
        imgui.create_context()
        self.renderer = PygletRenderer(self.window)
        self.impl = PygletRenderer(self.window)

    def clear(self):
        gl.glClearColor(1, 1, 1, 1)

    def dispatch(self):
        self.clear()

        @self.window.event
        def on_draw():
            self.window.clear()
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
    showTestWindow = False

    def update(self, dt):
        imgui.new_frame()

        self.crosshair()

        if self.showTestWindow:
            self.testWindow()

        if self.showDrawTools:  # show Drawing Tools window
            self.drawTools()

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

    color = .0, .0, .0  # used for drawing color

    def drawTools(self):
        imgui.begin("Drawing Tools")
        imgui.button("Circle", 100, 20)
        imgui.button("Ellipse", 100, 20)
        changed, self.color = imgui.color_edit3("Set Color", *self.color)

        imgui.end()


def main():
    app = Application()
    app.dispatch()
    app.shutdown()


if __name__ == "__main__":
    main()
