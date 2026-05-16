from gameplay.api import stats, schedule


def study():
    def tick_effect(gs):
        stats.mod(gs, schedule.get_current_lesson(gs), 1)

    def can_continue(gs):
        return
