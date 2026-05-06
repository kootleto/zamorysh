import asyncio
import sys

import keyboard

from config import SETTINGS
from engine import gs_api
from engine.schema import GameState, ActivityOptions
from gameplay.api import vitals, stats
from tools.logger import log


def init_ui():
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


async def prompt_activity(options: ActivityOptions) -> int:
    """
    Запросить у игрока выбор активности. Если он выберет активность, для которой требуется зажать клавишу,
    дождаться нажатия клавиши.

    Args:
        options: Информация об активностях в формате `(name, hold_required)`.

    Returns:
        Индекс выбранной активности.
    """

    display("Выберите активность")
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


def play_music(title: str):
    display(f"Играет музыка: {title}")


def stop_music():
    display("Музыка остановлена.")


def refresh_ui(gs: GameState, _vs, _options):
    display(
        f"Time: {gs_api.get_time(gs)}, Fatigue: {vitals.get(gs, vitals.FATIGUE)}, Money: {stats.get(gs, stats.MONEY)}"
    )
    display(
        f"Social: {stats.get(gs, stats.SOCIAL)}, Mental: {vitals.get(gs, vitals.MENTAL)}"
    )
    display(f"Knowledge: {stats.get(gs, stats.KNOWLEDGE)}")


def check_button_pressed():
    """Проверить, нажата ли клавиша Space."""
    return keyboard.is_pressed("space")


async def on_finish():
    display("--- GAME FINISHED ---")
    await prompt("Press Enter to exit")
