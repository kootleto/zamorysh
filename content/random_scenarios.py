from engine import scenarios_api, gs_api
from gameplay.api import stats, vitals
from interface import ui
import random
from engine import state_api


def random_scenario(state=None):
    def check_tick():
        return {"tick": random.randint(1, 3)}

    state = state_api.init_fn(state, check_tick)

    def ti(gs):
        return gs_api.get_time(gs) == state["tick"]

    def eff(gs):
        vitals.mod(gs, "fatigue", +5)
        ui.display("Вы РАНДОМНО устали")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, ti, eff),
        ]
    )


def random_scenario2(state=None):
    def check_tick2():
        return {"tick": random.randint(4, 6)}

    state = state_api.init_fn(state, check_tick2)

    def ti(gs):
        return gs_api.get_time(gs) == state["tick"]

    def eff(gs):
        r = random.randint(1, 100) # У событий не одинаковые вероятности, потому что в жизни так не бывает.
        if r % 6 == 0:
            stats.mod(gs, "money", -5)
            ui.display(
                "Вы оставили кошелек на Басмаче и оплатили проезд в метро деньгами."
            )
        if r % 6 == 1:
            vitals.mod(gs, vitals.sleepiness, +20)
            ui.display(
                "Одногруппник, сидящий рядом с вами на семинаре, зевнул. Вы тоже зевнули и захотели спать."
            )
        if r % 6 == 2:
            vitals.mod(gs, vitals.mental, -30)
            ui.display(
                "Онет. Вы увидели свою оценку за домашку по Линде. Она меньше 4,7."
            )
        if r % 6 == 3:
            stats.mod(gs, stats.knowledge, +5)
            ui.display(
                "Вы искали что-то в Википедии и случайно перешли по ссылке на статью языка тигринья. Вы чувствуете себя умнее."
            )
        if r % 6 == 4:
            ui.display("ВЫ ПРОИГРАЛИ")
        if r % 6 == 5:
            stats.mod(gs, stats.social, -10)
            ui.display("Вам пришлось говорить о СОПе с одногруппниками. Это тяжело.")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, ti, eff),
        ]
    )


scenarios = [random_scenario, random_scenario2]
