import sys
from time import sleep

import keyboard

from config import settings
from engine import gs_api
from gameplay.api import vitals, stats
from tools.logger import log


def display(*message, sep: str = " "):
    """
    Вывести в консоль сообщение с разделителем sep. Если логирование включено, вывести как лог типа UI.

    Аналог стандартной функции `print`.
    """
    message = sep.join(map(str, message))
    if settings.log_enabled:
        log(message, log_type="ui")
    else:
        print(message)


def prompt(*message, sep: str = " ") -> str:
    """
    Вывести в консоль сообщение с разделителем sep и вернуть ответ игрока.
    Если логирование включено, вывести как лог типа UI.

    Аналог стандартной функции `input`.
    """

    message = sep.join(map(str, message))
    if settings.log_enabled:
        log(message, log_type="ui")
        response = input()
    else:
        response = input(message)
    return response


def clear_input_buffer():
    """
    Очистить набранный пользователем текст.
    """
    # Windows
    if sys.platform.startswith("win"):
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()
    # Unix / macOS
    else:
        import termios

        termios.tcflush(sys.stdin, termios.TCIFLUSH)


def check_key_pressed():
    """Проверить, нажата ли клавиша Space."""
    return keyboard.is_pressed("space")


def handle_input(activities_ui_info: list[tuple]) -> int:
    """
    Запросить у игрока выбор активности. Если он выберет активность, для которой требуется зажать клавишу,
    дождаться нажатия клавиши.

    Args:
        activities_ui_info: Информация об активностях в формате `(name, hold_required)`.

    Returns:
        Индекс выбранной активности.
    """

    display("Выберите активность")
    for i in range(len(activities_ui_info)):
        display(i, activities_ui_info[i][0])

    # Если пользователю ранее надо было зажимать кнопку,
    # без очистки буфера терминал интерпретирует это как набор текста
    clear_input_buffer()
    selected_index = int(prompt("Введите номер активности: "))

    # Дождаться нажатия, если необходимо
    if activities_ui_info[selected_index][1]:
        display("Зажмите пробел, чтобы начать")
        while not check_key_pressed():
            sleep(0.01)

    return selected_index


def show_stats(gs):
    display(
        f"Time: {gs_api.get_time(gs)}, Fatigue: {vitals.get(gs, vitals.fatigue)}, Money: {stats.get(gs, stats.money)}"
    )
    display(
        f"Social: {stats.get(gs, stats.social)}, Mental: {vitals.get(gs, vitals.mental)}"
    )
    display(f"Knowledge: {stats.get(gs, stats.knowledge)}")
