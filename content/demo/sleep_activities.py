from engine import activities_api, gs_api
from gameplay.activity_wrappers import single_tick_activity
from gameplay.api import timers, vitals
from interface import ui


def set_alarm(state=None):  # игрок должен ввести время будильника

    async def tick_effect(gs):
        time = int(await ui.prompt("Установите время: "))
        timers.set(gs, "alarm", time)

    return single_tick_activity(
        activities_api.base_activity(tick_effect, hold_required=True, name="set_alarm"),
        state,
    )


def sleep():

    def tick_effect(gs):
        vitals.mod(gs, vitals.SLEEPINESS, -2)  # 20 каждый час
        gs_api.multiply_next_tick_interval(gs, 0.01)

    def can_continue(gs):
        return (
            gs_api.get_time(gs) < timers.get(gs, "alarm")
            and vitals.get(gs, vitals.SLEEPINESS) > 0
        )

    return activities_api.base_activity(tick_effect, can_continue, name="sleep")


ACTIVITIES = [set_alarm, sleep]
