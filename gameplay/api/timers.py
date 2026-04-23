from engine import gs_api
from engine.resolver_api import resolve_generic

domain = "timers"

alarm = "alarm"

initial = {
    alarm: 0,
}


def resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        domain,
        set_fn=min,  # Лучше раньше, чем позже
        clamp_fn=lambda v: max(0, v),
    )


def get(gs, timer):
    return gs_api.get_value(gs, domain, timer)


def set(gs, timer, value):
    gs_api.set_value(gs, domain, timer, value)
