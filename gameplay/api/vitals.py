from engine import gs_api
from engine.resolver_api import resolve_generic

domain = "vitals"

fatigue = "fatigue"
sleepiness = "sleepiness"
mental = "mental"

initial = {
    fatigue: 0,
    sleepiness: 0,
    mental: 100,
}


def resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        domain,
        set_fn=max,  # Обычно для игрока чем выше, тем хуже
        mod_fn=sum,
        clamp_fn=lambda v: max(
            0, min(100, v)
        ),  # vitals ограничены значениями от 0 до 100
    )


def get(gs, vital):
    return gs_api.get_value(gs, domain, vital)


def set(gs, vital, value):
    gs_api.set_value(gs, domain, vital, value)


def mod(gs, vital, delta):
    gs_api.mod_value(gs, domain, vital, delta)
