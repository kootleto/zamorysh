import random

from engine import scenarios_api
from engine.data_api import init_defaults
from gameplay.api import location, time, vitals
from gameplay.api.location import Place
from interface import ui


def earlybird_notice():
    def tr(gs):
        return location.get_place(gs) == Place.SURF_COFFEE

    def eff():
        ui.display(
            "В этой кофейне действует акция: первый покупатель с утра получает бесплатный кофе. "
            "Было бы здорово получить его несколько раз."
        )

    return scenarios_api.base_scenario([scenarios_api.base_transition(0, 1, tr, eff)])


def earlybird_scenario(state=None):

    state = init_defaults(state, counter=0)

    def tr(gs):
        return (
            location.get_place(gs) == Place.SURF_COFFEE
            and time.get_hour(gs) == 7
            and time.get_minute(gs) == 0
        )

    def eff(gs):
        if random.choice([True, False]):
            vitals.mod(gs, vitals.MENTAL, -2)
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            ui.display(
                "Поздравляю! Вы первый покупатель. Наслаждайтесь своим бесплатным кофе!"
            )

            state["counter"] += 1

        else:
            vitals.mod(gs, vitals.FATIGUE, +2)
            ui.display(
                "Не повезло! Кто-то забрал ваш бесплатный кофе. (Зато вы не опоздаете в университет...)"
            )

        if state["counter"] == 1:
            ui.display("Первый есть!")
        if state["counter"] == 2:
            ui.display("Ещё немного...")

        if state["counter"] == 3:
            ui.display("Вы настоящая ранняя пташка!")
            vitals.set(gs, vitals.SLEEPINESS, 0)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 0, tr, eff),
        ]
    )


SCENARIOS = [earlybird_scenario]
