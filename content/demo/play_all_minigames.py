from content import minigames
from engine import scenarios_api

games = [
    minigames.anagram,
    minigames.hangman,
    minigames.ugaiday_chislo,
    minigames.yazyki_i_semi,
    minigames.bulls_and_cows,
    minigames.kamen_nozhnitsy_bumaga,
]


def play_all_minigames():

    async def play_games():
        for game in games:
            await game()

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(
                0,
                1,
                True,
                play_games,
            )
        ]
    )


SCENARIOS = [play_all_minigames]
