import random

from engine import activities_api
from gameplay.activity_wrappers import single_tick_activity, timed_activity
from gameplay.api import vitals, stats


def drink_coffee(
    hold_required=False, earn_sleepiness=-5, earn_mental=5, earn_money=-10, state=None
):

    def tick_effect(gs):
        vitals.mod(gs, vitals.sleepiness, earn_sleepiness)
        vitals.mod(gs, vitals.mental, earn_mental)
        stats.mod(gs, stats.money, earn_money)

    def can_continue(gs):
        return stats.get(gs, stats.money) > 9

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required,
            name="drink coffee",
        ),
        state,
    )


def socialize(state=None, hold_required=True):

    def tick_effect(gs):
        vitals.mod(gs, vitals.fatigue, +5)
        vitals.mod(gs, vitals.mental, +2)
        stats.mod(gs, stats.social, +5)
        stats.mod(gs, stats.money, +5)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required=hold_required,
            name="socialize",
        ),
        state,
        duration=10,
    )


def walk(state=None, hold_required=True):

    def tick_effect(gs):
        vitals.mod(gs, vitals.fatigue, -5)
        vitals.mod(gs, vitals.mental, +10)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required=hold_required,
            name="walk",
        ),
        state,
        duration=10,
    )


def scroll(state=None, hold_required=True):

    def tick_effect(gs):
        if random.choice([True, False]):
            vitals.mod(gs, vitals.mental, +5)
        else:
            vitals.mod(gs, vitals.mental, -5)
        stats.mod(gs, stats.knowledge, -2)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required=hold_required,
            name="scroll",
        ),
        state,
        duration=10,
    )


def eat_lunch(hold_required=True):

    def tick_effect(gs):
        stats.mod(gs, stats.money, -10)
        vitals.mod(gs, vitals.fatigue, -10)

    def can_continue(gs):
        return stats.get(gs, stats.money) > 9

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="eat_lunch",
    )


def study(state=None, hold_required=True):

    def tick_effect(gs):
        vitals.mod(gs, vitals.fatigue, +5)
        vitals.mod(gs, vitals.mental, -5)
        stats.mod(gs, stats.knowledge, +5)

    return timed_activity(
        activities_api.base_activity(
            tick_effect,
            hold_required=hold_required,
            name="study",
        ),
        state,
        duration=10,
    )


activities = [drink_coffee, socialize, walk, scroll, eat_lunch, study]
