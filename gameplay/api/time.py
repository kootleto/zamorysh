from datetime import datetime, timedelta
from enum import IntEnum

from engine import gs_api

START_DATETIME = datetime(2026, 9, 1, 7, 30, 0, 0)


class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def get_datetime(gs):
    return START_DATETIME + timedelta(minutes=gs_api.get_time(gs))


def get_year(gs):
    return get_datetime(gs).year


def get_month(gs):
    return get_datetime(gs).month


def get_day(gs):
    return get_datetime(gs).day


def get_hour(gs):
    return get_datetime(gs).hour


def get_minute(gs):
    return get_datetime(gs).minute


def get_weekday(gs):
    return Weekday(get_datetime(gs).weekday())


def get_time(gs):
    return get_datetime(gs).time()


def datetime_to_tick(dt):
    return int((dt - START_DATETIME).total_seconds() / 60)
