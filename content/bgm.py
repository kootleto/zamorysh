from engine import scenarios_api
from interface import ui


def start_bgm():
    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 1, True, lambda: ui.play_music("1.wav"))]
    )


SCENARIOS = [start_bgm]
