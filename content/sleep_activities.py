from datetime import datetime, timedelta

from engine import gs_api, activities_api
from gameplay.activity_wrappers import single_tick_activity
from gameplay.api import vitals, timers, time
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
        input_time = list(map(int, (await ui.prompt("Установите время")).split(":")))
        dt = datetime(
            year=time.get_year(gs),
            month=time.get_month(gs),
            day=time.get_day(gs),
            hour=input_time[0],
            minute=input_time[1],
        )
        if dt >= time.get_datetime(gs):
            timers.set(gs, "alarm", time.datetime_to_tick(dt))
        else:
            dt += timedelta(days=1)
            timers.set(gs, "alarm", time.datetime_to_tick(dt))

    return single_tick_activity(
        activities_api.base_activity(tick_effect, name="поставить будильник"),
        state,
    )


@activities_api.with_auto_start
def get_sleepy():
    def tick_effect(gs):
        vitals.mod(gs, vitals.SLEEPINESS, 0.085)

    return activities_api.base_activity(
        tick_effect, True, is_stackable=True, is_background=True
    )


ACTIVITIES = [sleep, set_alarm, get_sleepy]
