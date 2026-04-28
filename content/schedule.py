from gameplay.api import time

WEEK_SCHEDULE = {
    time.MONDAY: {"13:00": "Лингвистическая антропология"},
    time.TUESDAY: {
        "11:10": "Языковое разнообразие (лекция)",
        "13:00": "Латынь",
        "14:40": "Язык",
    },
    time.WEDNESDAY: {
        "09:30": "Дискретная математика (лекция)",
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
        "11:10": "Цифровая грамотность",
        "13:00": "НИС",
        "14:40": "Язык",
        "16:20": "Введение в лингвистику (лекция)",
    },
    time.SATURDAY: {"11:10": "История"},
}


def get_week_schedule():
    return WEEK_SCHEDULE


def get_day_schedule(weekday):
    return WEEK_SCHEDULE[weekday]


def get_current_lesson(gs):
    for lesson_time, lesson in get_day_schedule(time.get_weekday(gs)).items():
        if (
            0
            <= time.get_hour(gs) * 60
            + time.get_minute(gs)
            - int(lesson_time[:2]) * 60
            - int(lesson_time[3:5])
            <= 120
        ):
            return lesson
    return "Сейчас нет пар"
