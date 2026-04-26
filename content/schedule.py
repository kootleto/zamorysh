from datetime import datetime

from gameplay.api import time

week_schedule = {
    time.MONDAY: {"13:00": "Лингвистическая антропология"},
    time.TUESDAY: {
        "11:10": "Языковое разнообразие (лекция)",
        "13:00": "Латынь",
        "14:40": "Язык",
    },
    time.WEDNESDAY: {
        "9:30": "Дискретная математика (лекция)",
        "11:10": "Старославянский",
        "12:30": "Языковое разнообразие (семинар)",
        "14:40": "Дискретная математика (семинар)",
        "16:20": "Введение в лингвистику (семинар)",
    },
    time.THURSDAY: {
        "13:00": "Лингвистические данные (лекция)",
        "14:40": "Латынь",
        "16:20": "Лингвистические данные (семинар)",
    },
    time.FRIDAY: {
        "13:00": "НИС",
        "14:40": "Язык",
        "16:20": "Введение в лингвистику (лекция)",
    },
    time.SATURDAY: {"11:10": "История"},
}


def get_week_schedule():
    return week_schedule


def get_day_schedule(weekday, gs):
    return week_schedule[weekday]


def scheduled_time(sch_time: str):
    return datetime.strptime(sch_time, '%H:%M')


def get_current_lesson(gs):
    for lesson_time, lesson in get_day_schedule(gs):
        if (time.get_time(gs) - scheduled_time(lesson_time)).minute <= 120:
            return lesson
    return "Сейчас нет пар"
