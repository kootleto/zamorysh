from gameplay.api import stats, productivity


def study():
    def tick_effect(gs):
        stats.mod(gs, stats.KNOWLEDGE, productivity.get(gs))

    def can_continue(gs):
        return
