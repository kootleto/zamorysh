from content import schedule
from engine import activities_api
from gameplay.api import time


def check_today_schedule():
    def tick_effect(gs):
        return schedule.get_day_schedule(time.get_weekday(gs), gs)

    def can_continue(gs):
        return time.get_weekday(gs) != 6

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required=True,
        name="посмотреть расписание на сегодня",
    )


def check_tomorrow_schedule():
    def tick_effect(gs):
        return schedule.get_day_schedule(time.get_weekday(gs) + 1, gs)

    def can_continue(gs):
        return time.get_weekday(gs) != 5

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required=True,
        name="посмотреть расписание на завтра",
    )
