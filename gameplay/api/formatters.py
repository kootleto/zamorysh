from datetime import datetime

RU_MONTHS = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]

RU_WEEKDAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]


def get_formatted_time(dt: datetime) -> str:
    return f"{dt.hour:02}:{dt.minute:02}"


def get_formatted_date(dt: datetime) -> str:
    return f"{RU_WEEKDAYS[dt.weekday()]}, {dt.day} {RU_MONTHS[dt.month - 1]} {dt.year}"
