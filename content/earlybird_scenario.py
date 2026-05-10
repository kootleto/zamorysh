from engine import scenarios_api, state_api
from gameplay.api import location, time, vitals
from interface import ui
import random


def earlybird_scenario(
    state=None,
):

    def tr(gs):
        return (
            location.get_place(gs) == "Surf coffee"
            and time.get_hour(gs) == 7
            and time.get_minute(gs) == 0
        )

    def eff(gs):
        if random.choice([True, False]):
            vitals.mod(gs, vitals.MENTAL, -2)
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            ui.display("You came first and got free coffee. Yay.")
        else:
            vitals.mod(gs, vitals.FATIGUE, +2)
            ui.display(
                "No luck today! Someone has already gotten your free coffee. (At least you're not gonna be late.)"
            )

    def tr1(gs):
        return time.get_hour(gs) != 7

    def eff1(gs):
        pass  # Эффекта нет

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, eff1),
        ]
    )


SCENARIOS = [earlybird_scenario]
