from copy import deepcopy

from tools.logger import log

# Начальное состояние игры. Сюда надо добавлять все новые поля
initial_gs = {
    "vitals": {
        "fatigue": 0,
        "sleepiness": 0,
        "mental": 100,
    },
    "stats": {
        "money": 0,
        "social": 0,
        "knowledge": 0,
    },
    "flags": {
        "is_end": False,
    },
    "timers": {
        "alarm": 0,
    },
    "time": 0,
    "activity_entries": [],
    "scenario_entries": [],
    "intents": [],
    "next_id": 0,
}


def get_initial_gs():
    # deepcopy позволяет возвращать не ссылку на словарь и не словарь ссылок, а истинную копию словаря,
    # чтобы при его изменении не менялся сам словарь initial_gs
    return deepcopy(initial_gs)


# Все операции над gs выполняются через функции API. Это позволяет активностям и сценариям
# не знать о внутренней структуре движка


def get_vital(gs, vital):
    return gs["vitals"][vital]


def get_stat(gs, stat):
    return gs["stats"][stat]


def get_flag(gs, flag):
    return gs["flags"][flag]


def get_timer(gs, timer):
    return gs["timers"][timer]


def get_time(gs):
    return gs["time"]


def get_activity_entries(gs):
    return gs["activity_entries"]


def get_scenario_entries(gs):
    return gs["scenario_entries"]


# Функции не мутируют gs напрямую, а создают интенты (намерения),
# которые потом считывает резолвер.
# Это нужно для того, чтобы то, что в логике игры выполняется одновременно, работало с одним и тем же состоянием


def set_vital(gs, vital, value):
    gs["intents"].append(
        {"type": "vital", "target": vital, "op": "set", "value": value}
    )
    log("SET VITAL", vital, value, log_type="intent")


def set_stat(gs, stat, value):
    gs["intents"].append({"type": "stat", "target": stat, "op": "set", "value": value})
    log("SET STAT", stat, value, log_type="intent")


def set_flag(gs, flag, value):
    gs["intents"].append({"type": "flag", "target": flag, "op": "set", "value": value})
    log("SET FLAG", flag, value, log_type="intent")


def set_timer(gs, timer, value):
    gs["intents"].append(
        {"type": "timer", "target": timer, "op": "set", "value": value}
    )
    log("SET TIMER", timer, value, log_type="intent")


def mod_vital(gs, vital, delta):
    gs["intents"].append(
        {"type": "vital", "target": vital, "op": "mod", "value": delta}
    )
    log("MOD VITAL", vital, delta, log_type="intent")


def mod_stat(gs, stat, delta):
    gs["intents"].append({"type": "stat", "target": stat, "op": "mod", "value": delta})
    log("MOD STAT", stat, delta, log_type="intent")


# Системные функции движка
# В отличие от других модификаторов и сетеров, здесь не используются интенты,
# потому что эти изменения мгновенные и не могут ни с чем конфликтовать


def tick(gs):
    gs["time"] += 1


def set_activity_entries(gs, entries):
    gs["activity_entries"] = entries


# При добавлении любого объекта в gs следует присваивать ему ID,
# чтобы объект можно было запомнить и потом идентифицировать


def with_id(gs, obj):
    """Вернуть словарь объекта, присвоив ему уникальный ID."""
    obj_id = gs["next_id"]
    gs["next_id"] += 1
    return {**obj, "id": obj_id}
