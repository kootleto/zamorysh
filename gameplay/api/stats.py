from engine import gs_api
from engine.resolver_api import resolve_generic

domain = "stats"

money = "money"
social = "social"
knowledge = "knowledge"

initial = {
    money: 0,
    social: 0,
    knowledge: 0,
}


def resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        domain,
        set_fn=min,  # Обычно для игрока чем ниже, тем хуже
        mod_fn=sum,
        clamp_fn=lambda v: max(0, v),
    )


def get(gs, stat):
    return gs_api.get_value(gs, domain, stat)


def set(gs, stat, value):
    gs_api.set_value(gs, domain, stat, value)


def mod(gs, stat, delta):
    gs_api.mod_value(gs, domain, stat, delta)
