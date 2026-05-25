from enum import StrEnum

from gameplay.api import time


class Subject(StrEnum):
    ENGLISH = "Английский"
    DIVERSITY = "Языковое разнообразие"
    LATIN = "Латынь"
    LANGUAGE = "Язык"
    MATH = "Дискретная математика"
    OCS = "Старославянский"
    INTRO = "Введение в лингвистику"
    LINGDATA = "Лингвистические данные"
    DIGLIT = "Цифровая грамотность"
    ELECTIVE = "НИС"
    HISTORY = "История"


WEEK_SCHEDULE = {
    time.Weekday.MONDAY: {
        "13:00": {"subject": Subject.ENGLISH, "room": 205, "type": "семинар"}
    },
    time.Weekday.TUESDAY: {
        "11:10": {"subject": Subject.DIVERSITY, "room": 511, "type": "лекция"},
        "13:00": {"subject": Subject.LATIN, "room": 506, "type": "семинар"},
        "14:40": {"subject": Subject.LANGUAGE, "room": 516, "type": "семинар"},
    },
    time.Weekday.WEDNESDAY: {
        "09:30": {"subject": Subject.MATH, "room": 501, "type": "лекция"},
        "11:10": {"subject": Subject.OCS, "room": 507, "type": "семинар"},
        "12:30": {"subject": Subject.DIVERSITY, "room": 316, "type": "семинар"},
        "14:40": {"subject": Subject.MATH, "room": 505, "type": "семинар"},
        "16:20": {"subject": Subject.INTRO, "room": 507, "type": "семинар"},
    },
    time.Weekday.THURSDAY: {
        "13:00": {"subject": Subject.LINGDATA, "room": 501, "type": "лекция"},
        "14:40": {"subject": Subject.LATIN, "room": 506, "type": "семинар"},
        "16:20": {"subject": Subject.LINGDATA, "room": 401, "type": "семинар"},
    },
    time.Weekday.FRIDAY: {
        "11:10": {"subject": Subject.DIGLIT, "room": 509, "type": "семинар"},
        "13:00": {"subject": Subject.ELECTIVE, "room": 505, "type": "семинар"},
        "14:40": {"subject": Subject.LANGUAGE, "room": 516, "type": "семинар"},
        "16:20": {"subject": Subject.INTRO, "room": 501, "type": "лекция"},
    },
    time.Weekday.SATURDAY: {
        "11:10": {"subject": Subject.HISTORY, "room": 502, "type": "семинар"}
    },
}


def get_week_schedule():
    return WEEK_SCHEDULE


def get_day_schedule(weekday):
    if weekday == time.Weekday.SUNDAY:
        return {}
    else:
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
            <= 80
        ):
            current_lesson["hour"] = int(lesson_time[:2])
            current_lesson["minute"] = int(lesson_time[3:5])
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


def get_end_of_lesson(start_hour, start_minute):
    end_hour = (start_hour * 60 + start_minute + 80) // 60
    end_minute = (start_hour * 60 + start_minute + 80) % 60
    return {"hour": end_hour, "minute": end_minute}
