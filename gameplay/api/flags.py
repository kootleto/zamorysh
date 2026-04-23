from engine import gs_api
from engine.resolver_api import resolve_generic

domain = "flags"

initial = {}


def resolve(gs, intents):
    resolve_generic(gs, intents, domain, set_fn=any)


def get(gs, flag):
    return gs_api.get_value(gs, domain, flag)


def set(gs, flag, value: bool):
    gs_api.set_value(gs, domain, flag, value)
