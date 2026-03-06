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
    "scenario": "cyan",
    "activity": "cyan",
    "tick": "white",
    "status": "blue",
}


def log(*message, log_type="log", color=None, sep=" "):
    message = sep.join(map(str, message))
    log_type = log_type.lower()
    if not LOG_ENABLED:
        return
    chosen_color = color or LOG_TYPE_COLORS.get(log_type.lower(), "blue")
    color_code = COLORS.get(chosen_color, COLORS["blue"])
    print(f"{color_code}[{log_type.upper()}] {message}{COLORS['reset']}")
