import os

from dotenv import load_dotenv

load_dotenv()

# Если переменная в .env не задана, по умолчанию считаем, что это False
# Приводим все к нижнему регистру, чтобы распознавать любое написание
LOG_ENABLED = os.getenv("LOG_ENABLED", "False").lower() == "true"

# Доступные через escape-коды цвета.
# Escape-коды — последовательности символов, которые терминал распознает как команды, а не как текст
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

# Разные типы логов подсвечиваются разными цветами
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


def log(*message, log_type="log", color: str = None, sep=" "):
    """
    Если логирование включено, вывести в консоль сообщение в формате `[LOG_TYPE] message-sep-message-sep-...`

    Доступны цвета `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.
    По умолчанию `blue`.

    Для типов логов `ui`, `loader`, `config`, `intent`, `resolver`, `activity`, `scenario`, `tick`, `status`
    настроена подсветка уникальным цветом, если не указан иной.
    """
    message = sep.join(map(str, message))
    log_type = log_type.lower()
    if not LOG_ENABLED:
        return
    chosen_color = color or LOG_TYPE_COLORS.get(log_type, "blue")
    color_code = COLORS.get(chosen_color, COLORS["blue"])
    print(f"{color_code}[{log_type.upper()}] {message}{COLORS['reset']}")
