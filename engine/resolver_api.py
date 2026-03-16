from collections import defaultdict
from typing import Callable, Iterable

from gameplay import tasks
from tools.logger import log


def resolve_intents(gs):

    # Группируем интенты по категории в gs, к которой относится цель
    grouped_intents = defaultdict(list)
    for intent in gs["intents"]:
        grouped_intents[intent["type"]].append(intent)

    # Для каждого типа пытаемся применить резолвер с соответствующим именем.
    # Если такого нет, вызываем ошибку
    for intent_type, intents in grouped_intents.items():
        resolver_name = f"resolve_{intent_type}s"
        if resolver_name in globals():
            globals()[resolver_name](gs, intents)
        else:
            raise NotImplementedError(
                f"No resolver implemented for intent type '{intent_type}'"
            )

    # После обработки интентов очищаем массив в gs
    gs["intents"].clear()


def resolve_generic(
    gs,
    intents: Iterable[dict],
    gs_key: str,
    set_fn: Callable = max,
    mod_fn: Callable = sum,
    clamp_fn: Callable = lambda x: x,
):
    """
    Универсальный резолвер для категории gs_key.

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
            value = gs[gs_key][target]
        value += mod_fn([i["value"] for i in grouped["mod"]])
        value = clamp_fn(value)
        log(f"{target} {gs[gs_key][target]} -> {value}", log_type="resolver")
        gs[gs_key][target] = value


def resolve_vitals(gs, intents):
    resolve_generic(
        gs,
        intents,
        "vitals",
        set_fn=max,  # Обычно для игрока чем выше, тем хуже
        mod_fn=sum,
        clamp_fn=lambda v: max(
            0, min(100, v)
        ),  # vitals ограничены значениями от 0 до 100
    )


def resolve_stats(gs, intents):
    resolve_generic(
        gs,
        intents,
        "stats",
        set_fn=min,  # Обычно для игрока чем ниже, тем хуже
        mod_fn=sum,
        clamp_fn=lambda v: max(0, v),
    )


def resolve_flags(gs, intents):
    resolve_generic(
        gs,
        intents,
        "flags",
        set_fn=any,  # Логическое ИЛИ
        clamp_fn=lambda v: v,
    )


def resolve_timers(gs, intents):
    resolve_generic(
        gs,
        intents,
        "timers",
        set_fn=min,  # Лучше раньше, чем позже
        clamp_fn=lambda v: max(0, v),
    )


# WORK IN PROGRESS
def resolve_tasks(gs, intents):
    grouped_intents = defaultdict(lambda: {"mod": [], "set": []})
    for intent in intents:
        grouped_intents[intent["target"]][intent["op"]].append(intent)
    for target, grouped in grouped_intents.items():
        task = tasks.get_task_by_id(gs, target)
        value = tasks.get_progress(task)
        value += sum([i["value"] for i in grouped["mod"]])
        value = min(value, tasks.get_required(task))

        log(
            f"Task {target} progress {tasks.get_progress(task)} -> {value} / {tasks.get_required(task)}",
            log_type="resolver",
        )

        tasks.set_progress(task, value)
