from engine import activities_api
from engine.activities_api import override_activity
from gameplay import productivity
from gameplay.api import stats, schedule, floors, vitals, location


def study():
    def tick_effect(gs):
        stats.mod(gs, stats.KNOWLEDGE, productivity.get(gs) * 0.25)
        vitals.mod(gs, vitals.FATIGUE, -0.25)

    def can_continue(gs):
        return floors.get(gs, floors.CLASSROOM) == schedule.get_current_room(gs)

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required=True, name="учиться"
    )


def auto_study():
    return override_activity(study(), hold_required=False, is_visible=False)


def do_homework():
    def tick_effect(gs):
        stats.mod(gs, stats.KNOWLEDGE, productivity.get(gs) * 0.25)
        vitals.mod(gs, vitals.FATIGUE, -0.25)

    def can_continue(gs):
        return (
            location.get_place(gs) == location.Place.HOME
            or location.get_place(gs) == location.Place.UNIVERSITY
        )

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required=True, name="делать домашку"
    )


ACTIVITIES = [study, auto_study, do_homework]
