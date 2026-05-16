from engine import gs_api
from engine.resolver_api import resolve_generic
from gameplay.api.schedule import Subject

_DOMAIN = "stats"

MONEY = "money"
SOCIAL = "social"

_INITIAL = {
    MONEY: 0,
    SOCIAL: 0,
    Subject.ENGLISH: 0,
    Subject.DIVERSITY: 0,
    Subject.LATIN: 0,
    Subject.LANGUAGE: 0,
    Subject.MATH: 0,
    Subject.OCS: 0,
    Subject.INTRO: 0,
    Subject.LINGDATA: 0,
    Subject.DIGLIT: 0,
    Subject.ELECTIVE: 0,
    Subject.HISTORY: 0,
}


def _resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        _DOMAIN,
        set_fn=min,  # Обычно для игрока чем ниже, тем хуже
        mod_fn=sum,
        clamp_fn=lambda v: max(0, v),
    )


def get(gs, stat):
    return gs_api.get_value(gs, _DOMAIN, stat)


def set(gs, stat, value):
    gs_api.set_value(gs, _DOMAIN, stat, value)


def mod(gs, stat, delta):
    gs_api.mod_value(gs, _DOMAIN, stat, delta)
