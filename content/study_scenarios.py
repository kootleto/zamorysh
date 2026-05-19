from engine import activities_api
from engine.activities_api import override_activity
from gameplay.api import schedule, vitals, floors
from random import choice
from interface import ui
from content import studying


def study_scenario(activity_definitions):
    def check(gs):
        return floors.get(gs, floors.CLASSROOM) == schedule.get_current_lesson(gs)["room"]
    def study(gs):
        if schedule.get_current_lesson(gs)["type"] == "лекция":
            activities_api.start_activity_by_definition(
                gs, activity_definitions, override_activity(studying.study(), hold_required=False)
            )
            if choice([True, False]):
                ui.display('Ура, тема интересная!')
                vitals.mod(gs, vitals.MENTAL, 5)
            else:
                ui.display('Эх, тема скучная...')
                vitals.mod(gs, vitals.MENTAL, -5)

        else:
            if choice([True, False]):
                # minigames (random / subject / choice ? )
            else:
                # studying is available    nothing???

