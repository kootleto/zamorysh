import importlib
import pkgutil

from config import settings
from tools.logger import log


def load_from_package(package_name: str, attr_name: str, skip=None) -> dict:
    """
    Вернуть словарь с парами `путь.к.файлу` (от `package_name` не включительно) - значение `attr_name`. Значение
    добавляется в словарь, если не выполняется условие `skip` (функция от `module_name`).
    """
    result = {}
    package = importlib.import_module(package_name)

    def walk_modules(pkg):
        for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
            if skip is not None and skip(module_name):
                continue

            full_name = f"{pkg.__name__}.{module_name}"
            module = importlib.import_module(full_name)

            if hasattr(module, attr_name):
                result[full_name] = getattr(module, attr_name)

            # Если модуль сам — пакет (то есть папка с __init__.py), проходим по нему рекурсивно
            if is_pkg:
                walk_modules(module)

    walk_modules(package)
    return result


def load_definitions(package_name: str) -> dict[str, dict]:
    """
    Args:
        package_name: Имя пакета, из которого требуется загрузить определения.

    Returns:
        Словарь с ключами `activities` и `scenarios`, по которым лежат словари с парами `"модуль.функция"` — `функция`.
    """

    skip = lambda name: "demo" in name and not settings.include_demo
    activities = load_from_package(package_name, "activities", skip)
    scenarios = load_from_package(package_name, "scenarios", skip)

    activity_definitions = {
        f"{k}.{f.__name__}": f for k, funcs in activities.items() for f in funcs
    }

    scenario_definitions = {
        f"{k}.{f.__name__}": f for k, funcs in scenarios.items() for f in funcs
    }

    log(
        f"Loaded activities: {", ".join(activity_definitions.keys())}",
        log_type="loader",
    )
    log(
        f"Loaded scenarios: {", ".join(scenario_definitions.keys())}",
        log_type="loader",
    )

    return {"activities": activity_definitions, "scenarios": scenario_definitions}
