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
        return floors.get(gs, floors.FLOOR) == floor_number

    def show_classrooms():
        ui.display(f"Аудитории: {", ".join(floors.CLASSROOMS[floor_number])}")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition("out", "in", check, show_classrooms),
            scenarios_api.base_transition(
                "in", "out", lambda gs: not check(gs), lambda: None
            ),
        ]
    )


def first_floor_classrooms():
    return get_classrooms(1)


def second_floor_classrooms():
    return get_classrooms(2)


def third_floor_classrooms():
    return get_classrooms(3)


def fourth_floor_classrooms():
    return get_classrooms(4)


def fifth_floor_classrooms():
    return get_classrooms(5)


SCENARIOS = [
    first_floor,
    second_floor,
    third_floor,
    fourth_floor,
    fifth_floor,
    first_floor_classrooms,
    second_floor_classrooms,
    third_floor_classrooms,
    fourth_floor_classrooms,
    fifth_floor_classrooms,
]
