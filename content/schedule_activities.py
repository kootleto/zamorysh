from content import schedule
from engine import activities_api
from gameplay import activity_wrappers
from gameplay.api import time
from interface import ui


def check_today_schedule():
    def tick_effect(gs):
        for lesson_time, lesson in schedule.get_day_schedule(
            time.get_weekday(gs)
        ).items():
            ui.display(f"{lesson_time}: {lesson}")

    def can_continue(gs):
        return time.get_weekday(gs) != time.SUNDAY

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required=True,
        name="посмотреть расписание на сегодня",
    )


def check_tomorrow_schedule():
    def tick_effect(gs):
        if time.get_weekday(gs) != time.SUNDAY:
            for lesson_time, lesson in schedule.get_day_schedule(
                time.get_weekday(gs) + 1
            ).items():
                ui.display(f"{lesson_time}: {lesson}")
        else:
            for lesson_time, lesson in schedule.get_day_schedule(time.MONDAY).items():
                ui.display(f"{lesson_time}: {lesson}")

    def can_continue(gs):
        return time.get_weekday(gs) != time.SATURDAY

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required=True,
        name="посмотреть расписание на завтра",
    )


def check_current_lesson():
    def tick_effect(gs):
        ui.display(schedule.get_current_lesson(gs))

    def can_continue(gs):
        return time.get_weekday(gs) != time.SUNDAY

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required=True,
        name="посмотреть текущую пару",
    )


activities = [
    activity_wrappers.single_tick_activity(check_today_schedule),
    activity_wrappers.single_tick_activity(check_tomorrow_schedule),
    activity_wrappers.single_tick_activity(check_current_lesson),
]
