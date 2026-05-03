from engine import activities_api
from gameplay.api import floor


def move_up():
    def tick_effect(gs):
        floor.mod(gs, 1)

    def can_continue(gs):
        return floor.get(gs) < 5

    return activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required=True,
            name="подняться наверх")


def move_down():
    def tick_effect(gs):
        floor.mod(gs, -1)

    def can_continue(gs):
        return floor.get(gs) > 1

    return activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required=True,
            name="спуститься вниз")
