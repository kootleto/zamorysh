"""Все эти функции следует вызывать только из движка.
Если вы вызываете их откуда-то ещё, вы делаете что-то неправильно."""

from copy import deepcopy
from typing import Any

from engine.schema import SystemState, GameState, ActivityEntry, ScenarioEntry, Intent
from tools.logger import log

DEFAULT_TICK_INTERVAL = 0.15

INITIAL_SYSTEM_DATA: SystemState = {
    "time": 0,
    "activity_entries": [],
    "scenario_entries": [],
    "intents": [],
    "just_finished": [],
    "next_id": 0,
    "is_running": True,
    "tick_interval": DEFAULT_TICK_INTERVAL,
}


def init_gs(initial_state: dict[str, dict]) -> GameState:
    # deepcopy позволяет возвращать не ссылку на словарь и не словарь ссылок, а истинную копию словаря
    return {
        "gameplay": deepcopy(initial_state),
        "system": deepcopy(INITIAL_SYSTEM_DATA),
    }


# Гетеры


def get_activity_entries(gs: GameState) -> list[ActivityEntry]:
    return gs["system"]["activity_entries"]


def get_scenario_entries(gs: GameState):
    return gs["system"]["scenario_entries"]


def get_intents(gs: GameState) -> list[Intent]:
    return gs["system"]["intents"]


def get_just_finished(gs: GameState) -> list[ActivityEntry]:
    return gs["system"]["just_finished"]


def is_running(gs: GameState) -> bool:
    return gs["system"]["is_running"]


def get_tick_interval(gs: GameState) -> float:
    return gs["system"]["tick_interval"]


# Сетеры


def apply_value(gs: GameState, domain: str, key: str, value: Any):
    gs["gameplay"][domain][key] = value


def set_activity_entries(gs: GameState, entries: list[ActivityEntry]):
    gs["system"]["activity_entries"] = entries


def clear_intents(gs: GameState):
    gs["system"]["intents"].clear()


def clear_just_finished(gs: GameState):
    gs["system"]["just_finished"].clear()


def apply_is_running(gs: GameState, value: bool):
    gs["system"]["is_running"] = value


def apply_tick_interval(gs: GameState, interval: int | float):
    gs["system"]["tick_interval"] = interval


# Модификаторы


def tick(gs: GameState):
    gs["system"]["time"] += 1


def add_activity_entry(gs: GameState, entry: ActivityEntry):
    log("Add activity entry:", entry)
    gs["system"]["activity_entries"].append(entry)


def add_scenario_entry(gs: GameState, entry: ScenarioEntry):
    gs["system"]["scenario_entries"].append(entry)


def add_finished_entry(gs: GameState, entry: ActivityEntry):
    gs["system"]["just_finished"].append(entry)
