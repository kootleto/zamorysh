from datetime import datetime

from engine import gs_api, activities_api, data_api
from gameplay.api import time


def wait():
    def tick_effect(gs):
        gs_api.multiply_next_tick_interval(gs, 0.01)

    return activities_api.base_activity(
        tick_effect, hold_required=True, name="подождать"
    )


@activities_api.system_only
def wait_until(params):
    until_hour = data_api.get_params(params, "hour")
    until_minute = data_api.get_params(params, "minute")

    def tick_effect(gs):
        gs_api.multiply_next_tick_interval(gs, 0.01)

    def can_continue(gs):
        until_time = datetime(
            year=time.get_year(gs),
            month=time.get_month(gs),
            day=time.get_day(gs),
            hour=until_hour,
            minute=until_minute,
        )
        return gs_api.get_time(gs) < time.datetime_to_tick(until_time)

    return activities_api.base_activity(tick_effect, can_continue, hold_required=False)


ACTIVITIES = [wait, wait_until]
