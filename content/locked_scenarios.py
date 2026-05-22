from engine import scenarios_api
from gameplay.api import time, location
from gameplay.api.location import Place
from interface import ui


def lock_surf_coffee():
    def tr_l(gs):
        return (
            time.get_hour(gs) in [0, 1, 2, 3, 4, 5, 6, 22, 23]
            and location.get_place(gs) == "surf_coffee"
        )

    def eff_l(gs):
        location.lock(gs, Place.SURF_COFFEE)
        ui.display("Surf coffee закрыт")

    def tr_u(gs):
        return time.get_hour(gs) not in [0, 1, 2, 3, 4, 5, 6, 22, 23]

    def eff_u(gs):
        location.unlock(gs, Place.SURF_COFFEE)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr_l, eff_l),
            scenarios_api.base_transition(1, 0, tr_u, eff_u),
        ]
    )
