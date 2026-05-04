from functools import lru_cache
from inspect import signature, isawaitable
from typing import Callable

from engine.schema import GameState


@lru_cache(maxsize=1024)
def accepts(param: str, func: Callable) -> bool:
    """Проверить, принимает ли функция этот параметр. Результат кэшируется для повышения производительности."""
    sig = signature(func)
    return param in sig.parameters


def _get_result(gs: GameState, func: Callable, *args, **kwargs):
    if accepts("gs", func):
        return func(gs, *args, **kwargs)
    return func(*args, **kwargs)


def call_with_gs(gs: GameState, func: Callable, *args, **kwargs):
    """
    Передать `gs`, если функция ожидает этот аргумент, иначе вызвать функцию без аргументов.

    Позволяет не прописывать этот параметр в функциях, которым он не нужен.
    """
    return _get_result(gs, func, *args, **kwargs)


async def call_with_gs_async(gs: GameState, func: Callable, *args, **kwargs):
    result = _get_result(gs, func, *args, **kwargs)
    return await result if isawaitable(result) else result


def ensure_callable(val) -> Callable:
    """Если значение еще не функция, превратить его в функцию, которая может принимать любые аргументы."""
    return val if callable(val) else (lambda *args, **kwargs: val)
