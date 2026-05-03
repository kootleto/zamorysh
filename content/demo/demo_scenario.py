from engine import scenarios_api, gs_api
from gameplay.api import stats
from interface import ui


# Пример простого сценария с двумя переходами.
# Эффекты могут быть не только выводом в консоль. Они могут и как-то менять gs
def rich_scenario():
    def check_rich(gs):
        return stats.get(gs, stats.MONEY) >= 20

    # Если функции не нужен gs, его можно не передавать как параметр
    # благодаря обертке call_with_gs в tools/utils: если gs нет в параметрах, он не будет передан
    def congratulations():
        ui.display("--- HI THERE! YOU ARE RICH! ---")

    def check_ultra_rich(gs):
        return stats.get(gs, stats.MONEY) >= 50

    def game_over(gs):
        ui.display("--- GAME OVER: YOU ARE TOO RICH FOR THIS WORLD ---")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_rich, congratulations),
            scenarios_api.base_transition(1, 2, check_ultra_rich, game_over),
        ]
    )


# SCENARIOS = [rich_scenario]
# Строчка закомментирована, потому что аналогичный сценарий уже есть в endings