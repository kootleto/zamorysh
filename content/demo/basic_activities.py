from engine import activities_api, gs_api, state_api


def drink_coffee(state=None, hold_required=True):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "sleepiness", -1)
        gs_api.mod_vital(gs, "mental", -1)
        state["counter"] -= 1

    def can_continue(gs):
        return gs_api.get_vital(gs, "sleepiness") > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="drink coffee",
    )


def socialize(hold_required=False, earn_fatigue=1, earn_mental=1, state=None):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +earn_fatigue)
        gs_api.mod_vital(gs, "mental", +earn_mental)
        state["counter"] -= 1

    def can_continue():
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="socialize",
    )


def listen_to_music(hold_required=False, earn_mental=-5, earn_sleepiness=1, state=None):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "mental", +earn_mental)
        gs_api.mod_vital(gs, "sleepiness", +earn_sleepiness)
        state["counter"] -= 1

    def can_continue():
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="listen to music",
    )


activities = [drink_coffee, socialize, listen_to_music]
