from collections import defaultdict

from engine import gs_api, resolver_api

_DOMAIN = "location"

X = "xcoordinate"
Y = "ycoordinate"

NORTH_BORDER = 5
SOUTH_BORDER = 0
EAST_BORDER = 60
WEST_BORDER = 0

_INITIAL = {
    X: 0,
    Y: 0,
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
        directions.append("east")
    if get(gs, X) > WEST_BORDER:
        directions.append("west")
    if get(gs, Y) < NORTH_BORDER:
        directions.append("north")
    if get(gs, Y) > SOUTH_BORDER:
        directions.append("south")
    return directions


places = {
    "home": lambda gs: get(gs, Y) == 0 and get(gs, X) == 0,
    "metro": lambda gs: 10 < get(gs, X) < 40,
    "park": lambda gs: get(gs, Y) == 5 and get(gs, X) == 0,
    "coffee house": lambda gs: get(gs, Y) == 5
    and (get(gs, X) == 10 or get(gs, X) == 60),
    "club": lambda gs: get(gs, Y) == 5 and get(gs, X) == 40,
    "university": lambda gs: get(gs, Y) == 0 and get(gs, X) == 60,
}


def get_place(gs):
    for place, check_coordinate in places.items():
        if check_coordinate(gs):
            return place
    return "outside"


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
