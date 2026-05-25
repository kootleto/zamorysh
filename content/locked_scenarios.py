from engine import scenarios_api
from gameplay.api import time, location
from gameplay.api.location import Place, X, Y
from interface import ui

working_hours = {
    Place.SURF_COFFEE: (7, 22),
    Place.ANOTHER_COFFEE: (8, 22),
    Place.CLUB: (22, 4),
    Place.UNIVERSITY: (9, 23),
}


def lock_unlock(place, hours):
    def tr_unlock(gs):
        if hours[0] < hours[1]:
            return hours[0] <= time.get_hour(gs) < hours[1]
        else:
            return hours[0] <= time.get_hour(gs) < 24 or time.get_hour(gs) < hours[1]

    def eff_unlock(gs):
        location.unlock(gs, place, "schedule")

    def tr_lock(gs):
        return not tr_unlock(gs)

    def eff_lock(gs):
        location.lock(gs, place, "schedule")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr_lock, eff_lock),
            scenarios_api.base_transition(1, 0, tr_unlock, eff_unlock),
        ]
    )


def locked_surf_coffee():
    return lock_unlock(Place.SURF_COFFEE, working_hours[Place.SURF_COFFEE])


def locked_another_coffee():
    return lock_unlock(Place.ANOTHER_COFFEE, working_hours[Place.ANOTHER_COFFEE])


def locked_club():
    return lock_unlock(Place.CLUB, working_hours[Place.CLUB])


def locked_university():
    return lock_unlock(Place.UNIVERSITY, working_hours[Place.UNIVERSITY])


def display_locked(place, message):
    def tr_locked(gs):
        return (
            location.get_place_by_coords(location.get(gs, X), location.get(gs, Y))
            == place
            and location.get_place(gs) == Place.OUTSIDE
        )

    def eff_locked():
        ui.display(message)

    def tr_unlocked(gs):
        return not tr_locked(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr_locked, eff_locked),
            scenarios_api.base_transition(1, 0, tr_unlocked, None),
        ]
    )


def display_surf_coffee():
    return display_locked(Place.SURF_COFFEE, "Surf Coffee сейчас закрыт.")


def display_another_coffee():
    return display_locked(Place.ANOTHER_COFFEE, "Другая кофейня сейчас не работает.")


def display_club():
    return display_locked(
        Place.CLUB,
        "Приходите в рабочие часы <<Nightlife>>.",
    )


def display_university():
    return display_locked(Place.UNIVERSITY, "Сейчас в университет не попасть.")


SCENARIOS = [
    locked_surf_coffee,
    locked_another_coffee,
    locked_club,
    locked_university,
    display_surf_coffee,
    display_another_coffee,
    display_club,
    display_university,
]
