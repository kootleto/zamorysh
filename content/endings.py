from engine import gs_api, scenarios_api
from engine.data_api import init_defaults
from gameplay.api import time, vitals, stats
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
            "-- Игра окончена: вам стоило больше следить за своим ментальным здоровьем. "
            "У вас случился нервный срыв и вы отчислились.  -- "
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr1, eff1),
            scenarios_api.base_transition(1, 2, tr2, eff2),
        ]
    )


def verytired_scenario(state=None):
    def tr1(gs):
        return vitals.get(gs, vitals.FATIGUE) == 100

    def eff1():
        ui.display("-- Вы чувствуете очень сильную усталость... --")
        state["counter"] += 1

    def tr2(gs):
        return vitals.get(gs, vitals.MENTAL) == 0 and state["counter"] == 2

    def eff2(gs):
        ui.display(
            "-- Игра окончена: вы настолько истощены, что больше ничего не можете делать. -- "
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr1, eff1),
            scenarios_api.base_transition(1, 2, tr2, eff2),
        ]
    )


def rich_scenario():
    def check_rich(gs):
        return stats.get(gs, stats.MONEY) >= 200

    def congratulations():
        ui.display("-- Вау! Вы так богаты! --")

    def check_ultra_rich(gs):
        return stats.get(gs, stats.MONEY) >= 300

    def game_over(gs):
        ui.display("-- Игра окончена: вы слишком богаты для студента. --")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_rich, congratulations),
            scenarios_api.base_transition(1, 2, lambda gs: not check_rich(gs), None),
            scenarios_api.base_transition(1, 2, check_ultra_rich, game_over),
        ]
    )


def sociable_scenario():
    def check_sociable(gs):
        return stats.get(gs, stats.MONEY) >= 500

    def game_over(gs):
        ui.display(
            "-- Игра окончена: вы завели столько полезных знакомств, "
            "что вам уже не нужно учиться в университете. --"
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_sociable, game_over),
        ]
    )


def win_scenario():

    def check_time(gs):
        return time.get_day(gs) >= 8

    def successfully_survived(gs):
        ui.display(
            "-- Хорошая концовка: вы героически пережили неделю! Удачи пережить ещё много недель... -- "
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 1, check_time, successfully_survived)]
    )


SCENARIOS = [
    rich_scenario,
    breakdown_scenario,
    verytired_scenario,
    win_scenario,
]
