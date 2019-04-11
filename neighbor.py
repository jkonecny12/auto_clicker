#!/usr/bin/python3

import time

from enum import Enum

from autoclicker import MouseLocator, MouseController, Point
from argparse import ArgumentParser


class PointNames(Enum):
    NEXT_BUTTON = "Next"

    FIRST_SUPPORT_BUTTON = "First support"
    SECOND_SUPPORT_BUTTON = "Second support"

    FIRST_PUB_BUTTON = "First pub"
    SECOND_PUB_BUTTON = "Second pub"


class PointManager(object):
    """Store and load points used for further runs."""

    def __init__(self, locator):
        self._points = {}
        self._locator = locator

    def add_point(self, name, position):
        self._points[name] = position

    def ask_for_point(self, point):
        pos = self._get_position("Move cursor to the {} button".format(point.value))
        self.add_point(point, pos)

    def _get_position(self, question):
        ask_user_and_wait(question)
        self._locator.get_mouse_location()
        return locator.coordinates

    def __getitem__(self, key):
        return self._points[key]


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


def click_all_support(locator, controller):
    point_mgr = PointManager(locator)

    point_mgr.ask_for_point(PointNames.NEXT_BUTTON)
    point_mgr.ask_for_point(PointNames.FIRST_SUPPORT_BUTTON)
    point_mgr.ask_for_point(PointNames.SECOND_SUPPORT_BUTTON)

    p_space = Point(point_mgr[PointNames.SECOND_SUPPORT_BUTTON].x
                    - point_mgr[PointNames.FIRST_SUPPORT_BUTTON].x, 0)

    for i in range(0, 31):
        for y in range(0, 5):
            p = Point(point_mgr[PointNames.FIRST_SUPPORT_BUTTON].x + (p_space.x * y),
                      point_mgr[PointNames.FIRST_SUPPORT_BUTTON].y + (p_space.y * y))
            controller.set_position(p)
            controller.left_click()
        controller.set_position(point_mgr[PointNames.NEXT_BUTTON])
        controller.left_click()


def click_all_pubs(locator, controller):
    point_mgr = PointManager(locator)

    point_mgr.ask_for_point(PointNames.NEXT_BUTTON)
    point_mgr.ask_for_point(PointNames.FIRST_PUB_BUTTON)
    point_mgr.ask_for_point(PointNames.SECOND_PUB_BUTTON)

    p_space = Point(point_mgr[PointNames.SECOND_PUB_BUTTON].x -
                    point_mgr[PointNames.FIRST_PUB_BUTTON].x, 0)

    for i in range(0, 31):
        for y in range(0, 5):
            p = Point(point_mgr[PointNames.FIRST_PUB_BUTTON].x + (p_space.x * y),
                      point_mgr[PointNames.FIRST_PUB_BUTTON].y + (p_space.y * y))
            controller.set_position(p)
            controller.left_click()
            controller.left_click()
        controller.set_position(point_mgr[PointNames.NEXT_BUTTON])
        controller.left_click()


if __name__ == "__main__":
    ns = parse_args()
    locator = MouseLocator()

    controller = MouseController()
    controller.delay_before = 0.5
    controller.delay_after = 0.4

    if ns.action == "support":
        click_all_support(locator, controller)
    elif ns.action == "pub":
        click_all_pubs(locator, controller)
