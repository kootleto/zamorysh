import random

from engine import scenarios_api
from gameplay.api import floors, schedule, location
from interface import ui


def floor_scenario(floor_number):
    def check(gs):
        return floors.get(gs, floors.FLOOR) == floor_number

    def enter(gs):
        ui.display_at(gs, f"{floor_number} этаж")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, "in", check, lambda: None),
            scenarios_api.base_transition(
                0, "out", lambda gs: not check(gs), lambda: None
            ),
            scenarios_api.base_transition("out", "in", check, enter),
            scenarios_api.base_transition(
                "in", "out", lambda gs: not check(gs), lambda: None
            ),
        ]
    )


def zero_floor():
    return floor_scenario(0)


def first_floor():
    return floor_scenario(1)


def second_floor():
    return floor_scenario(2)


def third_floor():
    return floor_scenario(3)


def fourth_floor():
    def check(gs):
        return floors.get(gs, floors.FLOOR) == 4

    def enter(gs):
        ui.display_at(gs, "Fourth floor")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, "in", check, lambda: None),
            scenarios_api.base_transition(
                0, "out", lambda gs: not check(gs), lambda: None
            ),
            scenarios_api.base_transition("out", "in", check, enter),
            scenarios_api.base_transition(
                "in", "out", lambda gs: not check(gs), lambda: None
            ),
        ]
    )


def fifth_floor():
    return floor_scenario(5)


def wrong_class():
    def check_wrong(gs):
        return location.get_place(
            gs
        ) == location.Place.UNIVERSITY and schedule.get_current_room(gs) != floors.get(
            gs, floors.CLASSROOM
        )

    def wrong():
        ui.display(
            f"У вас сейчас пара в другой аудитории. Здесь {random.choice(["нет пар", "семинар по филологии", "конференция", "пара по китайскому"])}"
        )

    def check_restart(gs):
        return floors.get(gs, floors.CLASSROOM) == 0

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_wrong, wrong),
            scenarios_api.base_transition(1, 0, check_restart, None),
        ]
    )


SCENARIOS = [
    zero_floor,
    first_floor,
    second_floor,
    third_floor,
    fourth_floor,
    fifth_floor,
]
