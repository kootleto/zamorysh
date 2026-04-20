from engine import gs_api
from collections import defaultdict
from typing import Callable, Iterable, Any
from engine.schema import GameState, Intent, Resolver
from tools.logger import log

domain = "location"

x = "xcoordinate"
y = "ycoordinate"
# coordinates = (xcoordinate, ycoordinate)
place = ""


initial = {
    x: 0,
    y: 0,
}


def resolve_intents(
    gs: GameState,
    intents: Iterable[Intent],
    domain: str,
    set_fn: Callable[[Iterable[Any]], Any] = max,
    mod_fn: Callable[[Iterable[Any]], Any] = sum,
    clamp_fn: Callable = lambda x: x,
):
    grouped_intents = defaultdict(lambda: {"set": [], "mod": []})
    for intent in intents:
        grouped_intents[intent["target"]][intent["op"]].append(intent)
    for target, grouped in grouped_intents.items():
        if grouped["set"]:
            value = set_fn([i["value"] for i in grouped["set"]])
        else:
            value = gs["gameplay"][domain][target]
        value += mod_fn([i["value"] for i in grouped["mod"]])
        if


def get(gs, coordinate):
    return gs_api.get_value(gs, domain, coordinate)


def set(gs, coordinate, value):
    gs_api.set_value(gs, domain, coordinate, value)


def mod(gs, coordinate, delta):
    gs_api.mod_value(gs, domain, coordinate, delta)


def get_directions(gs):
    directions = []
    if get(gs, x) < 60:
        directions.append("east")
    if get(gs, x) > 0:
        directions.append("west")
    if get(gs, y) < 5:
        directions.append("north")
    if get(gs, y) > 0:
        directions.append("south")
    return directions


def get_place(gs):
    if get(gs, x) == 0 and get(gs, y) == 0:
        mod(gs, place, "home")
    elif 0 <= get(gs, x) < 11 and get(gs, y) == 5:
        mod(gs, place, "park")
    elif 10 < get(gs, x) < 40:
        mod(gs, place, "metro")
    elif get(gs, x) == 60 and get(gs, y) == 0:
        mod(gs, place, "university")
    elif (get(gs, x) == 10 or get(gs, x) == 60) and get(
        gs, y
    ) == 5:
        mod(gs, place, "coffee house")
    elif get(gs, x) == 40 and get(gs, y) == 5:
        mod(gs, place, "club")
    else:
        mod(gs, place, "outside")
    return place
