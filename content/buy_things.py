import random

import keyboard

from gameplay.api import location
from engine import activities_api, state_api
from gameplay.activity_wrappers import single_tick_activity, timed_activity
from gameplay.api import vitals, stats
from gameplay.api.location import y, x
from interface import ui


def buy_drink1(hold_required=False, state=None):
    # def can_continue(gs):
    # return stats.get(gs, stats.money) < 0
    # state = state_api.init_defaults(state, counter=1)

    def tick_effect(gs):
        ui.display("Buy coffee1 for 2$? (Press a + Enter)")
        ui.display("Buy coffee2 for 2$? (Press b + Enter)")
        vv = ui.prompt("Pick your poison: ")
        if vv == "a":
            vitals.mod(gs, vitals.fatigue, -5)
            stats.mod(gs, stats.money, -2)
            ui.display("You bought tasty coffee1. You feel better.")
        if vv == "b":
            vitals.mod(gs, vitals.fatigue, -5)
            stats.mod(gs, stats.money, -2)
            ui.display("You bought tasty coffee2. You feel better.")
        # if keyboard.is_pressed("space"):
        # keyboard.write("\n You chose a")

        # state["counter"] -= 1
        # if keyboard.is_pressed("b"):
        # vitals.mod(gs, vitals.fatigue, -5)
        # stats.mod(gs, stats.money, -0)
        # ui.display("You bought coffee. You feel better.")
        # state["counter"] -= 1
        # else:
        # 1 == 1

    def can_continue(gs):
        return stats.get(gs, stats.money) > 2 and (
            (location.get(gs, y) == 5 and location.get(gs, x) == 10)
            or (location.get(gs, y) == 5 and location.get(gs, x) == 60)
        )
        # return stats.get(gs, stats.money) > 2

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required,
            name="buy_drink",
        ),
        state,
    )


activities = [buy_drink1]
