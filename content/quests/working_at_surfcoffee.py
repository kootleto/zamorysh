import datetime
import random

from engine import activities_api, scenarios_api, gs_api, data_api
from gameplay.api import stats, vitals, location, time, quests
from interface import ui


@activities_api.system_only
def work():

    def tick_effect(gs):
        gs_api.multiply_next_tick_interval(gs, 0.01)
        stats.mod(gs, stats.MONEY, 0.5)
        vitals.mod(gs, vitals.FATIGUE, 0.5)
        stats.mod(gs, stats.SOCIAL, 0.5)

    def can_continue(gs):
        return (
            location.get_place(gs) == location.Place.SURF_COFFEE
            and 20 <= time.get_hour(gs) < 22
            and quests.is_active(gs, "surf_coffee")
        )

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required=False, name="работать"
    )


def coffee_quest(activity_definitions, state=None):
    state = data_api.init_defaults(state, working_days=0)

    def proposal_trigger(gs):
        return (
            time.get_day(gs) == time.START_DATETIME.day + 2
            and location.get_place(gs) == location.Place.SURF_COFFEE
        )

    def proposal(gs):
        quests.set_status(gs, "surf_coffee", quests.Status.ACTIVE)
        ui.display(
            "Вы видите объявление на кассе:\n«Нам срочно нужен бариста на вечерние смены."
            "\nТвоя задача - обслуживать покупателей с 20:00 до 22:00 три дня подряд."
            "\nОплата - 60 кредитов за смену."
            "\nЕсли тебя заинтересовало предложение, приходи завтра к 19:50, обучим всему на месте."
            "\nЖдём тебя!»"
        )

    def check_start(gs):
        return (
            time.get_day(gs) == time.START_DATETIME.day + 3
            and location.get_place(gs) == location.Place.SURF_COFFEE
            and time.get_time(gs) == datetime.time(19, 50)
        )

    def start():
        ui.display(
            f"Вы видите шеф-баристу, {random.choice(["она", "он"])} замечает ваш взгляд и подходит к вам."
            "\n-- Привет! Ты на подработку? Сейчас я покажу тебе всё, а начнём в 20:00."
        )

    def check_working(gs):
        return location.get_place(gs) == location.Place.SURF_COFFEE and time.get_time(
            gs
        ) == datetime.time(20, 0)

    def start_working(gs):
        activities_api.start_activity_by_definition(gs, activity_definitions, work)

    def check_absence(gs):
        return location.get_place(gs) != location.Place.SURF_COFFEE and time.get_time(
            gs
        ) == datetime.time(20, 0)

    def fire(gs):
        ui.display(
            "Вам приходит сообщение от шеф-баристы: «Тебя нет на рабочем месте, так что нам придётся тебя "
            "уволить :( Всё равно будем ждать тебя в нашей кофейне как клиента!»"
        )
        vitals.mod(gs, vitals.MENTAL, -20)
        quests.finish(gs, "surf_coffee")

    def check_finish_day(gs):
        return time.get_time(gs) == datetime.time(22, 0)

    def finish_day():
        state["working_days"] += 1
        ui.display("Смена закончилась! Можно идти домой.")

    def seeing_friend(gs):
        return (
            location.get_place(gs) == location.Place.SURF_COFFEE
            and time.get_hour(gs) < 20
            and random.randint(0, 4) == 0
        )

    def greeting_friend(gs):
        gender = random.choice(["woman", "man"])
        if gender == "woman":
            your = "вашу"
            pronoun = "она"
        else:
            your = "вашего"
            pronoun = "он"
        ui.display(
            f"Вы видите {your} коллегу за кассой, {pronoun} улыбается и машет вам. "
            f"Теплота и радость наполняют ваше сердце. Вы тоже улыбаетесь."
        )
        vitals.mod(gs, vitals.MENTAL, 10)
        stats.mod(gs, stats.SOCIAL, 5)

    def check_finish():
        return state["working_days"] == 3

    def finish(gs):
        ui.display("К вам обращается шеф-бариста:")
        ui.display(
            "-- Спасибо тебе большое за помощь! Без тебя наша кофейня бы закрылась. "
            "Будем рады видеть тебя снова! Не только на смене, конечно."
        )
        ui.display("Вы довольны, что помогли любимой кофейне.")
        vitals.mod(gs, vitals.MENTAL, 10)
        quests.finish(gs, "surf_coffee")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, "proposal", proposal_trigger, proposal),
            scenarios_api.base_transition("proposal", "hired", check_start, start),
            scenarios_api.base_transition(
                "hired", "working", check_working, start_working
            ),
            scenarios_api.base_transition(
                "working", "hired", check_finish_day, finish_day
            ),
            scenarios_api.base_transition("hired", "fired", check_absence, fire),
            scenarios_api.base_transition(
                "hired", "hired", seeing_friend, greeting_friend
            ),
            scenarios_api.base_transition("hired", "fired", check_finish, finish),
        ]
    )


ACTIVITIES = [work]
SCENARIOS = [coffee_quest]
