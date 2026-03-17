from engine import activities_api, gs_api


def work(hold_required=False, fatigue_cost=1, earn_knowledge=1):
    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +fatigue_cost)
        gs_api.mod_stat(gs, "knowledge", +earn_knowledge)

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") < 10

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required, name="work"
    )


def rest(hold_required=True):
    return activities_api.base_activity(
        lambda gs: gs_api.mod_vital(gs, "fatigue", -1),
        True,
        hold_required,
        name="rest",
    )


def rest_hard():
    return activities_api.override_activity(rest(False), name="rest in peace")


def work_and_rest(definitions=None, state=None, hold_required=True):
    return activities_api.override_activity(
        activities_api.composite_activity(
            state,
            definitions,
            lambda: [
                activities_api.create_activity_entry(work),
                activities_api.create_activity_entry(rest),
            ],
            name="work then rest",
        ),
        hold_required=hold_required,
    )


def cry(state=None, hold_required=True):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +1)
        state["counter"] -= 1

    def can_continue(gs):
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required, name="cry"
    )


def drink_coffee(state=None, hold_required=True):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "sleepiness", -1)
        gs_api.mod_vital(gs, "mental", -1)
        state["counter"] -= 1

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="drink coffee",
    )


def socialize(hold_required=False, earn_fatigue=1, earn_mental=1, state=None):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +earn_fatigue)
        gs_api.mod_vital(gs, "mental", +earn_mental)
        state["counter"] -= 1

    def can_continue(gs):
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        hold_required,
        can_continue,
        name="socialize",
    )


def listen_to_music(hold_required=False, earn_mental=-5, earn_sleepiness=1, state=None):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_stat(gs, "mental", +earn_mental)
        gs_api.mod_stat(gs, "sleepiness", +earn_sleepiness)
        state["counter"] -= 1

    def can_continue(gs):
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        hold_required,
        can_continue,
        name="listen to music",
    )


activities = [
    work,
    rest,
    rest_hard,
    work_and_rest,
    cry,
    socialize,
    drink_coffee,
    listen_to_music,
]
# Раскомментируйте эту строчку, чтобы добавить в игру демо-активности
