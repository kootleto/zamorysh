from engine.activities_api import base_activity
from gameplay.activity_wrappers import single_tick_activity
from gameplay.api import location, floors
from gameplay.api.location import Place
from interface import ui


def move_up():
    def tick_effect(gs):
        floors.mod_floor(gs, 1)

    def can_continue(gs):
        return (
            floors.get(gs, floors.FLOOR) < 5
            and location.get_place(gs) == Place.UNIVERSITY
        )

    return base_activity(
        tick_effect, can_continue, hold_required=True, name="подняться наверх"
    )


def move_down():
    def tick_effect(gs):
        floors.mod_floor(gs, -1)

    def can_continue(gs):
        return (
            floors.get(gs, floors.FLOOR) > 0
            and location.get_place(gs) == Place.UNIVERSITY
            and floors.get(gs, floors.CLASSROOM) == 0
        )

    return base_activity(
        tick_effect, can_continue, hold_required=True, name="спуститься вниз"
    )


def go_to_classroom(state=None):
    async def tick_effect(gs):
        classrooms = floors.CLASSROOMS[floors.get(gs, floors.FLOOR)]
        ui.display(f"Выберите аудиторию: {", ".join(map(str, classrooms))}")
        floors.set(gs, floors.CLASSROOM, int(await ui.prompt()))

    def can_continue(gs):
        return (
            location.get_place(gs) == Place.UNIVERSITY
            # and floors.get(gs, floors.FLOOR) != 1
            and floors.get(gs, floors.CLASSROOM) == 0
        )

    return single_tick_activity(
        base_activity(tick_effect, can_continue, name="пойти в аудиторию"), state
    )


def go_out_of_classroom(state=None):
    def tick_effect(gs):
        floors.set(gs, floors.CLASSROOM, 0)

    def can_continue(gs):
        return floors.get(gs, floors.CLASSROOM) != 0

    return single_tick_activity(
        base_activity(tick_effect, can_continue, name="выйти из аудитории"), state
    )


ACTIVITIES = [move_up, move_down, go_to_classroom, go_out_of_classroom]
