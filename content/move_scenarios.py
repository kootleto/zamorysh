from engine import scenarios_api
from gameplay.api import location
from gameplay.api.location import Place, PLACES_FORMS
from interface import ui


def move_scenario(place):
    def check(gs):
        return location.get_place(gs) == place

    def enter(gs):
        ui.display_at(gs, f"Вы входите в {place["in"]}!")

    def exit(gs):
        ui.display_at(gs, f"Вы выходите из {place["out"]}!")

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
    return move_scenario(PLACES_FORMS[Place.HOME])


def metro_scenario():
    return move_scenario(Place.METRO)


def surfcoffee_scenario():
    return move_scenario(Place.SURF_COFFEE)


def anothercoffee_scenario():
    return move_scenario(Place.ANOTHER_COFFEE)


def club_scenario():
    return move_scenario(Place.CLUB)


def park_scenario():
    return move_scenario(Place.PARK)


def university_scenario():
    return move_scenario(Place.UNIVERSITY)


SCENARIOS = [
    home_scenario,
    metro_scenario,
    surfcoffee_scenario,
    anothercoffee_scenario,
    club_scenario,
    park_scenario,
    university_scenario,
]
