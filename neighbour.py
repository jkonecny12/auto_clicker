#!/usr/bin/python3

import time

from autoclicker import MouseLocator, MouseController, Point


if __name__ == "__main__":
    locator = MouseLocator()

    time.sleep(5)
    locator.get_mouse_location()
    controller = MouseController()

    p_next = locator.coordinates
    p_first = Point(p_next.x + 62, p_next.y + 52)
    p_space = Point(103, 0)

    print(p_next)

    for i in range(0, 5):
        for y in range(0, 5):
            p_help = Point(p_first.x + (p_space.x * y), p_first.y + (p_space.y * y))
            print(p_help)
            controller.set_position(p_help)
            time.sleep(0.5)
            controller.left_click()
            time.sleep(0.2)
        controller.set_position(p_next)
        time.sleep(0.5)
        controller.left_click()
        time.sleep(0.2)
