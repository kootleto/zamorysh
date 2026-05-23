from random import choice

from content import studying, wait, minigames
from engine import activities_api, scenarios_api
from gameplay.api import schedule, vitals, floors, stats
from interface import ui


def study_scenario(activity_definitions):
    def check(gs):
        return floors.get(gs, floors.CLASSROOM) == schedule.get_current_room(gs)

    async def study(gs):
        if schedule.get_current_type(gs) == "лекция":

            if choice([True, False]):
                ui.display("Вам очень понравилась тема лекции! Вы в предвкушении!")
                vitals.mod(gs, vitals.MENTAL, 5)
                activities_api.start_activity_by_definition(
                    gs, activity_definitions, studying.auto_study
                )
            else:
                ui.display(
                    "Тема лекции показалась вам скучной, и вам придётся слушать её с трудом..."
                )
                vitals.mod(gs, vitals.MENTAL, -5)

        else:
            ui.display("Семинар начинается...")
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
                print(
                    schedule.get_end_of_lesson(
                        schedule.get_current_lesson(gs)["hour"],
                        schedule.get_current_lesson(gs)["minute"],
                    )
                )
                # скип времени до конца пары
                activities_api.start_activity_by_definition(
                    gs,
                    activity_definitions,
                    wait.wait_until(
                        {
                            "hour": schedule.get_end_of_lesson(
                                schedule.get_current_lesson(gs)["hour"],
                                schedule.get_current_lesson(gs)["minute"],
                            )["hour"],
                            "minute": schedule.get_end_of_lesson(
                                schedule.get_current_lesson(gs)["hour"],
                                schedule.get_current_lesson(gs)["minute"],
                            )["minute"],
                        }
                    ),
                )
            else:
                activities_api.start_activity_by_definition(
                    gs, activity_definitions, studying.auto_study
                )

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check, study),
            scenarios_api.base_transition(1, 0, lambda gs: not check(gs), None),
        ]
    )


SCENARIOS = [study_scenario]
