from engine import activities_api, gs_api
from interface import ui


def set_alarm(time):  # игрок должен ввести время будильника
    time = ui.prompt("Установите время:")

    def tick_effect(gs):
        gs_api.set_timer(gs, "alarm", time)

    return activities_api.base_activity(tick_effect, name="set_alarm")


def sleep():

    def tick_effect(gs):
        gs_api.mod_vital(gs, "sleepiness", -2)  # 20 каждый час
        gs_api.mod_vital(gs, "current_sleeping_time", 1)  # посчитать количество тиков

    def can_continue(gs):
        return (
            gs_api.get_time(gs) < gs_api.get_timer(gs, "alarm")
            and gs_api.get_vital(gs, "sleepiness") > 0
        )

    return activities_api.base_activity(tick_effect, can_continue, name="sleep")


def get_up():
    def tick_effect(gs):
        gs_api.mod_vital(
            gs, "sleeping_time", gs_api.get_vital(gs, "current_sleeping_time")
        )
        gs_api.mod_vital(
            gs, "current_sleeping_time", -gs_api.get_vital(gs, "current_sleeping time")
        )  # либо поменять значение sleeping_time на 0

    def can_continue(gs):
        return (
            gs_api.get_vital(gs, "current_sleeping_time") > 0
        )  # хочется чтобы запускалось только после сна...

    return activities_api.base_activity(tick_effect, can_continue, name="get_up")
