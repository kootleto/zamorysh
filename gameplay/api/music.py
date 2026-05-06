from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "music"

TRACK_TITLE = "track_title"

_INITIAL = {TRACK_TITLE: None}


def _resolve(gs, intents):
    resolve_generic(
        gs,
        intents,
        _DOMAIN,
        # Сначала мы сравниваем элементы по первому элементу кортежа, затем по второму
        # False < True, поэтому None всегда меньше, чем строка
        # Если в списке нет None, мы выберем трек с первым по алфавиту названием
        set_fn=lambda values: min(values, key=lambda x: (x is not None, x)),
    )


def get_current_track(gs) -> str:
    return gs_api.get_value(gs, _DOMAIN, TRACK_TITLE)


def play(gs, title: str):
    gs_api.set_value(gs, _DOMAIN, TRACK_TITLE, title)


def stop(gs):
    gs_api.set_value(gs, _DOMAIN, TRACK_TITLE, None)
