import importlib
import pkgutil

import ui_api


def load_definitions(package_name):
    activity_definitions = {}
    scenario_definitions = {}

    package = importlib.import_module(package_name)

    def walk_modules(pkg):
        for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
            full_module_name = f"{pkg.__name__}.{module_name}"
            module = importlib.import_module(full_module_name)

            if hasattr(module, "activities"):
                for func in module.activities:
                    key = f"{full_module_name}.{func.__name__}"
                    activity_definitions[key] = func

            if hasattr(module, "scenarios"):
                for func in module.scenarios:
                    key = f"{full_module_name}.{func.__name__}"
                    scenario_definitions[key] = func

            if is_pkg:
                walk_modules(module)

    walk_modules(package)

    ui_api.log(
        f"Loaded activities: {", ".join(activity_definitions.keys())}",
        log_type="loader",
    )
    ui_api.log(
        f"Loaded scenarios: {", ".join(scenario_definitions.keys())}",
        log_type="loader",
    )

    return {"activities": activity_definitions, "scenarios": scenario_definitions}
