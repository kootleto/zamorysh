from engine import scenarios_api
from gameplay.api import floors
from interface import ui


def floor_scenario(floor_number):
    def check(gs):
        return floors.get(gs, floors.FLOOR) == floor_number

    def enter():
        ui.display(f"{floor_number} этаж")

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


def first_floor():
    return floor_scenario(1)


def second_floor():
    return floor_scenario(2)


def third_floor():
    return floor_scenario(3)


def fourth_floor():
    def check(gs):
        return floors.get(gs, floors.FLOOR) == 4

    def enter():
        ui.display("Fourth floor")

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


SCENARIOS = [
    first_floor,
    second_floor,
    third_floor,
    fourth_floor,
    fifth_floor,
]
