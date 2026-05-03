from engine import scenarios_api
from gameplay.api import location
from interface import ui


def move_scenario(place):
    def check(gs):
        return location.get_place(gs) == place

    def enter():
        ui.display(f"You are entering {place}!")

    def exit():
        ui.display(f"You are exiting {place}!")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, "in", check, lambda: None),
            scenarios_api.base_transition(
                0, "out", lambda gs: not check(gs), lambda: None
            ),
            scenarios_api.base_transition("out", "in", check, enter),
            scenarios_api.base_transition("in", "out", lambda gs: not check(gs), exit),
        ]
    )


def home_scenario():
    return move_scenario("home")


def metro_scenario():
    return move_scenario("metro")


def coffee_scenario():
    return move_scenario("coffee house")


def club_scenario():
    return move_scenario("club")


def park_scenario():
    return move_scenario("park")


def university_scenario():
    return move_scenario("university")


SCENARIOS = [
    home_scenario,
    metro_scenario,
    coffee_scenario,
    club_scenario,
    park_scenario,
    university_scenario,
]
