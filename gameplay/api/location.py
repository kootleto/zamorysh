from collections import defaultdict
from enum import StrEnum

from engine import gs_api, resolver_api

_DOMAIN = "location"

X = "xcoordinate"
Y = "ycoordinate"

NORTH_BORDER = 5
SOUTH_BORDER = 0
EAST_BORDER = 60
WEST_BORDER = 0


class Place(StrEnum):
    HOME = "home"
    METRO = "metro"
    PARK = "park"
    SURF_COFFEE = "surf_coffee"
    ANOTHER_COFFEE = "another_coffee"
    CLUB = "club"
    UNIVERSITY = "university"
    OUTSIDE = "outside"


_INITIAL = {
    X: 0,
    Y: 0,
    "locked": {
        Place.HOME: False,
        Place.METRO: False,
        Place.PARK: False,
        Place.SURF_COFFEE: False,
        Place.ANOTHER_COFFEE: False,
        Place.CLUB: False,
        Place.UNIVERSITY: False,
        Place.OUTSIDE: False,
    },
}


def get(gs, coordinate):
    return gs_api.get_value(gs, _DOMAIN, coordinate)


def set(gs, coordinate, value):
    gs_api.set_value(gs, _DOMAIN, coordinate, value)


def mod(gs, coordinate, delta):
    gs_api.mod_value(gs, _DOMAIN, coordinate, delta)


def get_directions(gs):
    directions = []
    if get(gs, X) < EAST_BORDER:
        directions.append("восток")
    if get(gs, X) > WEST_BORDER:
        directions.append("запад")
    if get(gs, Y) < NORTH_BORDER:
        directions.append("север")
    if get(gs, Y) > SOUTH_BORDER:
        directions.append("юг")
    return directions


places = {
    Place.HOME: lambda x, y: y == 0 and x == 0,
    Place.METRO: lambda x, y: 10 < x < 40,
    Place.PARK: lambda x, y: y == 5 and x == 0,
    Place.SURF_COFFEE: lambda x, y: y == 5 and x == 10,
    Place.ANOTHER_COFFEE: lambda x, y: y == 5 and x == 60,
    Place.CLUB: lambda x, y: y == 5 and x == 40,
    Place.UNIVERSITY: lambda x, y: y == 0 and x == 60,
}


def lock(gs, place: Place):
    gs_api.set_value(gs, _DOMAIN, place, True)


def unlock(gs, place: Place):
    gs_api.set_value(gs, _DOMAIN, place, False)


def get_locked_places(gs):
    return gs_api.get_value(gs, _DOMAIN, "locked")


def check_locked(gs, place: Place):
    return get_locked_places(gs)[place]


def get_place_by_coords(x, y):
    for place, check_coordinate in places.items():
        if check_coordinate(x, y):
            return place
    return Place.OUTSIDE


def get_place(gs):
    place = get_place_by_coords(get(gs, X), get(gs, Y))
    if not check_locked(gs, place):
        return place
    else:
        return Place.OUTSIDE


def _resolve(gs, intents):
    grouped_intents = defaultdict(list)
    for intent in intents:
        grouped_intents[intent["target"]].append(intent)
    resolver_api.resolve_generic(
        gs,
        grouped_intents[X],
        _DOMAIN,
        clamp_fn=lambda v: max(WEST_BORDER, min(EAST_BORDER, v)),
    )
    resolver_api.resolve_generic(
        gs,
        grouped_intents[Y],
        _DOMAIN,
        clamp_fn=lambda v: max(SOUTH_BORDER, min(NORTH_BORDER, v)),
    )

    def apply_fn(gs, _domain, target, value):
        get_locked_places(gs)[target] = value

    for place in Place:
        resolver_api.resolve_generic(
            gs,
            grouped_intents[place],
            _DOMAIN,
            get_fn=lambda gs, _domain, target: check_locked(gs, Place(target)),
            apply_fn=apply_fn,
            set_fn=any,
        )
