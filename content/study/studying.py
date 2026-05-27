from engine import activities_api
from engine.activities_api import override_activity
from gameplay import productivity
from gameplay.api import stats, schedule, floors, vitals


def study():
    def tick_effect(gs):
        stats.mod(gs, stats.KNOWLEDGE, productivity.get(gs) * 0.25)
        vitals.mod(gs, vitals.FATIGUE, 0.25)

    def can_continue(gs):
        return floors.get(gs, floors.CLASSROOM) == schedule.get_current_room(gs)

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required=True, name="учиться"
    )


@activities_api.system_only
def auto_study():
    return override_activity(study(), hold_required=False)


ACTIVITIES = [study, auto_study]
