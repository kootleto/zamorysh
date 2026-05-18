import random

from engine import scenarios_api
from gameplay.api import location, time, vitals
from gameplay.api.location import Place
from interface import ui


def earlybird_scenario():

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
        else:
            vitals.mod(gs, vitals.FATIGUE, +2)
            ui.display(
                "Не повезло! Кто-то забрал ваш бесплатный кофе. (Зато вы не опоздаете в университет...)"
            )

    def tr1(gs):
        return time.get_hour(gs) != 7

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, None),
        ]
    )


SCENARIOS = [earlybird_scenario]
