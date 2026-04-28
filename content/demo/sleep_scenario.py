from engine import scenarios_api
from gameplay.api import vitals


def sleepiness_scenario():
    def check():
        return True

    def getting_sleepy(gs):
        return vitals.mod(gs, vitals.SLEEPINESS, 1)  # 10 в час

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, check, getting_sleepy)]
    )


# SCENARIOS = [sleepiness_scenario]
# Строчка закомментирована, потому что у нас теперь есть фоновая активность get_tired
