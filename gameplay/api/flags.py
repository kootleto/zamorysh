from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "flags"

_INITIAL = {}


def _resolve(gs, intents):
    resolve_generic(gs, intents, _DOMAIN, set_fn=any)


def get(gs, flag):
    return gs_api.get_value(gs, _DOMAIN, flag)


def set(gs, flag, value: bool):
    gs_api.set_value(gs, _DOMAIN, flag, value)
