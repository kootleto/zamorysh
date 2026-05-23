import random

from engine import data_api
from engine import scenarios_api, gs_api
from gameplay.api import vitals
from interface import ui


def random_scenario(state=None):
    def check_tick():
        return {"tick": random.randint(1, 3)}

    state = data_api.init_fn(state, check_tick)

    def ti(gs):
        return gs_api.get_time(gs) == state["tick"]

    def eff(gs):
        vitals.mod(gs, vitals.FATIGUE, +5)
        ui.display("Вы РАНДОМНО устали")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, ti, eff),
        ]
    )


SCENARIOS = [random_scenario]
