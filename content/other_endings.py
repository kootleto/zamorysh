from engine import gs_api, scenarios_api
from gameplay.api import vitals, stats, time, scenes
from interface import ui


def breakdown_ending_trigger(gs):
    return vitals.get(gs, vitals.MENTAL) == 0


def breakdown_scenario():
    def eff1():
        ui.display(
            "-- Вы в порядке?... Вы выглядите так, как будто вам очень плохо... --"
        )

    def tr_normal(gs):
        return vitals.get(gs, vitals.MENTAL) >= 25

    def eff2(gs):
        ui.display(
            "-- Игра окончена: Вам стоило больше следить за своим ментальным здоровьем. У вас случился нервный срыв и вы отчислились.  -- "
        )
        scenes.set_sprite(gs, "dead.png")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, breakdown_ending_trigger, eff1),
            scenarios_api.base_transition(1, 2, tr_normal, None),
            scenarios_api.base_transition(2, 3, breakdown_ending_trigger, eff2),
        ]
    )


def tired_ending_trigger(gs):
    return vitals.get(gs, vitals.FATIGUE) == 100


def verytired_scenario():
    def eff1():
        ui.display("-- Вы чувствуете очень сильную усталость... --")

    def tr_normal(gs):
        return vitals.get(gs, vitals.FATIGUE) <= 75

    def eff2(gs):
        ui.display(
            "-- Игра окончена: вы настолько истощены, что больше ничего не можете делать. -- "
        )
        scenes.set_sprite(gs, "dead.png")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tired_ending_trigger, eff1),
            scenarios_api.base_transition(1, 2, tr_normal, None),
            scenarios_api.base_transition(2, 3, tired_ending_trigger, eff2),
        ]
    )


def rich_ending_trigger(gs):
    return stats.get(gs, stats.MONEY) >= 300


def rich_scenario():
    def check_rich(gs):
        return stats.get(gs, stats.MONEY) >= 200

    def congratulations():
        ui.display("-- Вау! Вы так богаты! --")

    def game_over(gs):
        ui.display("-- Игра окончена: вы слишком богаты для студента. --")
        scenes.set_sprite(gs, "happy.png")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_rich, congratulations),
            scenarios_api.base_transition(1, 0, lambda gs: not check_rich(gs), None),
            scenarios_api.base_transition(1, 2, rich_ending_trigger, game_over),
        ]
    )


def social_ending_trigger(gs):
    return stats.get(gs, stats.SOCIAL) >= 500


def sociable_scenario():
    def game_over(gs):
        ui.display(
            "-- Игра окончена: вы завели столько полезных знакомств, "
            "что вам уже не нужно учиться в университете. --"
        )
        scenes.set_sprite(gs, "happy.png")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, social_ending_trigger, game_over),
        ]
    )


def clever_ending_trigger(gs):
    return stats.get(gs, stats.KNOWLEDGE) >= 500


def clever_scenario():

    def game_over(gs):
        ui.display(
            "-- Игра окончена: вы накопили очень много знаний и получили автомат за экзамен! Ура! --"
        )
        scenes.set_sprite(gs, "smart.png")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, clever_ending_trigger, game_over),
        ]
    )


def win_ending_trigger(gs):
    return time.get_day(gs) >= 8


def win_scenario():
    def successfully_survived(gs):
        ui.display(
            "-- Хорошая концовка: Вы героически пережили неделю! Удачи пережить еще много недель... -- "
        )
        scenes.set_sprite(gs, "happy.png")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 1, win_ending_trigger, successfully_survived)]
    )


SCENARIOS = [
    rich_scenario,
    breakdown_scenario,
    verytired_scenario,
    sociable_scenario,
    clever_scenario,
    win_scenario,
]
