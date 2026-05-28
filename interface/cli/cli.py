import asyncio
import sys

import keyboard

from config import SETTINGS
from engine.schema import GameState, ActivityOptions
from gameplay.api import vitals, stats, time, formatters
from tools.logger import log


def init_ui(_vs_path):
    return {}


def display(*message, sep: str = " "):
    """
    Вывести в консоль сообщение с разделителем sep. Если логирование включено, вывести как лог типа UI.

    Аналог стандартной функции `print`.
    """
    message = sep.join(map(str, message))
    if SETTINGS.log_enabled:
        log(message, log_type="ui")
    else:
        print(message)


def display_at(gs, *message, sep: str = " "):
    time_str = formatters.get_formatted_time(time.get_datetime(gs))
    message = sep.join(map(str, message))
    display(f"[{time_str}]", message)


# DEPRECATED
async def prompt(*message, sep: str = " ") -> str:
    """
    Вывести в консоль сообщение с разделителем sep и вернуть ответ игрока.
    Если логирование включено, вывести как лог типа UI.

    Аналог стандартной функции `input`.
    """

    message = sep.join(map(str, message))
    if SETTINGS.log_enabled:
        log(message, log_type="ui")
        response = input()
    else:
        response = input(message)
    return response


def _clear_input_buffer():
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


async def ask_option(options, message, _submit_required, _submit_message, cols):
    display(message)
    choice = ""
    for i, option in enumerate(options):
        choice += f"{i} {option}\t"
        if (i + 1) % cols == 0:
            choice += "\n"
    display(choice)
    return options[int(await prompt())]


async def prompt_activity(options: ActivityOptions) -> int:
    """
    Запросить у игрока выбор активности. Если он выберет активность, для которой требуется зажать клавишу,
    дождаться нажатия клавиши.

    Args:
        options: Информация об активностях в формате `(name, hold_required)`.

    Returns:
        Индекс выбранной активности.
    """

    display("Выберите действие")
    for i in range(len(options)):
        display(i, options[i]["label"])

    # Если пользователю ранее надо было зажимать кнопку,
    # без очистки буфера терминал интерпретирует это как набор текста
    _clear_input_buffer()
    selected_index = int(await prompt("Введите номер активности: "))

    # Дождаться нажатия, если необходимо
    if options[selected_index]["hold_required"]:
        display("Зажмите пробел, чтобы начать")
        while not check_button_pressed():
            await asyncio.sleep(0.001)

    return selected_index


def refresh_ui(gs: GameState, _options):
    display(
        f"Time: {formatters.get_formatted_time(time.get_datetime(gs))}, Fatigue: {vitals.get(gs, vitals.FATIGUE)}, Money: {stats.get(gs, stats.MONEY)}, "
        f"Social: {stats.get(gs, stats.SOCIAL)}, Mental: {vitals.get(gs, vitals.MENTAL)}, "
        f"Knowledge: {stats.get(gs, stats.KNOWLEDGE)}"
    )


def check_button_pressed():
    """Проверить, нажата ли клавиша Space."""

    return keyboard.is_pressed("space")


async def on_finish():
    display("--- GAME FINISHED ---")
    await prompt("Press Enter to exit")
