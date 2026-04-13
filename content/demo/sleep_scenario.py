from engine import scenarios_api, gs_api


def sleepiness_scenario():
    def check():
        return True

    def getting_sleepy(gs):
        return gs_api.mod_vital(gs, "sleepiness", 1)  # 10 в час

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, check, getting_sleepy)]
    )


# scenarios = [sleepiness_scenario]
# Строчка закомментирована, потому что у нас теперь есть фоновая активность get_tired
