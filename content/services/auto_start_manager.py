from engine import scenarios_api
from gameplay.process_auto_start import process_auto_start


def auto_start_manager(activity_definitions):
    """Запустить все активности с декоратором @with_auto_start."""

    def start(gs):
        process_auto_start(gs, activity_definitions)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 1, True, start)]
    )


SCENARIOS = [auto_start_manager]
