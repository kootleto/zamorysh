from datetime import datetime, timedelta
from engine import gs_api

start_datetime = datetime(2026, 9, 1, 0, 0, 0, 0)


def _get_datetime(gs):
    return start_datetime + timedelta(minutes=gs_api.get_time(gs))


def get_year(gs):
    return _get_datetime(gs).year


def get_month(gs):
    return _get_datetime(gs).month


def get_day(gs):
    return _get_datetime(gs).day


def get_hour(gs):
    return _get_datetime(gs).hour


def get_minute(gs):
    return _get_datetime(gs).minute


def get_weekday(gs):
    return _get_datetime(gs).weekday


def datetime_to_tick(sceduled_time, gs):
    return (
        sceduled_time - _get_datetime(gs)
    ) * 1440  # некрасиво, а как ещё? дельта в днях считается
