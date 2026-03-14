from engine import scenarios_api, gs_api


def sleepiness_scenario():  # будет ли это каждый тик??
    def check():
        return True

    def getting_sleepy(gs):
        return gs_api.mod_vital(gs, "sleepiness", 1)  # 10 в час

    return scenarios_api.base_scenario(
        scenarios_api.base_transition(0, 1, check, getting_sleepy)
    )


def sleep_scenario():
    def check_enough(gs):
        return gs_api.get_vital(gs, "sleeping_time") >= 420  # 7 часов короче

    def enough(gs):
        if gs_api.get_vital(gs, "sleeping_debt") >= 20:
            gs_api.mod_vital(gs, "sleeping_debt", -20)

    def check_little(gs):
        return 240 < gs_api.get_vital(gs, "sleeping_time") < 420

    def little(gs):
        return gs_api.mod_vital(gs, "sleeping_debt", 10)

    def check_very_little(gs):
        return gs_api.get_vital(gs, "sleeping_debt") <= 240

    def very_little(gs):
        return gs_api.mod_vital(gs, "sleeping_debt", 20)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(
                0, 1, check_enough, enough
            ),  # номер состояния??
            scenarios_api.base_transition(1, 2, check_little, little),
            scenarios_api.base_transition(2, 3, check_very_little, very_little),
        ]
    )
