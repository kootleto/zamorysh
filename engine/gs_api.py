from collections.abc import Mapping
from copy import deepcopy
from typing import Any, TypeVar

from engine.schema import GameState, SystemState, Operation, ActivityEntry
from tools.logger import log

initial_system_data: SystemState = {
    "time": 0,
    "activity_entries": [],
    "scenario_entries": [],
    "intents": [],
    "next_id": 0,
    "is_end": False,
}


def get_initial_gs(initial_state: dict[str, dict]) -> GameState:
    # deepcopy позволяет возвращать не ссылку на словарь и не словарь ссылок, а истинную копию словаря
    return {
        "gameplay": deepcopy(initial_state),
        "system": deepcopy(initial_system_data),
    }


def get_value(gs: GameState, domain: str, key: str) -> Any:
    return gs["gameplay"][domain][key]


# Функции не мутируют gs напрямую, а создают интенты (намерения),
# которые потом считывает резолвер.
# Это нужно для того, чтобы то, что в логике игры выполняется одновременно, работало с одним и тем же состоянием
def push_intent(gs: GameState, domain: str, key: str, value: Any, operation: Operation):
    gs["system"]["intents"].append(
        {"domain": domain, "target": key, "op": operation, "value": value}
    )
    log(operation.upper(), domain.upper(), key, value, log_type="intent")


def set_value(gs: GameState, domain: str, key: str, value: Any):
    push_intent(gs, domain, key, value, "set")


def mod_value(gs: GameState, domain: str, key: str, delta: Any):
    push_intent(gs, domain, key, delta, "mod")


def stop(gs: GameState):
    set_value(gs, "system", "is_end", True)


def get_time(gs: GameState) -> int:
    return gs["system"]["time"]


# Системные функции движка
# Здесь не используются интенты,
# потому что эти изменения мгновенные и не могут ни с чем конфликтовать


def is_running(gs: GameState) -> bool:
    return not gs["system"]["is_end"]


def tick(gs: GameState):
    gs["system"]["time"] += 1


def get_activity_entries(gs: GameState) -> list[ActivityEntry]:
    return gs["system"]["activity_entries"]


def set_activity_entries(gs: GameState, entries: list[ActivityEntry]):
    gs["system"]["activity_entries"] = entries


def get_scenario_entries(gs: GameState):
    return gs["system"]["scenario_entries"]


# При добавлении любого объекта в gs следует присваивать ему ID,
# чтобы объект можно было запомнить и потом идентифицировать

T = TypeVar("T", bound=Mapping[str, Any])


def with_id(gs: GameState, obj: T) -> T:
    """Вернуть словарь объекта, присвоив ему уникальный ID."""
    obj_id = gs["system"]["next_id"]
    gs["system"]["next_id"] += 1
    return {**obj, "id": obj_id}
