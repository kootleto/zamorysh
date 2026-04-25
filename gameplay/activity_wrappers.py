from engine import state_api, activities_api


def timed_activity(activity, state=None, duration=30):
    """Создать активность, которая принудительно завершается после duration тиков (но может и раньше!)."""
    state = state_api.init_defaults(state, timed={"elapsed": 0})

    def wrapped_tick_effect(gs):
        state["timed"]["elapsed"] += 1
        activities_api.apply_tick_effect(gs, activity)

    def wrapped_can_continue(gs):
        return state["timed"][
            "elapsed"
        ] < duration and activities_api.check_can_continue(gs, activity)

    return activities_api.override_activity(
        activity, tick_effect=wrapped_tick_effect, can_continue=wrapped_can_continue
    )


def single_tick_activity(activity, state=None):
    """Создать активность, которая длится всего тик. Удобно для простых атомарных действий."""
    return timed_activity(activity, state, 1)
