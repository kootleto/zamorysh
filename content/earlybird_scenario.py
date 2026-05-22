import random

from engine import scenarios_api
from engine.state_api import init_fn
from gameplay.api import location, time, vitals
from gameplay.api.location import Place
from interface import ui


def earlybird_scenario(state=None):
    def init():
        return {"counter": 0}

    state = init_fn(state, init)

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
                "Поздравляю! Вы - первый покупатель. Наслаждайтесь своим бесплатным кофе!"
            )

            state["counter"] += 1

        else:
            vitals.mod(gs, vitals.FATIGUE, +2)
            ui.display(
                "Не повезло! Кто-то забрал ваш бесплатный кофе. (Зато вы не опоздаете в университет...)"
            )

    def tr1(gs):
        return time.get_minute(gs) != 0

    def tr_1(gs):
        return location.get_place(gs) == Place.SURF_COFFEE

    def eff_1():
        ui.display(
            "В этой кофейне действует акция: первый покупатель с утра получает бесплатный кофе. Было бы здорово получить его несколько раз."
        )

    def tr_2():
        return state["counter"] == 1

    def eff_2():
        ui.display("Первый есть!")

    def tr_3():
        return state["counter"] == 3

    def eff_3():
        ui.display("Ранняя пташка хватает кофейка!")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, None),
            # scenarios_api.base_transition(0, 3, tr_1, eff_1),
            # scenarios_api.base_transition(1, 2, tr_2, eff_2),
            scenarios_api.base_transition(1, 2, tr_3, eff_3),
        ]
    )


SCENARIOS = [earlybird_scenario]
