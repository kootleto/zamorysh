from engine import scenarios_api
from gameplay.api import location, time, music, quests


def music_manager():
    def update_track(gs):
        if location.get_place(gs) == location.Place.HOME:
            music.play(gs, "bright.wav")
        elif (
            quests.is_active(gs, "keys")
            or location.get_place(gs) == location.Place.CLUB
        ):
            music.play(gs, "anxious.wav")
        elif (
            location.get_place(gs) == location.Place.OUTSIDE
            and not 7 <= time.get_hour(gs) <= 16
        ):
            music.play(gs, "dark.wav")
        else:
            music.play(gs, "main_theme.wav")

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, True, update_track)]
    )


SCENARIOS = [music_manager]
