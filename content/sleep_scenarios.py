from content import sleep_activities
from engine import scenarios_api, activities_api
from gameplay.api import vitals
from interface import ui


def falling_asleep(activity_definitions):
    def check_sleepy(gs):
        return vitals.get(gs, vitals.SLEEPINESS) >= 80

    def go_to_sleep():
        ui.display("Вам пора бы лечь спать...")

    def check_very_sleepy(gs):
        return vitals.get(gs, vitals.SLEEPINESS) == 100

    def auto_sleep(gs):
        activities_api.start_activity_by_definition(
            gs, activity_definitions, sleep_activities.auto_sleep
        )

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_sleepy, go_to_sleep),
            scenarios_api.base_transition(1, 0, lambda gs: not check_sleepy(gs), None),
            scenarios_api.base_transition(1, 2, check_very_sleepy, auto_sleep),
            scenarios_api.base_transition(
                2, 1, lambda gs: not check_very_sleepy(gs), None
            ),
        ]
    )


SCENARIOS = [falling_asleep]
