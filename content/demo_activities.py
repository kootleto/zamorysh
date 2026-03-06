from engine import activities_api, gs_api


def work(hold_required=False, fatigue_cost=1, earn_money=1):
    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +fatigue_cost)
        gs_api.mod_stat(gs, "money", +earn_money)

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") < 10

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required, name="work"
    )


def rest(hold_required=True):
    return activities_api.base_activity(
        lambda gs: gs_api.mod_vital(gs, "fatigue", -1),
        lambda gs: True,
        hold_required,
        name="rest",
    )


def rest_hard():
    return rest(False)


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


activities = [work, rest, rest_hard, work_and_rest, cry]
