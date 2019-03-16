#!/usr/bin/python3

import time

from autoclicker import MouseLocator, MouseController, Point


def ask_user_and_wait(question):
    print(question)
    input("Press any key and wait 3 secs")
    print("=============================")
    time.sleep(3)


def get_position(locator, question):
    ask_user_and_wait(question)
    locator.get_mouse_location()
    return locator.coordinates


if __name__ == "__main__":
    locator = MouseLocator()

    controller = MouseController()
    controller.delay_before = 0.5
    controller.delay_after = 0.4

    p_next = get_position(locator, "Move cursor to the next 5 people on the left button")
    p_first = get_position(locator, "Move cursor to the first portrait HELP button")
    p_second = get_position(locator, "Move cursor to the second portrait HELP button")
    p_space = Point(p_second.x - p_first.x, 0)

    print(p_next)

    for i in range(0, 3):
        for y in range(0, 5):
            p_help = Point(p_first.x + (p_space.x * y), p_first.y + (p_space.y * y))
            print(p_help)
            controller.set_position(p_help)
            controller.left_click()
        controller.set_position(p_next)
        controller.left_click()
