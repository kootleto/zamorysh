from enum import StrEnum

from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "quests"

QUESTS = "quests_list"

_INITIAL = {QUESTS: {}}


class Status(StrEnum):
    INACTIVE = "INACTIVE"
    FINISHED = "FINISHED"


def _get_quests(gs):
    return gs_api.get_value(gs, _DOMAIN, QUESTS)


def set_status(gs, quest, status):
    gs_api.set_value(gs, _DOMAIN, quest, status)


def finish(gs, quest):
    gs_api.set_value(gs, _DOMAIN, quest, Status.FINISHED)


def get_status(gs, quest):
    quests = _get_quests(gs)
    if not quest in quests:
        return Status.INACTIVE
    return quests[quest]


def is_active(gs, quest):
    quests = _get_quests(gs)
    return quest in quests and quests[quest] != Status.FINISHED


def _resolve(gs, intents):

    def apply_status(_gs, _domain, target, value):
        quests = _get_quests(_gs)
        quests[target] = value

    resolve_generic(
        gs,
        intents,
        _DOMAIN,
        set_fn=min,
        get_fn=lambda _gs, _domain, _target: _get_quests(_gs),
        apply_fn=apply_status,
    )
