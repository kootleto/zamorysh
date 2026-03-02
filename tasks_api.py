import gs_api

def make_task(task_type="default", required=100):
    return {
        "progress": 0,
        "required": required,
        "type": task_type,
        "is_completed": False,
    }

def add_task(gs, task):
    task = gs_api.with_id(gs, task)
    gs["tasks"].append(task)

def get_task_progress(gs, task_id):
    return get_task_by_id(gs, task_id)["progress"]

def get_task_type(gs, task_id):
    return get_task_by_id(gs, task_id)["type"]

def is_task_completed(gs, task_id):
    return get_task_by_id(gs, task_id)["is_completed"]

def increment_task_progress(gs, task_id, delta):
    if delta < 0:
        raise ValueError(f"Progress increment must be non-negative (task_id={task_id})")
    task = get_task_by_id(gs, task_id)
    task["progress"] = min(task["required"], task["progress"] + delta)
    if task["progress"] == task["required"]:
        task["is_completed"] = True


def get_task_by_id(gs, task_id):
    for task in gs["tasks"]:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Task with id {task_id} not found")