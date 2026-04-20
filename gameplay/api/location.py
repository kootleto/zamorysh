from collections import defaultdict

from engine import gs_api, resolver_api

domain = "location"

x = "xcoordinate"
y = "ycoordinate"

NORTH_BORDER = 5
SOUTH_BORDER = 0
EAST_BORDER = 60
WEST_BORDER = 0

initial = {
    x: 0,
    y: 0,
}


def get(gs, coordinate):
    return gs_api.get_value(gs, domain, coordinate)


def set(gs, coordinate, value):
    gs_api.set_value(gs, domain, coordinate, value)


def mod(gs, coordinate, delta):
    gs_api.mod_value(gs, domain, coordinate, delta)


def get_directions(gs):
    directions = []
    if get(gs, x) < EAST_BORDER:
        directions.append("east")
    if get(gs, x) > WEST_BORDER:
        directions.append("west")
    if get(gs, y) < NORTH_BORDER:
        directions.append("north")
    if get(gs, y) > SOUTH_BORDER:
        directions.append("south")
    return directions


def check_home(gs):
    return get(gs, x) == 0 and get(gs, y) == 0


def check_metro(gs):
    return 10 < get(gs, y) < 40


def check_park(gs):
    return get(gs, x) == 5 and get(gs, y) == 0


def check_coffee(gs):
    return get(gs, x) == 5 and (get(gs, y) == 10 or get(gs, y) == 60)


def check_club(gs):
    return get(gs, x) == 5 and get(gs, y) == 40


def check_university(gs):
    return get(gs, x) == 0 and get(gs, y) == 60


places = {
    "home": check_home,
    "metro": check_metro,
    "park": check_park,
    "coffee_house": check_coffee,
    "club": check_club,
    "university": check_university,
}


def get_place(gs):
    for place, check_coordinate in places.items():
        if check_coordinate(gs):
            return place
    return "outside"


def resolve(gs, intents):
    grouped_intents = defaultdict(list)
    for intent in intents:
        grouped_intents[intent["target"]].append(intent)
    resolver_api.resolve_generic(
        gs,
        grouped_intents[x],
        domain,
        clamp_fn=lambda v: max(WEST_BORDER, min(EAST_BORDER, v)),
    )
    resolver_api.resolve_generic(
        gs,
        grouped_intents[y],
        domain,
        clamp_fn=lambda v: max(SOUTH_BORDER, min(NORTH_BORDER, v)),
    )
