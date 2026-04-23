from engine import scenarios_api, gs_api
from gameplay import time_api


def money_getting():
    def weekday_check():
        weekday = time_api.get_weekday(time_api)
        return weekday == 0

    def great_day(gs):
        return gs_api.mod_stat(gs, "money", +50)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, weekday_check, great_day)]
    )


scenarios = [money_getting]
