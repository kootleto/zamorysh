import gs_api
import scenarios_api
import ui_api


def rich_scenario():
    def check_rich(gs):
        return gs_api.get_stat(gs, "money") >= 20

    def congratulations(gs):
        ui_api.display("--- HI THERE! YOU ARE RICH! ---")

    def check_ultra_rich(gs):
        return gs_api.get_stat(gs, "money") >= 50

    def game_over(gs):
        ui_api.display("--- GAME OVER: YOU ARE TOO RICH FOR THIS WORLD ---")
        gs_api.set_flag(gs, "is_end", True)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_rich, congratulations),
            scenarios_api.base_transition(1, 2, check_ultra_rich, game_over),
        ]
    )


scenarios = [rich_scenario]
