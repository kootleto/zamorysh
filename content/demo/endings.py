from engine import scenarios_api, gs_api
from gameplay.api import stats, vitals
from interface import ui


def rich_scenario():
    def check_rich(gs):
        return stats.get(gs, stats.MONEY) >= 50

    def congratulations():
        ui.display("--- HI THERE! YOU ARE RICH! ---")

    def check_ultra_rich(gs):
        return stats.get(gs, stats.MONEY) >= 100

    def game_over(gs):
        ui.display("GAME OVER: YOU ARE TOO RICH FOR A UNIVERSITY STUDENT")
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_rich, congratulations),
            scenarios_api.base_transition(1, 2, check_ultra_rich, game_over),
        ]
    )


def breakdown_scenario():
    def check_kukukha(gs):
        return vitals.get(gs, vitals.MENTAL) <= 20

    def mental_warning():
        ui.display("--- ...ARE YOU OKAY, BUDDY? YOU'RE ACTING WEIRD. ---")

    def check_bad_kukukha(gs):
        return vitals.get(gs, vitals.MENTAL) <= 0

    def mental_game_over(gs):
        ui.display(
            "GAME OVER: YOU HAD A MENTAL BREAKDOWN AND DROPPED OUT OF UNIVERSITY. YOU SHOULD'VE PAID MORE ATTENTION TO YOUR MENTAL HEALTH."
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_kukukha, mental_warning),
            scenarios_api.base_transition(1, 2, check_bad_kukukha, mental_game_over),
        ]
    )


def eternalsleep_scenario():
    def check_sleep(gs):
        return vitals.get(gs, vitals.SLEEPINESS) >= 80

    def sleepwarning():
        ui.display("--- YOU COULD REALLY USE SOME SLEEP NOW. ---")

    def check_bad_sleep(gs):
        return vitals.get(gs, vitals.SLEEPINESS) >= 100

    def sleep_game_over(gs):
        ui.display(
            "GAME OVER: AFTER DAYS OF SLEEP DEPRIVATION, YOU FINALLY FELL ASLEEP. YOU ONLY MANAGED TO WAKE UP AFTER THE SEMESTER HAS ENDED."
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_sleep, sleepwarning),
            scenarios_api.base_transition(1, 2, check_bad_sleep, sleep_game_over),
        ]
    )


def verytired_scenario():
    def check_tired(gs):
        return vitals.get(gs, vitals.FATIGUE) >= 80

    def tiredwarning():
        ui.display("--- YOU FEEL VERY TIRED. ---")

    def check_very_tired(gs):
        return vitals.get(gs, vitals.FATIGUE) >= 100

    def fatigue_game_over(gs):
        ui.display(
            "GAME OVER: YOU BECAME SO EXHAUSTED YOU COULDN'T DO ANYTHING AT ALL ANYMORE."
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_tired, tiredwarning),
            scenarios_api.base_transition(1, 2, check_very_tired, fatigue_game_over),
        ]
    )


def win_scenario():

    def check_time(gs):
        return gs_api.get_time(gs) >= 1000

    def successfully_survived(gs):
        ui.display(
            "CONGRATULATIONS! YOU HAVE SURVIVED YOUR FIRST SEMESTER. GOOD LUCK WITH GETTING THROUGH 7 MORE..."
        )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 1, check_time, successfully_survived)]
    )


SCENARIOS = [
    rich_scenario,
    breakdown_scenario,
    eternalsleep_scenario,
    verytired_scenario,
    win_scenario,
]
