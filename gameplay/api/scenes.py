from engine import gs_api
from engine.resolver_api import resolve_generic

_DOMAIN = "scenes"

SCENE_NAME = "scene_name"
SPRITE_NAME = "sprite_name"

_INITIAL = {SCENE_NAME: None, SPRITE_NAME: None}


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


def get_current_scene(gs) -> str:
    return gs_api.get_value(gs, _DOMAIN, SCENE_NAME)


def set_scene(gs, name: str):
    print(name)
    gs_api.set_value(gs, _DOMAIN, SCENE_NAME, name)


def get_current_sprite(gs) -> str:
    return gs_api.get_value(gs, _DOMAIN, SPRITE_NAME)


def set_sprite(gs, name: str):
    gs_api.set_value(gs, _DOMAIN, SPRITE_NAME, name)
