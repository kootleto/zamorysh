from engine import scenarios_api
from gameplay.api import location, time, quests, stats, vitals
from gameplay.api.location import X, Y, Place
from interface import ui


def bird_quest():

    def start(gs):
        return (
            location.get(gs, X) == 59
            and location.get(gs, Y) == 0
            and time.get_day(gs) == time.START_DATETIME.day + 4
        )

    def start_eff(gs):
        quests.set_status(gs, "bird", quests.Status.ACTIVE)
        ui.display(
            "Вы видите на дереве перед басмачом птицу. Она выглядит очень грустной. "
            "\n Вам кажется, что нужно ее покормить..."
            "\n Вы помните, что видели где-то у парка ларек, в котором продавалось зерно."
        )

    def check_buy(gs):
        return (
            location.get(gs, location.X) == 1
            and location.get(gs, location.Y) == 5
            and stats.get(gs, stats.MONEY) > 3
        )

    def check_not_buy(gs):
        return (
            location.get(gs, location.X) == 1
            and location.get(gs, location.Y) == 5
            and stats.get(gs, stats.MONEY) <= 3
        )

    def eff_buy(gs):
        stats.mod(gs, stats.MONEY, -4)
        ui.display("Вы купили зерен для птицы! Нужно вернуться и накормить её!")

    def eff_not_buy(gs):
        ui.display("Вам не хватило денег на зерно... Возвращайтесь с деньгами.")

    def check_no_bird(gs):
        return location.get(gs, X) == 59 and location.get(gs, Y) == 0

    def eff_no_bird(gs):
        ui.display(
            "Ох, похоже, птица улетела. Вам нужно найти ее, ведь вы купили ей зерно!"
            "\n Наверное, она в каком-то месте, где есть деревья..."
        )

    def check_found_bird(gs):
        return location.get_place(gs) == Place.PARK

    def found_bird(gs):
        ui.display(
            "Птица медленно ходит вокруг скамейки в парке... Похоже, она ждала вас."
            "\n Вы медленно насыпаете зерно для птицы, и она с удовольствием ест его!"
        )
        vitals.mod(gs, vitals.MENTAL, +5)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, "saw_bird", start, start_eff),
            scenarios_api.base_transition(
                "saw_bird", "bought_seeds", check_buy, eff_buy
            ),
            scenarios_api.base_transition(
                "saw_bird", "didnt_buy", check_not_buy, eff_not_buy
            ),
            scenarios_api.base_transition(
                "didnt_buy", "bought_seeds", check_buy, eff_buy
            ),
            scenarios_api.base_transition(
                "bought_seeds", "no_bird", check_no_bird, eff_no_bird
            ),
            scenarios_api.base_transition(
                "no_bird", "found_bird", check_found_bird, found_bird
            ),
        ]
    )


SCENARIOS = [bird_quest]
