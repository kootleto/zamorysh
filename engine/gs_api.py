import copy

from tools import logger

initial_gs = {
    "vitals": {
        "fatigue": 0,
    },
    "stats": {
        "money": 0,
    },
    "flags": {
        "is_end": False,
    },
    "time": 0,
    "activity_entries": [],
    "scenario_entries": [],
    "tasks": [],
    "intents": [],
    "next_id": 0,
}


def get_initial_gs():
    return copy.deepcopy(initial_gs)


def get_vital(gs, vital):
    return gs["vitals"][vital]


def mod_vital(gs, vital, delta):
    gs["intents"].append(
        {"type": "vital", "target": vital, "op": "mod", "value": delta}
    )
    logger.log("MOD VITAL", vital, delta, log_type="intent")


def get_stat(gs, stat):
    return gs["stats"][stat]


def set_stat(gs, stat, value):
    gs["intents"].append({"type": "stat", "target": stat, "op": "set", "value": value})
    logger.log("SET STAT", stat, value, log_type="intent")


def mod_stat(gs, stat, delta):
    gs["intents"].append({"type": "stat", "target": stat, "op": "mod", "value": delta})
    logger.log("MOD STAT", stat, delta, log_type="intent")


def get_flag(gs, flag):
    return gs["flags"][flag]


def set_flag(gs, flag, value):
    gs["intents"].append({"type": "flag", "target": flag, "op": "set", "value": value})
    logger.log("SET FLAG", flag, value, log_type="intent")


def tick(gs):
    gs["time"] += 1


def get_time(gs):
    return gs["time"]


def get_activity_entries(gs):
    return gs["activity_entries"]


def set_activity_entries(gs, entries):
    gs["activity_entries"] = entries


def get_scenario_entries(gs):
    return gs["scenario_entries"]


def with_id(gs, obj):
    obj_id = gs["next_id"]
    gs["next_id"] += 1
    return {**obj, "id": obj_id}
