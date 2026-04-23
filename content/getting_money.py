from engine import scenarios_api
from gameplay.api import time, stats

def money_getting():
    def weekday_check(gs):
        weekday = time.get_weekday(gs)
        return weekday == 0

    def great_day(gs):
        stats.mod(gs, stats.money, +50)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, weekday_check, great_day)]
    )


scenarios = [money_getting]
