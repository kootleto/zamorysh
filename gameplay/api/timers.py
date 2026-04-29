from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "timers"

ALARM = "alarm"

_INITIAL = {
    ALARM: 0,
}


def _resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        _DOMAIN,
        set_fn=min,  # Лучше раньше, чем позже
        clamp_fn=lambda v: max(0, v),
    )


def get(gs, timer):
    return gs_api.get_value(gs, _DOMAIN, timer)


def set(gs, timer, value):
    gs_api.set_value(gs, _DOMAIN, timer, value)
