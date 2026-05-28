from collections.abc import Mapping
from typing import Any, TypeVar

from engine import gs_core, activities_api
from engine.schema import (
    GameState,
    Operation,
    ActivityDefinitions,
)
from tools.logger import log


# Функции не мутируют gs напрямую, а создают интенты (намерения),
# которые потом считывает резолвер.
# Это нужно для того, чтобы то, что в логике игры выполняется одновременно, работало с одним и тем же состоянием


def get_value(gs: GameState, domain: str, key: str) -> Any:
    return gs["gameplay"][domain][key]


def push_intent(gs: GameState, domain: str, key: str, value: Any, operation: Operation):
    gs["system"]["intents"].append(
        {"domain": domain, "target": key, "op": operation, "value": value}
    )
    log(operation.upper(), domain.upper(), key, value, log_type="intent")


def set_value(gs: GameState, domain: str, key: str, value: Any):
    push_intent(gs, domain, key, value, "set")


def mod_value(gs: GameState, domain: str, key: str, delta: Any):
    push_intent(gs, domain, key, delta, "mod")


# Некоторые значения из SystemState можно менять или получать через gs_api


def stop(gs: GameState):
    set_value(gs, "system", "is_running", False)


def get_tick_interval(gs: GameState):
    return gs["system"]["tick_interval"]


def set_next_tick_interval(gs: GameState, interval: int | float):
    set_value(gs, "system", "tick_interval", interval)


def multiply_next_tick_interval(gs: GameState, multiplier: int | float):
    mod_value(gs, "system", "tick_interval", multiplier)


def get_time(gs: GameState) -> int:
    return gs["system"]["time"]


def get_active_tags(gs: GameState, definitions: ActivityDefinitions) -> list[str]:
    entries = gs_core.get_activity_entries(gs)
    tags = set()
    for entry in entries:
        definition_tags = activities_api.read_tags(definitions[entry["activity_name"]])
        tags.update(definition_tags)
    return list(tags)


# При добавлении любого объекта в gs следует присваивать ему ID,
# чтобы объект можно было запомнить и потом идентифицировать

T = TypeVar("T", bound=Mapping[str, Any])


def with_id(gs: GameState, obj: T) -> T:
    """Вернуть словарь объекта, присвоив ему уникальный ID."""
    obj_id = gs["system"]["next_id"]
    gs["system"]["next_id"] += 1
    return {**obj, "id": obj_id}
