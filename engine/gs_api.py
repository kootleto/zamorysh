from copy import deepcopy

from tools.logger import log

initial_system_data = {
    "time": 0,
    "activity_entries": [],
    "scenario_entries": [],
    "intents": [],
    "next_id": 0,
    "is_end": False,
}


def get_initial_gs(initial_state):
    # deepcopy позволяет возвращать не ссылку на словарь и не словарь ссылок, а истинную копию словаря
    return {
        "gameplay": deepcopy(initial_state),
        "system": deepcopy(initial_system_data),
    }


def get_value(gs, domain, key):
    return gs["gameplay"][domain][key]


# Функции не мутируют gs напрямую, а создают интенты (намерения),
# которые потом считывает резолвер.
# Это нужно для того, чтобы то, что в логике игры выполняется одновременно, работало с одним и тем же состоянием
def push_intent(gs, domain, key, value, operation):
    gs["system"]["intents"].append(
        {"domain": domain, "target": key, "op": operation, "value": value}
    )
    log(operation.upper(), domain.upper(), key, value, log_type="intent")


def set_value(gs, domain, key, value):
    push_intent(gs, domain, key, value, "set")


def mod_value(gs, domain, key, delta):
    push_intent(gs, domain, key, delta, "mod")


def stop(gs):
    set_value(gs, "system", "is_end", True)


# Системные функции движка
# Здесь не используются интенты,
# потому что эти изменения мгновенные и не могут ни с чем конфликтовать


def is_running(gs):
    return not gs["system"]["is_end"]


def get_time(gs):
    return gs["system"]["time"]


def tick(gs):
    gs["system"]["time"] += 1


def get_activity_entries(gs):
    return gs["system"]["activity_entries"]


def set_activity_entries(gs, entries):
    gs["system"]["activity_entries"] = entries


def get_scenario_entries(gs):
    return gs["system"]["scenario_entries"]


# При добавлении любого объекта в gs следует присваивать ему ID,
# чтобы объект можно было запомнить и потом идентифицировать


def with_id(gs, obj):
    """Вернуть словарь объекта, присвоив ему уникальный ID."""
    obj_id = gs["system"]["next_id"]
    gs["system"]["next_id"] += 1
    return {**obj, "id": obj_id}
