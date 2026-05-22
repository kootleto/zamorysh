import random

from engine import activities_api
from gameplay.activity_wrappers import single_tick_activity
from gameplay.api import location, time
from gameplay.api import vitals, stats
from gameplay.api.location import Place
from interface import ui


def buy_drink1(hold_required=False, state=None):
    # def can_continue(gs):
    # return stats.get(gs, stats.money) < 0
    # state = data_api.init_defaults(state, counter=1)

    async def tick_effect(gs):
        ui.display("Купить латте? (Press a + Enter)")
        ui.display("Купить американо?  (Press b + Enter)")
        vv = await ui.prompt("Pick your poison: ")
        if vv == "a":
            vitals.mod(gs, vitals.FATIGUE, -5)
            stats.mod(gs, stats.MONEY, -15)
            ui.display("You bought tasty coffee1. You feel better.")
        if vv == "b":
            vitals.mod(gs, vitals.FATIGUE, -5)
            stats.mod(gs, stats.MONEY, -15)
            ui.display("You bought tasty coffee2. You feel better.")

    def can_continue(gs):
        return stats.get(gs, stats.MONEY) > 9 and (
            (
                location.get_place(gs) == Place.SURF_COFFEE
                or location.get_place(gs) == Place.ANOTHER_COFFEE
            )
            and 6 < time.get_hour(gs) < 23
        )

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required,
            name="buy_drink",
        ),
        state,
    )


def read_menu(state=None):
    def tick_effect():
        ui.display("Добро пожаловать в Surf Coffee!")
        ui.display("На данный момент в меню доступны следующие позиции:")
        ui.display("a. Латте  9$ | 15$")
        ui.display("b. Американо 8$ | -")
        ui.display("c. Капучино 11$ | 17$")
        if random.choice([True, False]):
            ui.display(
                "d. Раф кокосовая свежесть на миндальном молоке с инжиром 19$ | 23$"
            )

    def can_continue(gs):
        return (
            6 < time.get_hour(gs) < 23 and location.get_place(gs) == Place.SURF_COFFEE
        )

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect=tick_effect,
            can_continue=can_continue,
            name="read_menu",
        ),
        state,
    )


ACTIVITIES = [buy_drink1, read_menu]
