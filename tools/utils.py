from inspect import signature
from typing import Callable


def call_with_gs(gs: dict, func: Callable):
    """
    Передать `gs`, если функция ожидает этот аргумент, иначе вызвать функцию без аргументов.

    Позволяет не прописывать этот параметр в функциях, которым он не нужен.
    """
    sig = signature(func)
    if "gs" in sig.parameters:
        return func(gs)
    return func()
