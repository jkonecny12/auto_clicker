#!/usr/bin/python3

import time
import os

from enum import Enum
from configparser import ConfigParser

from autoclicker import MouseLocator, MouseController, Point
from argparse import ArgumentParser


CONFIG_PATH = os.path.expanduser("~/.config/foe-clicker/foe-clicker.config")


class PointNames(Enum):
    NEXT_BUTTON = "next_left"

    FIRST_SUPPORT_BUTTON = "first_support"
    SECOND_SUPPORT_BUTTON = "second_support"

    FIRST_PUB_BUTTON = "first_pub"
    SECOND_PUB_BUTTON = "second_pub"

    def get_description(self):
        if self is PointNames.NEXT_BUTTON:
            return "Next 5 people"
        elif self is PointNames.FIRST_SUPPORT_BUTTON:
            return "First support"
        elif self is PointNames.SECOND_SUPPORT_BUTTON:
            return "Second support"
        elif self is PointNames.FIRST_PUB_BUTTON:
            return "First pub"
        elif self is PointNames.SECOND_PUB_BUTTON:
            return "Second pub"


class PointManager(object):
    """Store and load points used for further runs."""

    _MAIN_SECTION = "MAIN"

    def __init__(self, locator):
        self._points = {}
        self._locator = locator

    def add_point(self, name, position):
        self._points[name] = position

    def ask_for_point(self, point):
        pos = self._get_position("Move cursor to the {} button".format(point.get_description()))
        self.add_point(point, pos)

    def _get_position(self, question):
        ask_user_and_wait(question)
        self._locator.get_mouse_location()
        return locator.coordinates

    def has_point(self, point_name):
        if point_name in self._points:
            return True
        else:
            return False

    def has_points(self, point_names):
        for name in point_names:
            if not self.has_point(name):
                return False

        return True

    def save_points(self):
        config_parser = ConfigParser()

        config_parser[self._MAIN_SECTION] = {}
        main = config_parser[self._MAIN_SECTION]

        for key, point in self._points.items():
            main[key.value] = "{} {}".format(point.x, point.y)

        self._create_config_dir()

        with open(CONFIG_PATH, "w") as fd:
            config_parser.write(fd)

    def load_points(self):
        if not os.path.exists(CONFIG_PATH):
            return False

        config_parser = ConfigParser()
        config_parser.read(CONFIG_PATH)

        main = config_parser[self._MAIN_SECTION]

        for key in main:
            x, y = main[key].split(" ")
            self.add_point(PointNames(key), Point(int(x), int(y)))

        return True

    @staticmethod
    def _create_config_dir():
        conf_dir = os.path.dirname(CONFIG_PATH)
        if not os.path.exists(conf_dir):
            os.makedirs(conf_dir)

    def __getitem__(self, key):
        return self._points[key]


def parse_args():
    parser = ArgumentParser(description="Automatic mouse controller to visit all neighbors in one"
                            "game")

    parser.add_argument("action", action="store", type=str, choices=["support", "pub", "store"],
                        help="""Run script for giving supports or visiting pubs.""")

    return parser.parse_args()


def ask_user_and_wait(question):
    print(question)
    input("Press any key and wait 3 secs")
    print("=============================")
    time.sleep(3)


def test_missing_points(point_manager, points):
    if not point_manager.has_points(points):
        print("Some points are not stored")
        print("Please run the application with a 'store' command")
        return False

    return True


def click_all_support(locator, controller):
    point_mgr = PointManager(locator)
    point_mgr.load_points()

    if not test_missing_points(point_mgr,
                               [PointNames.NEXT_BUTTON,
                                PointNames.FIRST_SUPPORT_BUTTON,
                                PointNames.SECOND_SUPPORT_BUTTON]):
        return

    _run_clicking_cycle(first_action_point=point_mgr[PointNames.FIRST_SUPPORT_BUTTON],
                        second_action_point=point_mgr[PointNames.SECOND_SUPPORT_BUTTON],
                        next_button_point=point_mgr[PointNames.NEXT_BUTTON],
                        confirmation_click=False)


def click_all_pubs(locator, controller):
    point_mgr = PointManager(locator)
    point_mgr.load_points()

    if not test_missing_points(point_mgr,
                               [PointNames.NEXT_BUTTON,
                                PointNames.FIRST_PUB_BUTTON,
                                PointNames.SECOND_PUB_BUTTON]):
        return

    _run_clicking_cycle(first_action_point=point_mgr[PointNames.FIRST_PUB_BUTTON],
                        second_action_point=point_mgr[PointNames.SECOND_PUB_BUTTON],
                        next_button_point=point_mgr[PointNames.NEXT_BUTTON],
                        confirmation_click=True)


def _run_clicking_cycle(first_action_point, second_action_point, next_button_point,
                        confirmation_click):
    p_space = Point(second_action_point.x - first_action_point.x, 0)

    for i in range(0, 31):
        for y in range(0, 5):
            p = Point(first_action_point.x + (p_space.x * y),
                      first_action_point.y + (p_space.y * y))
            controller.set_position(p)
            controller.left_click()
            if confirmation_click:
                controller.left_click()
        controller.set_position(next_button_point)
        controller.left_click()


def store_points(locator):
    point_mgr = PointManager(locator)

    point_mgr.ask_for_point(PointNames.NEXT_BUTTON)
    point_mgr.ask_for_point(PointNames.FIRST_SUPPORT_BUTTON)
    point_mgr.ask_for_point(PointNames.SECOND_SUPPORT_BUTTON)
    point_mgr.ask_for_point(PointNames.FIRST_PUB_BUTTON)
    point_mgr.ask_for_point(PointNames.SECOND_PUB_BUTTON)

    point_mgr.save_points()


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
    elif ns.action == "store":
        store_points(locator)
