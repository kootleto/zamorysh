from engine import activities_api
from gameplay.api import stats, productivity, schedule


def study():
    def tick_effect(gs):
        stats.mod(gs, stats.KNOWLEDGE, productivity.get(gs))

    def can_continue(gs):
        return floors.get(gs, floors.CLASSROOM) == schedule.get_current_lesson(gs)["room"]

    return activities_api.base_activity(tick_effect, can_continue, name="учиться")
