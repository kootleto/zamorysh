# WORK IN PROGRESS
from collections import defaultdict

from engine import gs_api
from tools.logger import log


def base_task(task_type="default", required=100):
    return {
        "progress": 0,
        "required": required,
        "type": task_type,
        "is_completed": False,
    }


def add_task(gs, task):
    task = gs_api.with_id(gs, task)
    gs["tasks"].append(task)
    return task["id"]


def get_progress(task):
    return task["progress"]


def set_progress(task, value):
    task["progress"] = value
    if task["progress"] == task["required"]:
        task["is_completed"] = True


def get_required(task):
    return task["required"]


def get_type(task):
    return task["type"]


def is_completed(task):
    return task["is_completed"]


def increment_task_progress(gs, task_id, delta):
    if delta < 0:
        raise ValueError(f"Progress increment must be non-negative (task_id={task_id})")
    gs["intents"].append(
        {"type": "task", "target": task_id, "op": "mod", "value": delta}
    )
    task = get_task_by_id(gs, task_id)
    task["progress"] = min(task["required"], task["progress"] + delta)
    if task["progress"] == task["required"]:
        task["is_completed"] = True


def get_task_by_id(gs, task_id):
    for task in gs["tasks"]:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Task with id {task_id} not found")


def resolve_tasks(gs, intents):
    grouped_intents = defaultdict(lambda: {"mod": [], "set": []})
    for intent in intents:
        grouped_intents[intent["target"]][intent["op"]].append(intent)
    for target, grouped in grouped_intents.items():
        task = get_task_by_id(gs, target)
        value = get_progress(task)
        value += sum([i["value"] for i in grouped["mod"]])
        value = min(value, get_required(task))

        log(
            f"Task {target} progress {get_progress(task)} -> {value} / {tasks.get_required(task)}",
            log_type="resolver",
        )

        set_progress(task, value)
