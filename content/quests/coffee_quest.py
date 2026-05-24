import datetime
import random

from engine import activities_api, scenarios_api, gs_api
from gameplay.api import stats, vitals, location, time
from interface import ui


def work(activity_definitions):

    def tick_effect(gs):
        gs_api.multiply_next_tick_interval(gs, 0.01)
        stats.mod(gs, stats.MONEY, 0.5)
        vitals.mod(gs, vitals.FATIGUE, 0.5)
        stats.mod(gs, stats.SOCIAL, 0.5)

    def can_continue(gs):
        return (
            location.get_place(gs) == location.Place.SURF_COFFEE
            and 20 <= time.get_hour(gs) < 22
        )

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required=False, name="работать"
    )


def coffee_quest():
    def proposal_trigger(gs):
        return (
            time.get_day(gs) == time.START_DATETIME.day + 2
            and location.get_place(gs) == location.Place.SURF_COFFEE
        )

    def proposal():
        ui.display(
            "Вы видите объявление на кассе:\n'Нам срочно нужен бариста на вечерние смены."
            "\nТвоя задача - обслуживать покупателей с 20:00 до 22:00 три дня подряд."
            "\nОплата - 60 кредитов за смену."
            "\nЕсли тебя заинтересовало предложение, приходи завтра к 19:50, обучим всему на месте."
            "\nЖдём тебя!'"
        )

    def check_start(gs):
        return (
            time.get_day(gs) == time.START_DATETIME.day + 2
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

    def finish_day():
        ui.display("Смена закончилась! Можно идти домой.")

    def seeing_friend(gs):
        return (
            location.get_place(gs) == location.Place.SURF_COFFEE
            and time.get_hour(gs) < 20
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
            f"Вы видите {your} коллегу за кассой, {pronoun} улыбается и машет вам. Теплота и радость наполняют ваше сердце. Вы тоже улыбаетесь."
        )
        vitals.mod(gs, vitals.MENTAL, 10)
        stats.mod(gs, stats.SOCIAL, 5)

    def finish(gs):
        ui.display("К вам обращается шеф-бариста:")
        ui.display(
            "-- Спасибо тебе большое за помощь! Без тебя наша кофейня бы закрылась. "
            "Будем рады видеть тебя снова! Не только на смене, конечно."
        )
        ui.display("Вы довольны, что помогли любимой кофейне.")
        vitals.mod(gs, vitals.MENTAL, 10)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, proposal_trigger, proposal),
            scenarios_api.base_transition(1, 2, check_start, start),
            scenarios_api.base_transition(2, 3, check_working, start_working),
            scenarios_api.base_transition(3, 4, True, finish_day),
            scenarios_api.base_transition(4, 5, check_working, start_working),
            scenarios_api.base_transition(5, 6, True, finish_day),
            scenarios_api.base_transition(6, 7, check_working, start_working),
            scenarios_api.base_transition(4, 4, seeing_friend, greeting_friend),
            scenarios_api.base_transition(6, 6, seeing_friend, greeting_friend),
            scenarios_api.base_transition(7, 8, True, finish),
        ]
    )
