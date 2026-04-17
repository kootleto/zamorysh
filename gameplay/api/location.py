from engine import gs_api
from engine.resolver_api import resolve_generic

domain = "location"

xcoordinate = "xcoordinate"
ycoordinate = "ycoordinate"
# coordinates = (xcoordinate, ycoordinate)
place = ""


initial = {
    xcoordinate: 0,
    ycoordinate: 0,
}


def resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        domain,
        set_fn=max,  # ???
        mod_fn=sum,
        clamp_fn=lambda v: max(
            0, min(100, v)
        ),  # а мне надо х от 0 до 60, а у от 0 до 5
    )


def get(gs, coordinate):
    return gs_api.get_value(gs, domain, coordinate)


def set(gs, coordinate, value):
    gs_api.set_value(gs, domain, coordinate, value)


def mod(gs, coordinate, delta):
    gs_api.mod_value(gs, domain, coordinate, delta)


def get_directions(gs):
    directions = []
    if get(gs, xcoordinate) < 60:
        directions.append("east")
    if get(gs, xcoordinate) > 0:
        directions.append("west")
    if get(gs, ycoordinate) < 5:
        directions.append("north")
    if get(gs, ycoordinate) > 0:
        directions.append("south")
    return directions


def get_place(gs):
    if get(gs, xcoordinate) == 0 and get(gs, ycoordinate) == 0:
        mod(gs, place, "home")
    elif 0 <= get(gs, xcoordinate) < 11 and get(gs, ycoordinate) == 5:
        mod(gs, place, "park")
    elif 10 < get(gs, xcoordinate) < 40:
        mod(gs, place, "metro")
    elif get(gs, xcoordinate) == 60 and get(gs, ycoordinate) == 0:
        mod(gs, place, "university")
    elif (get(gs, xcoordinate) == 10 or get(gs, xcoordinate) == 60) and get(
        gs, ycoordinate
    ) == 5:
        mod(gs, place, "coffee house")
    elif get(gs, xcoordinate) == 40 and get(gs, ycoordinate) == 5:
        mod(gs, place, "club")
    else:
        mod(gs, place, "outside")
    return place
