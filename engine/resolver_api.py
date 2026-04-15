from collections import defaultdict
from typing import Callable, Iterable

from tools.logger import log


def resolve_intents(gs, resolvers):
    # Добавляем обработку окончания игры
    resolvers["system"] = resolve_system

    # Группируем интенты по категории в gs, к которой относится цель
    grouped_intents = defaultdict(list)
    for intent in gs["system"]["intents"]:
        grouped_intents[intent["domain"]].append(intent)

    # Для каждого типа пытаемся применить резолвер с соответствующим именем.
    # Если такого нет, вызываем ошибку
    for intent_domain, intents in grouped_intents.items():
        try:
            resolver = resolvers[intent_domain]
            resolver(gs, intents)
        except KeyError:
            raise NotImplementedError(
                f"No resolver implemented for intent domain '{intent_domain}'"
            )

    # После обработки интентов очищаем массив в gs
    gs["system"]["intents"].clear()


def resolve_generic(
    gs,
    intents: Iterable[dict],
    domain: str,
    set_fn: Callable = max,
    mod_fn: Callable = sum,
    clamp_fn: Callable = lambda x: x,
):
    """
    Универсальный резолвер для категории domain.

    Работает по следующему алгоритму:
    1. Применяет изменения типа set при помощи set_fn.
    2. К результату применяет изменения типа mod при помощи mod_fn.
    3. Если результат выходит за границы допустимых значений, возвращает его в эти границы
    при помощи clamp_fn.
    """
    # Группируем интенты по цели и виду операции (mod или set)
    grouped_intents = defaultdict(lambda: {"mod": [], "set": []})
    for intent in intents:
        grouped_intents[intent["target"]][intent["op"]].append(intent)

    # Применяем изменения для каждой цели
    for target, grouped in grouped_intents.items():
        if grouped["set"]:
            value = set_fn([i["value"] for i in grouped["set"]])
        else:
            value = gs["gameplay"][domain][target]
        value += mod_fn([i["value"] for i in grouped["mod"]])
        value = clamp_fn(value)
        log(
            f"{target} {gs["gameplay"][domain][target]} -> {value}", log_type="resolver"
        )
        gs["gameplay"][domain][target] = value


# Обработка остановки игры
def resolve_system(gs, intents):
    if any(intent["target"] == "is_end" and intent["value"] for intent in intents):
        gs["system"]["is_end"] = True
