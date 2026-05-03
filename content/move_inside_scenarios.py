from engine import scenarios_api
from gameplay.api import floor
from interface import ui


def floor_scenario(floor_number):
    def check(gs):
        return floor.get(gs) == floor_number

    def enter():
        ui.display(f"{floor_number} этаж")

    return scenarios_api.base_scenario(
        [
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
    return floor_scenario(4)


def fifth_floor():
    return floor_scenario(5)


def get_classrooms(floor_number):
    def check(gs):
        return floor.get(gs) == floor_number

    def show_classrooms():
        ui.display(f"Аудитории: {", ".join(floor.CLASSROOMS[floor_number])}")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition("out", "in", check, show_classrooms),
            scenarios_api.base_transition(
                "in", "out", lambda gs: not check(gs), lambda: None
            ),
        ]
    )
