from engine import scenarios_api, gs_api
from interface import ui


# Пример простого сценария с двумя переходами.
# Эффекты могут быть не только выводом в консоль. Они могут и как-то менять gs
def rich_scenario():
    def check_rich(gs):
        return gs_api.get_stat(gs, "money") >= 20

    # Если функции не нужен gs, его можно не передавать как параметр
    # благодаря обертке call_with_gs в tools/utils: если gs нет в параметрах, он не будет передан
    def congratulations():
        ui.display("--- HI THERE! YOU ARE RICH! ---")

    def check_ultra_rich(gs):
        return gs_api.get_stat(gs, "money") >= 50

    def game_over(gs):
        ui.display("--- GAME OVER: YOU ARE TOO RICH FOR THIS WORLD ---")
        gs_api.set_flag(gs, "is_end", True)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_rich, congratulations),
            scenarios_api.base_transition(1, 2, check_ultra_rich, game_over),
        ]
    )


scenarios = [rich_scenario]
# Раскомментируйте эту строчку, чтобы добавить в игру демо-сценарий
