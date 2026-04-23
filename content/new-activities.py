from engine import activities_api, gs_api, state_api
import random


def drink_coffee(
    hold_required=False, earn_sleepiness=-5, earn_mental=5, earn_money=-10, state=None
):
    state = state_api.init_defaults(state, counter=1)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "sleepiness", earn_sleepiness)
        gs_api.mod_vital(gs, "mental", earn_mental)
        gs_api.mod_stat(gs, "money", earn_money)
        state["counter"] -= 1

    def can_continue(gs):
        return gs_api.get_stat(gs, "money") > 9 and state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="drink coffee",
    )


def socialize(state=None, hold_required=True):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +5)
        gs_api.mod_vital(gs, "mental", +2)
        gs_api.mod_stat(gs, "social", +5)
        state["counter"] -= 1

    def can_continue():
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="socialize",
    )


def walk(state=None, hold_required=True):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", -5)
        gs_api.mod_vital(gs, "mental", +10)
        state["counter"] -= 1

    def can_continue():
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="walk",
    )


def scroll(state=None, hold_required=True):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        if random.choice([True, False]):
            gs_api.mod_vital(gs, "mental", +5)
        else:
            gs_api.mod_vital(gs, "mental", -5)
        gs_api.mod_stat(gs, "knowledge", -2)
        state["counter"] -= 1

    def can_continue():
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="scroll",
    )


def eat_lunch(state=None, hold_required=True):
    state = state_api.init_defaults(state)

    def tick_effect(gs):
        gs_api.mod_stat(gs, "money", -10)
        gs_api.mod_vital(gs, "fatigue", -10)

    def can_continue(gs):
        return gs_api.get_stat(gs, "money") > 9

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="eat_lunch",
    )


def study(state=None, hold_required=True):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +5)
        gs_api.mod_vital(gs, "mental", -5)
        gs_api.mod_stat(gs, "knowledge", +5)
        state["counter"] -= 1

    def can_continue(gs):
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="study",
    )


activities = [drink_coffee, socialize, walk, scroll, eat_lunch, study]
