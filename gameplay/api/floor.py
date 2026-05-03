from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "floors"

FLOOR = "floor"

_INITIAl = {FLOOR: 1}


def _resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        _DOMAIN,
        set_fn=min,
        mod_fn=sum,
        clamp_fn=lambda v: max(1, min(5, v)),
    )


def get(gs):
    return gs_api.get_value(gs, _DOMAIN, FLOOR)


def set(gs, value):
    return gs_api.set_value(gs, _DOMAIN, FLOOR, value)


def mod(gs, delta):
    return gs_api.mod_value(gs, _DOMAIN, FLOOR, delta)


CLASSROOMS = {2: [205], 3: [316], 4: [401], 5: [501, 502, 505, 506, 507, 509, 511, 516]}
