from engine import gs_api, scenarios_api
from gameplay.api import vitals, stats, time
from interface import ui


def breakdown_scenario():
    def tr1(gs):
        return vitals.get(gs, vitals.MENTAL) == 0

    def eff1():
        ui.display(
            "-- Вы в порядке?... Вы выглядите так, как будто вам очень плохо... --"
        )

    def tr_normal(gs):
        return vitals.get(gs, vitals.MENTAL) >= 25

    def tr2(gs):
        return vitals.get(gs, vitals.MENTAL) == 0

    def eff2(gs):
        ui.display(
            "-- Игра окончена: Вам стоило больше следить за своим ментальным здоровьем. У вас случился нервный срыв и вы отчислились.  -- "
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr1, eff1),
            scenarios_api.base_transition(1, 2, tr_normal, None),
            scenarios_api.base_transition(2, 3, tr2, eff2),
        ]
    )


def verytired_scenario():
    def tr1(gs):
        return vitals.get(gs, vitals.FATIGUE) == 100

    def eff1():
        ui.display("-- Вы чувствуете очень сильную усталость... --")

    def tr_normal(gs):
        return vitals.get(gs, vitals.FATIGUE) <= 75

    def tr2(gs):
        return vitals.get(gs, vitals.FATIGUE) == 100

    def eff2(gs):
        ui.display(
            "-- Игра окончена: вы настолько истощены, что больше ничего не можете делать. -- "
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr1, eff1),
            scenarios_api.base_transition(1, 2, tr_normal, None),
            scenarios_api.base_transition(2, 3, tr2, eff2),
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
            scenarios_api.base_transition(1, 0, lambda gs: not check_rich(gs), None),
            scenarios_api.base_transition(1, 2, check_ultra_rich, game_over),
        ]
    )


def sociable_scenario():
    def check_sociable(gs):
        return stats.get(gs, stats.SOCIAL) >= 500

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


def clever_scenario():
    def check_clever(gs):
        return stats.get(gs, stats.KNOWLEDGE) >= 500

    def game_over(gs):
        ui.display(
            "-- Игра окончена: вы накопили очень много знаний и получили автомат за экзамен! Ура! --"
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_clever, game_over),
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
    rich_scenario,
    breakdown_scenario,
    verytired_scenario,
    sociable_scenario,
    clever_scenario,
    win_scenario,
]
