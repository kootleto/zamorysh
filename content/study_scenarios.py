from random import choice

import minigames
from content import studying
from engine import activities_api, scenarios_api
from engine.activities_api import override_activity
from gameplay.api import schedule, vitals, floors, stats
from interface import ui


def auto_study():
    return override_activity(studying.study(), hold_required=False)


def study_scenario(activity_definitions):
    def check(gs):
        return floors.get(gs, floors.CLASSROOM) == schedule.get_current_room(gs)

    async def study(gs):
        if schedule.get_current_type(gs) == "лекция":
            activities_api.start_activity_by_definition(
                gs, activity_definitions, auto_study
            )
            if choice([True, False]):
                ui.display(
                    "Ура, вам очень понравилась тема, и лекция пролетела незаметно!"
                )
                vitals.mod(gs, vitals.MENTAL, 5)
            else:
                ui.display(
                    "Эх, тема показалась вам скучной, и вы с трудом дослушали её до конца..."
                )
                vitals.mod(gs, vitals.MENTAL, -5)

        else:
            if choice([True, False]):
                minigame = choice(
                    [
                        minigames.anagram,
                        minigames.hangman,
                        minigames.ugaiday_chislo,
                        minigames.yazyki_i_semi,
                        minigames.bulls_and_cows,
                        minigames.kamen_nozhnitsy_bumaga,
                    ]
                )
                result = await minigame()
                if result:
                    vitals.mod(gs, vitals.MENTAL, 5)
                    stats.mod(gs, stats.KNOWLEDGE, 10)
                else:
                    vitals.mod(gs, vitals.MENTAL, -5)
                    stats.mod(gs, stats.KNOWLEDGE, 15)
                vitals.mod(gs, vitals.FATIGUE, 10)
                # TODO: сделать скип времени до конца пары

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check, study),
            scenarios_api.base_transition(1, 0, lambda gs: not check(gs), None),
        ]
    )


# SCENARIOS = [study_scenario]
