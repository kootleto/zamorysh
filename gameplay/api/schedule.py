from gameplay.api import time

WEEK_SCHEDULE = {
    time.Weekday.MONDAY: {
        "13:00": {"subject": "Английский", "room": 205, "type": "семинар"}
    },
    time.Weekday.TUESDAY: {
        "11:10": {"subject": "Языковое разнообразие", "room": 511, "type": "лекция"},
        "13:00": {"subject": "Латынь", "room": 506, "type": "семинар"},
        "14:40": {"subject": "Язык", "room": 516, "type": "семинар"},
    },
    time.Weekday.WEDNESDAY: {
        "09:30": {"subject": "Дискретная математика", "room": 501, "type": "лекция"},
        "11:10": {"subject": "Старославянский", "room": 507, "type": "семинар"},
        "12:30": {"subject": "Языковое разнообразие", "room": 316, "type": "семинар"},
        "14:40": {"subject": "Дискретная математика", "room": 505, "type": "семинар"},
        "16:20": {"subject": "Введение в лингвистику", "room": 507, "type": "семинар"},
    },
    time.Weekday.THURSDAY: {
        "13:00": {"subject": "Лингвистические данные", "room": 501, "type": "лекция"},
        "14:40": {"subject": "Латынь", "room": 506, "type": "семинар"},
        "16:20": {"subject": "Лингвистические данные", "room": 401, "type": "семинар"},
    },
    time.Weekday.FRIDAY: {
        "11:10": {"subject": "Цифровая грамотность", "room": 509, "type": "семинар"},
        "13:00": {"subject": "НИС", "room": 505, "type": "семинар"},
        "14:40": {"subject": "Язык", "room": 516, "type": "семинар"},
        "16:20": {"subject": "Введение в лингвистику", "room": 501, "type": "лекция"},
    },
    time.Weekday.SATURDAY: {
        "11:10": {"subject": "История", "room": 502, "type": "семинар"}
    },
}


def get_week_schedule():
    return WEEK_SCHEDULE


def get_day_schedule(weekday):
    return WEEK_SCHEDULE[weekday]


def get_current_lesson(gs):
    current_lesson = {"subject": None, "room": None, "type": None}
    for lesson_time, lesson in get_day_schedule(time.get_weekday(gs)).items():
        if (
            0
            <= time.get_hour(gs) * 60
            + time.get_minute(gs)
            - int(lesson_time[:2]) * 60
            - int(lesson_time[3:5])
            <= 120
        ):
            current_lesson["subject"] = lesson["subject"]
            current_lesson["room"] = lesson["room"]
            current_lesson["type"] = lesson["type"]
            break
    return current_lesson


def get_current_subject(gs):
    return get_current_lesson(gs)["subject"]


def get_current_type(gs):
    return get_current_lesson(gs)["type"]


def get_current_room(gs):
    return get_current_lesson(gs)["room"]
