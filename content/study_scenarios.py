from gameplay.api import schedule


def study_scenario():
    def check(gs):
        return schedule.get_current_lesson(gs)["subject"] is not None
    def study(gs):
