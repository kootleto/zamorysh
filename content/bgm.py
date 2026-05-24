from engine import scenarios_api
from gameplay.api import music


def start_bgm():
    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(
                0, 1, True, lambda gs: music.play(gs, "main_theme.wav")
            )
        ]
    )


SCENARIOS = [start_bgm]
