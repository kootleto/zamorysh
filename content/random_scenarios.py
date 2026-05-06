import random

from engine import scenarios_api, gs_api
from engine import state_api
from gameplay.api import stats, vitals, location
from interface import ui


def random_scenario(state=None):
    def check_tick():
        return {"tick": random.randint(1, 3)}

    state = state_api.init_fn(state, check_tick)

    def ti(gs):
        return gs_api.get_time(gs) == state["tick"]

    def eff(gs):
        vitals.mod(gs, vitals.FATIGUE, +5)
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
        r = random.randint(
            1, 100
        )  # У событий не одинаковые вероятности, потому что в жизни так не бывает.
        if r % 6 == 0:
            stats.mod(gs, stats.MONEY, -5)
            ui.display(
                "Вы оставили кошелек на Басмаче и оплатили проезд в метро деньгами."
            )
        if r % 6 == 1:
            vitals.mod(gs, vitals.SLEEPINESS, +20)
            ui.display(
                "Одногруппник, сидящий рядом с вами на семинаре, зевнул. Вы тоже зевнули и захотели спать."
            )
        if r % 6 == 2:
            vitals.mod(gs, vitals.MENTAL, -30)
            ui.display(
                "Онет. Вы увидели свою оценку за домашку по Линде. Она меньше 4,7."
            )
        if r % 6 == 3:
            stats.mod(gs, stats.KNOWLEDGE, +5)
            ui.display(
                "Вы искали что-то в Википедии и случайно перешли по ссылке на статью языка тигринья. Вы чувствуете себя умнее."
            )
        if r % 6 == 4:
            ui.display("ВЫ ПРОИГРАЛИ")
        if r % 6 == 5:
            stats.mod(gs, stats.SOCIAL, -10)
            ui.display("Вам пришлось говорить о СОПе с одногруппниками. Это тяжело.")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, ti, eff),
        ]
    )


def random_home_scenario(state=None):
    def check_tick2():
        return {"tick": random.randint(10, 11), "X": 0, "Y": 0}

    state = state_api.init_fn(state, check_tick2)

    def ti(gs):
        return (
            gs_api.get_time(gs) == state["tick"]
            and location.get(gs, location.Y) == state["Y"]
            and location.get(gs, location.X) == state["X"]
        )

    def eff(gs):
        def f1(gs):
            stats.mod(gs, stats.SOCIAL, -5)
            ui.display("Вы разбили любимую чашку. Жалко.")

        def f2(gs):
            stats.mod(gs, stats.MONEY, +2)
            ui.display("Вы нашли 2$ под подушкой.")

        def f3(gs):
            ui.display("Ничего не произощло")

        spis_func = [f1, f2, f3]
        chs = random.choice(spis_func)
        return chs(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, ti, eff),
        ]
    )


def random_coffeehouse_scenario(state=None):
    def initl():
        # (location.get(gs, location.Y) == 5 and location.get(gs, location.X) == 10) or (location.get(gs, location.Y) == 5 and location.get(gs, location.X) == 60)
        return {"tick": random.randint(20, 25), "X": 10, "Y": 5}

    state = state_api.init_fn(state, initl)

    def us(gs):
        return (
            gs_api.get_time(gs) == state["tick"]
            and location.get(gs, location.Y) == state["Y"]
            and location.get(gs, location.X) == state["X"]
        )

    def efc(gs):
        vitals.mod(gs, vitals.MENTAL, +5)
        ui.display("You got free coffee. Yay.")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, us, efc),
        ]
    )


def random_park_scenario(state=None):
    def initl():
        return {"tick": random.randint(10, 15), "X": 5, "Y": 0}

    state = state_api.init_fn(state, initl)

    def us(gs):
        return (
            gs_api.get_time(gs) == state["tick"]
            and location.get(gs, location.Y) == state["Y"]
            and location.get(gs, location.X) == state["X"]
        )

    def efc(gs):
        vitals.mod(gs, vitals.MENTAL, -5)
        stats.mod(gs, stats.SOCIAL, +5)
        ui.display("You bumped into your classmate. You were forced to have a chat.")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, us, efc),
        ]
    )


SCENARIOS = [
    random_scenario,
    random_scenario2,
    random_coffeehouse_scenario,
    random_park_scenario,
    random_home_scenario,
]
