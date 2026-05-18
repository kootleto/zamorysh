from engine import activities_api
from gameplay import activity_wrappers
from gameplay.api import time, schedule
from interface import ui


def check_today_schedule(state=None):
    def tick_effect(gs):
        for lesson_time, lesson in schedule.get_day_schedule(
            time.get_weekday(gs)
        ).items():
            ui.display(
                f"{lesson_time} {lesson["subject"]} ({lesson["type"]}) в аудитории {lesson["room"]}"
            )

    def can_continue(gs):
        return time.get_weekday(gs) != time.Weekday.SUNDAY

    return activity_wrappers.single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            name="посмотреть расписание на сегодня",
        ),
        state,
    )


def check_tomorrow_schedule(state=None):
    def tick_effect(gs):
        if time.get_weekday(gs) != time.Weekday.SUNDAY:
            for lesson_time, lesson in schedule.get_day_schedule(
                time.get_weekday(gs) + 1
            ).items():
                ui.display(
                    f"{lesson_time} {lesson["subject"]} ({lesson["type"]}) в аудитории {lesson["room"]}"
                )
        else:
            for lesson_time, lesson in schedule.get_day_schedule(
                time.Weekday.MONDAY
            ).items():
                ui.display(
                    f"{lesson_time} {lesson["subject"]} ({lesson["type"]}) в аудитории {lesson["room"]}"
                )

    def can_continue(gs):
        return time.get_weekday(gs) != time.Weekday.SATURDAY

    return activity_wrappers.single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            name="посмотреть расписание на завтра",
        ),
        state,
    )


def check_current_lesson(state=None):
    def tick_effect(gs):
        if schedule.get_current_lesson(gs)["subject"] is not None:
            ui.display(
                f"{schedule.get_current_subject(gs)} ({schedule.get_current_type(gs)} в аудитории {schedule.get_current_room(gs)}"
            )
        else:
            ui.display("Сейчас нет пар")

    def can_continue(gs):
        return time.get_weekday(gs) != time.Weekday.SUNDAY

    return activity_wrappers.single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            name="посмотреть текущую пару",
        ),
        state,
    )


ACTIVITIES = [
    check_today_schedule,
    check_tomorrow_schedule,
    check_current_lesson,
]
