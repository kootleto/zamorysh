import importlib
import pkgutil


def load_initial(package_name: str) -> dict[str, dict]:
    initial_data = {}

    package = importlib.import_module(package_name)

    def walk_modules(pkg):
        # Проходим по всем модулям в пакете
        for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
            full_module_name = f"{pkg.__name__}.{module_name}"
            module = importlib.import_module(full_module_name)

            if hasattr(module, "initial"):
                initial_data[full_module_name] = module.initial

            # Если модуль сам — пакет (то есть папка с __init__.py), проходим по нему рекурсивно
            if is_pkg:
                walk_modules(module)

    walk_modules(package)

    return initial_data
