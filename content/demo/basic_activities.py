from engine import activities_api, state_api
from gameplay.api import vitals


def drink_coffee(state=None, hold_required=True):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        vitals.mod(gs, vitals.sleepiness, -1)
        vitals.mod(gs, vitals.mental, -1)
        state["counter"] -= 1

    def can_continue(gs):
        return vitals.get(gs, vitals.sleepiness) > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="drink coffee",
    )


def socialize(hold_required=False, earn_fatigue=1, earn_mental=1, state=None):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        vitals.mod(gs, vitals.fatigue, +earn_fatigue)
        vitals.mod(gs, vitals.mental, +earn_mental)
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
        vitals.mod(gs, vitals.mental, +earn_mental)
        vitals.mod(gs, vitals.sleepiness, +earn_sleepiness)
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
