from inspect import signature
from typing import Callable

from engine.schema import GameState


def call_with_gs(gs: GameState, func: Callable):
    """
    Передать `gs`, если функция ожидает этот аргумент, иначе вызвать функцию без аргументов.

    Позволяет не прописывать этот параметр в функциях, которым он не нужен.
    """
    sig = signature(func)
    if "gs" in sig.parameters:
        return func(gs)
    return func()


def ensure_callable(val) -> Callable:
    """Если значение еще не функция, превратить его в функцию, которая может принимать любые аргументы."""
    return val if callable(val) else (lambda *args, **kwargs: val)
