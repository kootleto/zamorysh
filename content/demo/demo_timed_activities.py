from engine import state_api, activities_api
from gameplay.activity_wrappers import timed_activity, single_tick_activity
from gameplay.api import stats
from interface import ui


# Пример активности с ограничением по времени
# Эта активность будет длиться всего пять тиков. Теперь не надо вручную прописывать счетчик!
def display_numbers_for_10_ticks(state=None):
    state = state_api.init_defaults(state, number=2)

    def tick_effect(gs):
        ui.display(state["number"])
        state["number"] *= 2
        stats.mod(gs, stats.KNOWLEDGE, 1)

    # Обратите внимание: мы передаем в обертку уже готовую активность,
    # а не ее кусочки вроде tick_effect или can_continue
    return timed_activity(
        activities_api.base_activity(tick_effect, name="отображать рандомные числа"),
        state,
        duration=5,
    )


# Пример однотиковой активности
# Однотиковые активности используют под капотом такой же счетчик, что и обычные timed_activities
# Хотя здесь мы не используем state внутри основной активности, он ей всё равно нужен для этого счетчика
def display_hello_world(state=None):
    def tick_effect():
        ui.display("Hello world!")

    return single_tick_activity(
        activities_api.base_activity(tick_effect, name="сказать привет"), state
    )


ACTIVITIES = [display_numbers_for_10_ticks, display_hello_world]
