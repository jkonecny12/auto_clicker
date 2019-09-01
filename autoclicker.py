#!/usr/bin/python3

import subprocess
import time

from pymouse import PyMouse


class XDoTool(object):
    """Do a low level calls and reading of xdotool."""

    def __init__(self):
        self._program_name = "xdotool"

    def run_tool(self, args):
        """Run xdotool with arguments check output and return stdout

        :param args: list of arguments for the xdotool
        :type args: List[str]
        """
        cmd = [self._program_name]
        cmd.extend(args)
        out = subprocess.run(cmd, capture_output=True)
        out.check_returncode()
        return out.stdout.decode()


class Point(object):
    """Store coordinates."""

    def __init__(self, x, y):
        """Create the instance with x & y.

        :param x: X coordinate
        :type x: int
        :param y: Y coordinate
        :type y: int
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "Point({},{})".format(self.x, self.y)

    @property
    def str_x(self):
        """Return X coordinate as string"""
        return str(self.x)

    @property
    def str_y(self):
        """Return Y coordinate as string"""
        return str(self.y)


class MouseLocator(object):
    """Class to get location of the class."""

    def __init__(self):
        self._coordinates = Point(0, 0)
        self._mouse_controller = PyMouse()

    @property
    def coordinates(self):
        """Get coordinates.

        :return: Point class instance
        """
        return self._coordinates

    @property
    def x(self):
        """Get X coordinate.

        :return: X
        :rtype: int
        """
        return self._coordinates[0]

    @property
    def y(self):
        """Get Y coordinate.

        :return: Y
        :rtype: int
        """
        return self._coordinates[1]

    def get_mouse_location(self):
        """Get and store mouse location."""
        x, y = self._mouse_controller.position()

        self._coordinates = Point(x, y)


class MouseController(object):
    """Control mouse."""

    def __init__(self):
        self._runner = XDoTool()
        self._delay_before = 0
        self._delay_after = 0

    @property
    def delay_before(self):
        """Get delay before mouse click.

        :return: delay in seconds
        """
        return self._delay_before

    @delay_before.setter
    def delay_before(self, value):
        """Set delay before mouse click.

        :return: delay in seconds
        """
        self._delay_before = value

    @property
    def delay_after(self):
        """Get delay after mouse click.

        :return: delay in seconds
        """
        return self._delay_after

    @delay_after.setter
    def delay_after(self, value):
        """Set delay after mouse click.

        :return: delay in seconds
        """
        self._delay_after = value

    def set_position(self, position):
        """Set mouse position to given position.

        :param position: position where the mouse will be moved
        :type position: instance of the Point class
        """
        self._runner.run_tool(["mousemove", "--sync",
                               position.str_x, position.str_y])

    def left_click(self):
        """Click left mouse button on the actual position."""
        if self._delay_before != 0:
            time.sleep(self._delay_before)

        self._runner.run_tool(["click", "1"])

        if self._delay_after != 0:
            time.sleep(self._delay_after)


if __name__ == "__main__":
    mouse = MouseLocator()
    mouse.get_mouse_location()
    print(mouse.coordinates)
