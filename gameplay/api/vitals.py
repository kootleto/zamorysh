from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "vitals"

FATIGUE = "fatigue"
SLEEPINESS = "sleepiness"
MENTAL = "mental"

_INITIAL = {
    FATIGUE: 0,
    SLEEPINESS: 0,
    MENTAL: 100,
}


def _resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        _DOMAIN,
        set_fn=max,  # Обычно для игрока чем выше, тем хуже
        mod_fn=sum,
        clamp_fn=lambda v: max(
            0, min(100, v)
        ),  # vitals ограничены значениями от 0 до 100
    )


def get(gs, vital):
    return gs_api.get_value(gs, _DOMAIN, vital)


def set(gs, vital, value):
    gs_api.set_value(gs, _DOMAIN, vital, value)


def mod(gs, vital, delta):
    gs_api.mod_value(gs, _DOMAIN, vital, delta)
