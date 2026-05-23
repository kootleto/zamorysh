"""
Работа с локальным состоянием объектов (например, активностей и сценариев).
"""

from typing import Callable


def init_defaults(data: dict | None, **defaults) -> dict:
    """
    Если data — словарь, заполнить отсутствующие элементы значениями по умолчанию и вернуть.

    Если data — None, вернуть значения по умолчанию.

    Этот метод инициализации подходит, если изначальный state всегда одинаковый,
    так как он принимает уже готовый словарь, а не логику инициализации.
    """
    if data is None:
        return defaults
    for key, val in defaults.items():
        data.setdefault(key, val)
    return data


def get_params(params: dict | None, *keys, **defaults):
    params_set = init_defaults(params, **defaults)
    result = tuple(params_set[param] for param in keys)
    return result[0] if len(result) == 1 else result


def init_fn(state: dict | None, fn: Callable[[], dict]) -> dict:
    """
    Если state — пустой словарь, заполнить его результатом вызова функции инициализации и вернуть.

    Если state — `None`, вернуть значения по умолчанию.

    Если state — не пустой словарь, вернуть его. В отличие от `init_defaults`, этот метод не обрабатывает случаи,
    когда в state есть только часть необходимых значений, чтобы не вызывать каждый раз при создании активности
    функцию инициализации, которая может быть тяжелой.

    Этот метод инициализации подходит, если изначальный state вычисляется на основе параметра.
    Он позволяет вызывать логику инициализации только в том случае, если state еще не инициализирован.
    """
    if state is None:
        return fn()
    elif state == {}:
        state.update(fn())
    return state
