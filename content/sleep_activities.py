from engine import activities_api, gs_api
from interface import ui


def set_alarm():  # игрок должен ввести время будильника

    def tick_effect(gs):
        time = int(ui.prompt("Установите время: "))
        gs_api.set_timer(gs, "alarm", time)

    return activities_api.base_activity(
        tick_effect, hold_required=True, name="set_alarm"
    )


def sleep():

    def tick_effect(gs):
        gs_api.mod_vital(gs, "sleepiness", -2)  # 20 каждый час

    def can_continue(gs):
        return (
            gs_api.get_time(gs) < gs_api.get_timer(gs, "alarm")
            and gs_api.get_vital(gs, "sleepiness") > 0
        )

    return activities_api.base_activity(tick_effect, can_continue, name="sleep")


activities = [set_alarm, sleep]
