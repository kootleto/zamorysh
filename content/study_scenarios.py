from gameplay.api import schedule, vitals
from random import randint, choice
from interface import ui


def study_scenario():
    def check(gs):
        return schedule.get_current_lesson(gs)["subject"] is not None
    def study(gs):
        if schedule.get_current_lesson(gs)["type"] == "лекция":
            # активность стади
            if choice([True, False]):
                ui.display('Ура, тема интересная!')
                vitals.mod(gs, vitals.MENTAL, 5)
            else:
                ui.display('Эх, тема скучная...')
                vitals.mod(gs, vitals.MENTAL, -5)

        else:
            