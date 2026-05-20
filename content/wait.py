from engine import gs_api, activities_api


def wait():
    def tick_effect(gs):
        gs_api.multiply_next_tick_interval(gs, 0.01)

    return activities_api.base_activity(
        tick_effect, hold_required=True, name="подождать"
    )


ACTIVITIES = [wait]
