import importlib
import os
import pkgutil

from dotenv import load_dotenv

from tools.logger import log

load_dotenv()
INCLUDE_DEMO = os.getenv("INCLUDE_DEMO", "False").lower() == "true"


def load_definitions(package_name: str) -> dict[str, dict]:
    """
    Args:
        package_name: Имя пакета, из которого требуется загрузить определения.

    Returns:
        Словарь с ключами `activities` и `scenarios`, по которым лежат словари с парами `"модуль.функция"` — `функция`.
    """
    activity_definitions = {}
    scenario_definitions = {}

    package = importlib.import_module(package_name)

    def walk_modules(pkg):
        # Проходим по всем модулям в пакете
        for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
            full_module_name = f"{pkg.__name__}.{module_name}"
            module = importlib.import_module(full_module_name)

            if "demo" in module_name and not INCLUDE_DEMO:
                continue

            # Если в модуле есть списки activities или scenarios — кладем их содержимое
            # в соответствующие словари

            if hasattr(module, "activities"):
                for func in module.activities:
                    key = f"{full_module_name}.{func.__name__}"
                    activity_definitions[key] = func

            if hasattr(module, "scenarios"):
                for func in module.scenarios:
                    key = f"{full_module_name}.{func.__name__}"
                    scenario_definitions[key] = func

            # Если модуль сам — пакет (то есть папка с __init__.py), проходим по нему рекурсивно
            if is_pkg:
                walk_modules(module)

    walk_modules(package)

    log(
        f"Loaded activities: {", ".join(activity_definitions.keys())}",
        log_type="loader",
    )
    log(
        f"Loaded scenarios: {", ".join(scenario_definitions.keys())}",
        log_type="loader",
    )

    return {"activities": activity_definitions, "scenarios": scenario_definitions}
