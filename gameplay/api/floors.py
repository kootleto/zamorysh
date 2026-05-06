from collections import defaultdict

from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "floors"

FLOOR = "floor"
CLASSROOM = "classroom"

_INITIAl = {FLOOR: 1, CLASSROOM: None}
CLASSROOMS = {
    0: ["дизайнеры"],
    2: [205],
    3: [316],
    4: [401],
    5: [501, 502, 505, 506, 507, 509, 511, 516],
}


def _resolve(gs, intents):
    grouped_intents = defaultdict(list)
    for intent in intents:
        grouped_intents[intent["target"]].append(intent)
    resolve_generic(
        gs,
        grouped_intents[FLOOR],
        _DOMAIN,
        clamp_fn=lambda v: max(0, min(5, v)),
    )
    resolve_generic(
        gs,
        grouped_intents[CLASSROOM],
        _DOMAIN,
    )


def get(gs, loc):
    return gs_api.get_value(gs, _DOMAIN, loc)


def set(gs, loc, value):
    return gs_api.set_value(gs, _DOMAIN, loc, value)


def mod_floor(gs, delta):
    return gs_api.mod_value(gs, _DOMAIN, FLOOR, delta)
