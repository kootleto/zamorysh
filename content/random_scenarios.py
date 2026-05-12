import random

from engine import scenarios_api, gs_api
from engine import state_api
from engine.state_api import init_fn
from gameplay.api import stats, vitals, location
from gameplay.api import time
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

    def tr(gs):
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
            scenarios_api.base_transition(0, 1, tr, eff),
        ]
    )


def random_home_scenario(state=None):

    hour = random.randint(0, 23)
    minute = random.randint(0, 59)

    def tr(gs):
        return (
            time.get_hour(gs) == hour
            and time.get_minute(gs) == minute
            and location.get_place(gs) == "home"
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

        functions = [f1, f2, f3]
        chs = random.choice(functions)
        return chs(gs)

    def tr1(gs):
        return time.get_hour(gs) != hour

    def eff1(gs):
        pass  # Эффекта нет

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, eff1),
        ]
    )


def random_park_day_scenario(state=None):

    hour = random.randint(7, 21)  # В такое время в парке скорее такой набор событий.
    minute = random.randint(0, 59)

    def tr(gs):
        return (
            location.get_place(gs) == "park"
            and time.get_hour(gs) == hour
            and time.get_minute(gs) == minute
        )

    def eff(gs):
        def f1(gs):
            vitals.mod(gs, vitals.MENTAL, -5)
            stats.mod(gs, stats.SOCIAL, +5)
            ui.display("Вы столкнулись с одногруппником. Вам пришлось разговаривать.")

        def f2(gs):
            ui.display("Вы наступили в лужу и простудились.")
            vitals.mod(gs, vitals.FATIGUE, -7)

        def f3(gs):
            ui.display("Вы встретили Ландера. Вам ужасно неловко.")
            stats.mod(gs, stats.SOCIAL, -5)
            vitals.mod(gs, vitals.MENTAL, -5)

        def f4(gs):
            ui.display("Вам всучили брошюрку о вреде алкоголя. Вы и не собирались...")
            stats.mod(gs, stats.KNOWLEDGE, +5)

        def f5(gs):
            ui.display("Вы нашли траву и ПОТРОГАЛИ ее.")
            stats.mod(gs, stats.MENTAL, +15)
            vitals.mod(gs, vitals.FATIGUE, -10)

        def f6(gs):
            ui.display(
                "Собака, гуляющая в парке, украла ваш студак. Пока вы бежали за ней и отнимали его, вы очень устали."
            )
            vitals.mod(gs, vitals.FATIGUE, -5)

        def f7(gs):
            ui.display(
                "Вода в парке очень красиво плещется. Вы засмотрелись на нее, и она убаюкала вас... "
            )
            vitals.mod(gs, vitals.SLEEPINESS, +7)

        def f8(gs):
            ui.display(
                "С вами завел беседу бомж. Вы рассказали ему о своей курсовой. Он расстроился и дал вам 5 рублей."
            )
            stats.mod(gs, stats.MONEY, +5)

        def f9(gs):
            ui.display(
                "Вы увидели уведомление от тгк <<на старой басманной все спокойно>> и обрадовались!"
            )
            stats.mod(gs, stats.MENTAL, +5)

        def f10(gs):
            ui.display(
                "Солнце светило ярко, и вы решили поботать на природе... но ветер унес листы из вашего конспекта по дискре!"
            )
            stats.mod(gs, stats.KNOWLEDGE, -10)

        functions = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
        chs = random.choice(functions)
        return chs(gs)

    def tr1(gs):
        return time.get_hour(gs) != hour

    def eff1(gs):
        pass  # Эффекта нет

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, eff1),
        ]
    )


def random_scenario_somewhere(events, hours, place, cooldown, state=None):
    def init():
        return {
            "minutes": random.randint(0, 9),
            "cooldown": random.randint(0, cooldown - 1),
        }

    state = init_fn(state, init)

    def tr(gs):
        return (
            location.get_place(gs) == place
            and time.get_hour(gs) in hours
            and time.get_minute(gs) % 10 == state["minutes"]
        )

    def eff(gs):
        chs = random.choice(events)
        state.update(init())
        chs(gs)

    def tr1(gs):
        return time.get_minute(gs) % cooldown != state["cooldown"]

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, None),
        ]
    )


def random_park_night_scenario2(state=None):
    def f1(gs):
        vitals.mod(gs, vitals.MENTAL, -5)
        ui.display("Фонарь резко заморгал. Вы испугались.")

    def f2(gs):
        ui.display("Вы наступили в лужу и простудились.")
        vitals.mod(gs, vitals.FATIGUE, -7)

    def f3(gs):
        ui.display("Вы встретили Ландера. Вам ужасно неловко.")
        stats.mod(gs, stats.SOCIAL, -5)
        vitals.mod(gs, vitals.MENTAL, -5)

    def f4(gs):
        ui.display("Вам всучили брошюрку о вреде алкоголя. Вы и не собирались...")
        stats.mod(gs, stats.KNOWLEDGE, +5)

    def f5(gs):
        ui.display("Вы нашли траву и ПОТРОГАЛИ ее.")
        stats.mod(gs, stats.MENTAL, +15)
        vitals.mod(gs, vitals.FATIGUE, -10)

    def f6(gs):
        ui.display(
            "Собака, гуляющая в парке, украла ваш студак. Пока вы бежали за ней и отнимали его, вы очень устали."
        )
        vitals.mod(gs, vitals.FATIGUE, -5)

    def f7(gs):
        ui.display(
            "Вода в парке очень красиво плещется. Вы засмотрелись на нее, и она убаюкала вас... "
        )
        vitals.mod(gs, vitals.SLEEPINESS, +7)

    def f8(gs):
        ui.display(
            "С вами завел беседу бомж. Вы рассказали ему о своей курсовой. Он расстроился и дал вам 5 рублей."
        )
        stats.mod(gs, stats.MONEY, +5)

    def f9(gs):
        ui.display(
            "Вы увидели уведомление от тгк <<на старой басманной все спокойно>> и обрадовались!"
        )
        vitals.mod(gs, vitals.MENTAL, +5)

    def f10(gs):
        ui.display(
            "Солнце светило ярко, и вы решили поботать на природе... но ветер унес листы из вашего конспекта по дискре!"
        )
        stats.mod(gs, stats.KNOWLEDGE, -10)

    events = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    hours = [0, 1, 2, 3, 4, 5, 6, 22, 23]
    cooldown = 20
    place = "park"

    return random_scenario_somewhere(events, hours, place, cooldown, state)


def random_park_night_scenario(state=None):
    def init():
        return {"minutes": random.randint(0, 9), "cooldown": random.randint(0, 19)}

    hours = [0, 1, 2, 3, 4, 5, 6, 22, 23]

    state = init_fn(state, init)

    def tr(gs):
        return (
            location.get_place(gs) == "park"
            and time.get_hour(gs) in hours
            and time.get_minute(gs) % 10 == state["minutes"]
        )

    def eff(gs):
        def f1(gs):
            vitals.mod(gs, vitals.MENTAL, -5)
            ui.display("Фонарь резко заморгал. Вы испугались.")

        def f2(gs):
            ui.display("Вы наступили в лужу и простудились.")
            vitals.mod(gs, vitals.FATIGUE, -7)

        def f3(gs):
            ui.display("Вы встретили Ландера. Вам ужасно неловко.")
            stats.mod(gs, stats.SOCIAL, -5)
            vitals.mod(gs, vitals.MENTAL, -5)

        def f4(gs):
            ui.display("Вам всучили брошюрку о вреде алкоголя. Вы и не собирались...")
            stats.mod(gs, stats.KNOWLEDGE, +5)

        def f5(gs):
            ui.display("Вы нашли траву и ПОТРОГАЛИ ее.")
            stats.mod(gs, stats.MENTAL, +15)
            vitals.mod(gs, vitals.FATIGUE, -10)

        def f6(gs):
            ui.display(
                "Собака, гуляющая в парке, украла ваш студак. Пока вы бежали за ней и отнимали его, вы очень устали."
            )
            vitals.mod(gs, vitals.FATIGUE, -5)

        def f7(gs):
            ui.display(
                "Вода в парке очень красиво плещется. Вы засмотрелись на нее, и она убаюкала вас... "
            )
            vitals.mod(gs, vitals.SLEEPINESS, +7)

        def f8(gs):
            ui.display(
                "С вами завел беседу бомж. Вы рассказали ему о своей курсовой. Он расстроился и дал вам 5 рублей."
            )
            stats.mod(gs, stats.MONEY, +5)

        def f9(gs):
            ui.display(
                "Вы увидели уведомление от тгк <<на старой басманной все спокойно>> и обрадовались!"
            )
            vitals.mod(gs, vitals.MENTAL, +5)

        def f10(gs):
            ui.display(
                "Солнце светило ярко, и вы решили поботать на природе... но ветер унес листы из вашего конспекта по дискре!"
            )
            stats.mod(gs, stats.KNOWLEDGE, -10)

        functions = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
        chs = random.choice(functions)
        state.update(init())
        chs(gs)

    def tr1(gs):
        return time.get_minute(gs) % 20 != state["cooldown"]

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, None),
        ]
    )


def random_metro_scenario(state=None):

    hour = (random.randint(0, 23),)
    minute = random.randint(0, 59)

    def tr(gs):
        return (
            location.get_place(gs) == "metro"
            and time.get_hour(gs) == hour
            and time.get_minute == minute
        )

    def eff(gs):
        def f1(gs):
            stats.mod(gs, stats.SOCIAL, -5)
            ui.display("С вами кто-то столкнулся в метро. Ауч.")

        def f2(gs):
            vitals.mod(gs, vitals.MONEY, -5)
            ui.display(
                "Вы забыли карту москвича дома. Хорошо, что можно проехать по деньгам."
            )

        def f3(gs):
            stats.mod(gs, stats.KNOWLEGE, +5)
            ui.display("Вы увидели знак Т1 и порадовались, что знаете, что это.")

        functions = [f1, f2, f3]
        chs = random.choice(functions)
        return chs(gs)

    def tr1(gs):
        return time.get_hour(gs) != hour

    def eff1(gs):
        pass  # Эффекта нет

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, eff1),
        ]
    )


SCENARIOS = [
    random_scenario,
    random_scenario2,
    random_park_day_scenario,
    random_home_scenario,
    random_metro_scenario,
    # random_park_night_scenario,
    random_park_night_scenario2,
]
