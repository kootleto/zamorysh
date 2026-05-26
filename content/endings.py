from engine import gs_api, scenarios_api
from engine.data_api import init_defaults
from gameplay.api import time, vitals
from interface import ui


def breakdown_scenario(state=None):
    state = init_defaults(state, counter=0)

    def tr1(gs):
        return vitals.get(gs, vitals.MENTAL) == 0

    def eff1():
        ui.display(
            "-- Вы в порядке?... Вы выглядите так, как будто вам очень плохо... --"
        )
        state["counter"] += 1

    def tr2(gs):
        return vitals.get(gs, vitals.MENTAL) == 0 and state["counter"] == 2

    def eff2(gs):
        ui.display(
            "-- Игра окончена: Вам стоило больше следить за своим ментальным здоровьем. У вас случился нервный срыв и вы отчислились.  -- "
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr1, eff1),
            scenarios_api.base_transition(1, 2, tr1, eff1),
            scenarios_api.base_transition(2, 3, tr2, eff2),
        ]
    )


def win_scenario():

    def check_time(gs):
        return time.get_day(gs) >= 8

    def successfully_survived(gs):
        ui.display(
            "-- Хорошая концовка: Вы героически пережили неделю! Удачи пережить еще много недель... -- "
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 1, check_time, successfully_survived)]
    )


SCENARIOS = [
    # rich_scenario,
    breakdown_scenario,
    # verytired_scenario,
    win_scenario,
]
