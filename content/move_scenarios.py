from engine import scenarios_api
from gameplay.api import location
from interface import ui


def home_scenario():
    def check_home(gs):
        return location.get_place(gs) == "home"

    def enter():
        ui.display("You are entering home!")

    def exit():
        ui.display("You are exiting home!")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, "in", check_home, lambda: None),
            scenarios_api.base_transition(
                0, "out", lambda gs: not check_home, lambda: None
            ),
            scenarios_api.base_transition("out", "in", check_home, enter),
            scenarios_api.base_transition(
                "in", "out", lambda gs: not check_home(gs), exit
            ),
        ]
    )


scenarios = [home_scenario]
