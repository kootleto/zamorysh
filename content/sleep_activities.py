from engine import gs_api, activities_api
from gameplay.activity_wrappers import single_tick_activity
from gameplay.api import vitals, timers
from interface import ui


def sleep():

    def tick_effect(gs):
        vitals.mod(gs, vitals.SLEEPINESS, -0.255)
        gs_api.multiply_next_tick_interval(gs, 0.01)

    def can_continue(gs):
        return (
            gs_api.get_time(gs) != timers.get(gs, "alarm")
            and vitals.get(gs, vitals.SLEEPINESS) > 0
        )

    return activities_api.base_activity(tick_effect, can_continue, name="лечь спать")


def set_alarm(state=None):
    async def tick_effect(gs):
        time = int(await ui.prompt("Установите время: "))
        timers.set(gs, "alarm", time)

    return single_tick_activity(
        activities_api.base_activity(tick_effect, name="поставить будильник"),
        state,
    )


def get_sleepy():
    def tick_effect(gs):
        vitals.mod(gs, vitals.SLEEPINESS, 0.085)

    return activities_api.base_activity(
        tick_effect, True, is_stackable=True, is_background=True
    )


ACTIVITIES = [sleep, set_alarm, get_sleepy]
