from engine import scenarios_api
from gameplay.api import time, stats


def money_getting():
    def check(gs):
        hour = time.get_hour(gs)
        minute = time.get_minute(gs)
        return hour == 6 and minute == 0

    def great_day(gs):
        stats.mod(gs, stats.MONEY, +5)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, check, great_day)]
    )


SCENARIOS = [money_getting]
