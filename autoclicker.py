#!/usr/bin/python3

import subprocess


class XDoTool(object):

    def __init__(self):
        self._program_name = "xdotool"

    def run_tool(self, args):
        cmd = [self._program_name]
        cmd.extend(args)
        out = subprocess.run(cmd, capture_output=True)
        out.check_returncode()
        return out.stdout.decode()


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point({},{})".format(self.x, self.y)

    @property
    def str_x(self):
        return str(self.x)

    @property
    def str_y(self):
        return str(self.y)


class MouseLocator(object):

    def __init__(self):
        self._runner = XDoTool()
        self._window = ""
        self._coordinates = Point(0, 0)

    @property
    def window(self):
        return self._window

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

    def get_mouse_location(self):
        out = self._runner.run_tool(['getmouselocation', '--shell'])
        x = 0
        y = 0

        for line in out.strip().split('\n'):
            (key, value) = line.split('=')

            if key == 'X':
                x = int(value)
            elif key == 'Y':
                y = int(value)
            elif key == "WINDOW":
                self._window = int(value)

        self._coordinates = Point(x, y)


class MouseController(object):

    def __init__(self, window=None):
        self._runner = XDoTool()

    def set_position(self, position):
        self._runner.run_tool(["mousemove", "--sync",
                               position.str_x, position.str_y])

    def left_click(self):
        self._runner.run_tool(["click", "1"])


if __name__ == "__main__":
    mouse = MouseLocator()
    mouse.get_mouse_location()
    print(mouse.coordinates, mouse.window)
