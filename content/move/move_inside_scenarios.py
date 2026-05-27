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


def wrong_room():
    def check_wrong(gs):
        return (
            location.get_place(gs) == location.Place.UNIVERSITY
            and schedule.get_current_room(gs) != floors.get(gs, floors.CLASSROOM)
            and floors.get(gs, floors.CLASSROOM) != 0
            and floors.get(gs, floors.CLASSROOM) != 107
            and floors.get(gs, floors.CLASSROOM) != 405
            and floors.get(gs, floors.CLASSROOM) != 1
        )

    def wrong():
        ui.display(
            f"У вас сейчас нет пары в этой аудитории. Здесь {random.choice(["свободно", "семинар по филологии", "конференция", "пара по китайскому"])}."
        )

    def check_restart(gs):
        return floors.get(gs, floors.CLASSROOM) == 0

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_wrong, wrong),
            scenarios_api.base_transition(1, 0, check_restart, None),
        ]
    )


def designers_room():
    def check_designers(gs):
        return floors.get(gs, floors.CLASSROOM) == 1

    def desighers():
        ui.display("Здесь обитают дизайнеры.")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_designers, desighers),
            scenarios_api.base_transition(
                1, 0, lambda gs: not check_designers(gs), None
            ),
        ]
    )


SCENARIOS = [
    zero_floor,
    first_floor,
    second_floor,
    third_floor,
    fourth_floor,
    fifth_floor,
    wrong_room,
    designers_room,
]
