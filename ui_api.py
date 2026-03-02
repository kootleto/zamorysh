import keyboard
import sys
from time import sleep
import gs_api

LOG_ENABLED = True

COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}

LOG_TYPE_COLORS = {
    "ui": "red",
    "loader": "black",
    "config": "magenta",
    "intent": "yellow",
    "resolver": "green",
    "scenario": "blue",
    "tick": "white",
}


def log(*message, log_type="log", color=None, sep=" "):
    message = sep.join(map(str, message))
    log_type = log_type.lower()
    if not LOG_ENABLED:
        return
    chosen_color = color or LOG_TYPE_COLORS.get(log_type.lower(), "blue")
    color_code = COLORS.get(chosen_color, COLORS["blue"])
    print(f"{color_code}[{log_type.upper()}] {message}{COLORS['reset']}")


def display(*message, sep=" "):
    message = sep.join(map(str, message))
    if LOG_ENABLED:
        log(message, log_type="ui")
    else:
        print(message)


def prompt(*message, sep=" "):
    message = sep.join(map(str, message))
    if LOG_ENABLED:
        log(message, log_type="ui")
        response = input()
    else:
        response = input(message)
    return response


def clear_input_buffer():
    if sys.platform.startswith("win"):
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()
    else:  # Unix / macOS
        import termios

        termios.tcflush(sys.stdin, termios.TCIFLUSH)


def check_key_pressed():
    return keyboard.is_pressed("space")


def handle_input(activities_ui_info):
    # принимает информацию в формате (name, hold_required)

    display("Выберите активность")
    for i in range(len(activities_ui_info)):
        display(i, activities_ui_info[i][0])
    clear_input_buffer()
    selected_index = int(prompt("Введите номер активности: "))
    if activities_ui_info[selected_index][1]:
        display("Зажмите пробел, чтобы начать")
        while not check_key_pressed():
            sleep(0.01)

    return selected_index


def show_stats(gs):
    display(
        f"Time: {gs_api.get_time(gs)}, Fatigue: {gs_api.get_vital(gs, "fatigue")}, Money: {gs_api.get_stat(gs, "money")}"
    )
