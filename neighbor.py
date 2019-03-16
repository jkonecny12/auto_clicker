#!/usr/bin/python3

import time

from autoclicker import MouseLocator, MouseController, Point
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="Automatic mouse controller to visit all neighbors in one"
                            "game")

    parser.add_argument("action", action="store", type=str, choices=["support", "pub"],
                        help="""Run script for giving supports or visiting pubs.""")

    return parser.parse_args()


def ask_user_and_wait(question):
    print(question)
    input("Press any key and wait 3 secs")
    print("=============================")
    time.sleep(3)


def get_position(locator, question):
    ask_user_and_wait(question)
    locator.get_mouse_location()
    return locator.coordinates


def click_all_support(locator, controller):
    p_next = get_position(locator, "Move cursor to the next 5 people on the left button")
    p_first = get_position(locator, "Move cursor to the first portrait SUPPORT button")
    p_second = get_position(locator, "Move cursor to the second portrait SUPPORT button")
    p_space = Point(p_second.x - p_first.x, 0)

    for i in range(0, 30):
        for y in range(0, 5):
            p = Point(p_first.x + (p_space.x * y), p_first.y + (p_space.y * y))
            controller.set_position(p)
            controller.left_click()
        controller.set_position(p_next)
        controller.left_click()


if __name__ == "__main__":
    ns = parse_args()
    locator = MouseLocator()

    controller = MouseController()
    controller.delay_before = 0.5
    controller.delay_after = 0.4

    if ns.action == "support":
        click_all_support(locator, controller)
