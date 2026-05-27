import random

from engine import data_api, scenarios_api
from gameplay.api import time, location
from gameplay.api.location import Place
from interface import ui


def generate_outside_coords():
    all_coords = [
        (x, y)
        for x in range(location.WEST_BORDER, location.EAST_BORDER + 1)
        for y in range(location.SOUTH_BORDER, location.NORTH_BORDER + 1)
    ]

    outside_coords = [
        (x, y)
        for x, y in all_coords
        if location.get_place_by_coords(x, y) == Place.OUTSIDE
    ]
    return random.choice(outside_coords)


def key_lost_quest(state=None):
    state = data_api.init_defaults(state, key_x=None, key_y=None)

    def warning_trigger(gs):
        return (
            time.get_day(gs) >= time.START_DATETIME.day + 1
            and time.get_hour(gs) >= 12
            and location.get_place(gs) != Place.HOME
        )

    def start(gs):
        ui.display("Почему-то у вас плохое предчувствие...")
        location.lock(gs, Place.HOME, "key_lost")

    def activate_loss(gs):
        return location.get(gs, location.X) == 0 and location.get(gs, location.Y) == 0

    def home_locked():
        ui.display(
            "Вы потеряли ключи. Вы не помните, где вы видели их в последний раз."
        )
        state["key_x"], state["key_y"] = generate_outside_coords()

    def find_trigger(gs):
        return (
            location.get(gs, location.X) == state["key_x"]
            and location.get(gs, location.Y) == state["key_y"]
        )

    def key_found(gs):
        if 5 <= time.get_hour(gs) <= 8:
            key_msg = "На асфальте что-то блестит в лучах восходящего солнца."
        elif 9 <= time.get_hour(gs) <= 16:
            key_msg = "На асфальте что-то блестит, отражая солнечные лучи."
        elif 17 <= time.get_hour(gs) <= 21:
            key_msg = "На асфальте что-то блестит в огненных лучах закатного солнца."
        else:
            key_msg = (
                "От асфальта отражается тусклый лунный свет. На асфальте что-то лежит."
            )

        ui.display_at(gs, key_msg + " Вы нашли свои ключи.")
        location.unlock(gs, Place.HOME, "key_lost")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, warning_trigger, start),
            scenarios_api.base_transition(1, 2, activate_loss, home_locked),
            scenarios_api.base_transition(2, 3, find_trigger, key_found),
        ]
    )


SCENARIOS = [key_lost_quest]
