import random

from engine import activities_api, state_api
from gameplay.activity_wrappers import single_tick_activity, timed_activity
from gameplay.api import vitals, stats, location
from interface import ui


@activities_api.on_finish(
    lambda: "Кофе из термоса не такой вкусный, зато это недорого."
)
def drink_coffee(hold_required=False, earn_sleepiness=-1, state=None):

    def tick_effect(gs):
        vitals.mod(gs, vitals.SLEEPINESS, earn_sleepiness)

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required,
            name="выпить кофе",
        ),
        state,
    )


@activities_api.on_finish(
    lambda: ui.display("Вы чувствуете, что это заняло много ваших сил...")
)
def socialize(state=None, hold_required=True):

    def tick_effect(gs):
        vitals.mod(gs, vitals.FATIGUE, +5)
        vitals.mod(gs, vitals.MENTAL, +2)
        stats.mod(gs, stats.SOCIAL, +5)

    def can_continue(gs):
        return location.get_place(gs) != "home"

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required=hold_required,
            name="социализироваться",
        ),
        state,
        duration=10,
    )


@activities_api.on_finish(lambda: ui.display("Эх, благодать!"))
def walk(state=None, hold_required=True):

    def can_continue(gs):
        return location.get_place(gs) == "park"

    def tick_effect(gs):
        vitals.mod(gs, vitals.FATIGUE, -5)
        vitals.mod(gs, vitals.MENTAL, +10)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required,
            name="пойти прогуляться",
        ),
        state,
        duration=10,
    )


@activities_api.on_finish(lambda: ui.display("От музыки на душе всегда лучше!"))
def listen_to_music(state=None, hold_required=True):
    def tick_effect(gs):
        vitals.mod(gs, vitals.MENTAL, +2)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required=hold_required,
            name="послушать музыку",
        ),
        state,
        duration=10,
    )


@activities_api.on_finish(lambda: ui.display("Это было не очень продуктивно..."))
def scroll(state=None, hold_required=True):

    def tick_effect(gs):
        if random.choice([True, False]):
            vitals.mod(gs, vitals.MENTAL, +5)
        else:
            vitals.mod(gs, vitals.MENTAL, -5)
        stats.mod(gs, stats.KNOWLEDGE, -2)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required=hold_required,
            name="скроллить",
        ),
        state,
        duration=10,
    )


@activities_api.on_finish(lambda: ui.display("Слезами горю не поможешь..."))
def cry(state=None):
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        vitals.mod(gs, vitals.FATIGUE, +1)
        state["counter"] -= 1

    def can_continue():
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect, can_continue, True, name="поплакать"
    )


@activities_api.on_finish(lambda: ui.display("Хорошо, что вы заботитесь о себе!"))
def eat_lunch(hold_required=True):

    def tick_effect(gs):
        stats.mod(gs, stats.MONEY, -10)
        vitals.mod(gs, vitals.FATIGUE, -10)

    def can_continue(gs):
        return stats.get(gs, stats.MONEY) > 9 and (
            location.get_place(gs) == "surf_coffee"
            or location.get_place(gs) == "another_coffee"
            or location.get_place(gs) == "university"
        )

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="купить покушать",
    )


@activities_api.on_finish(lambda: ui.display("Приятно ни о чем не думать!"))
def dance(state=None, hold_required=True):
    def tick_effect(gs):
        vitals.mod(gs, vitals.FATIGUE, +2)
        vitals.mod(gs, vitals.MENTAL, +7)

    def can_continue(gs):
        return location.get_place(gs) == "club"

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required=hold_required,
            name="потанцевать",
        ),
        state,
        duration=10,
    )


@activities_api.on_finish(lambda: ui.display("Ботать-ботать."))
def study(state=None, hold_required=True):

    def tick_effect(gs):
        vitals.mod(gs, vitals.FATIGUE, +5)
        vitals.mod(gs, vitals.MENTAL, -5)
        stats.mod(gs, stats.KNOWLEDGE, +5)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required=hold_required,
            name="учиться",
        ),
        state,
        duration=10,
    )


ACTIVITIES = [
    drink_coffee,
    socialize,
    walk,
    scroll,
    eat_lunch,
    study,
    cry,
    listen_to_music,
    dance,
]
