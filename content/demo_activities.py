from engine import activities_api, gs_api

import random


def work(hold_required=False, fatigue_cost=1, earn_money=1, mental_cost=5):
    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +fatigue_cost)
        # gs_api.mod_vital(gs, "mental", -mental_cost)
        gs_api.mod_stat(gs, "money", +earn_money)

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") < 10

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required, name="work"
    )


def rest(hold_required=True):
    return activities_api.base_activity(
        lambda gs: gs_api.mod_vital(gs, "fatigue", -1),
        True,
        hold_required,
        name="rest",
    )


def pl(hold_required=False):

    def tick_effect(gs, money_loss=-1000, money_play=-1):
        if random.randint(1, 13) % 13 == 0:
            print("Онет!")
            gs_api.mod_stat(gs, "money", +money_loss)
        else:
            gs_api.mod_stat(gs, "money", +money_play)

    def can_continue(gs):
        return gs_api.get_stat(gs, "money") > 0

    return activities_api.base_activity(can_continue, name="pl")


def rest_hard():
    return activities_api.override_activity(rest(False), name="rest in peace")


def work_and_rest(definitions=None, state=None, hold_required=True):
    return activities_api.override_activity(
        activities_api.composite_activity(
            state,
            definitions,
            lambda: [
                activities_api.create_activity_entry(work),
                activities_api.create_activity_entry(rest),
            ],
            name="work then rest",
        ),
        hold_required=hold_required,
    )


def cry(state=None, hold_required=True):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +1)
        state["counter"] -= 1

    def can_continue(gs):
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required, name="cry"
    )


# if gs_api.get_time(gs) == 10:
# if random.randint(1, 3) % 3 == 0:
# gs_api.mod_vital(gs, "fatigue", +5.05)
# if random.randint(1, 3) % 3 == 1:
# gs_api.mod_vital(gs, "mental", +5.05)
# if random.randint(1, 3) % 3 == 2:
# gs_api.mod_stat(gs, "money", +5.05)


def play_games(hold_required=False, fatigue_cost=2, earn_money=-1, loose_money=-3):
    def tick_effect(gs):
        # if random.randint(1, 2) % 2 == 0:
        gs_api.mod_vital(
            gs, "money", +loose_money
        )  # вот так мы не делаем, короче идея в банкротстве
        gs_api.mod_vital(gs, "fatigue", +fatigue_cost)
        # else:
        # gs_api.mod_vital(gs, "fatigue", +fatigue_cost)
        # gs_api.mod_stat(gs, "money", +earn_money)

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") < 10

    return activities_api.base_activity(
        tick_effect, can_continue, hold_required, name="play_games"
    )


# def quote_kvest(hold_required=True, earn_money=1):
# print("Нужно угадать цитату")
# def tick_effect(gs):
# if
# gs_api.mod_stat(gs, "money", +earn_money)
# print("")


# return activities_api.base_activity(tick_effect, hold_required, name="quote_kvest")
def random_event(
    state=None,
    hold_required=False,
    # earn_money=random.randint(1, 2),
    # fatigue_cost=random.randint(1, 5),
    earn_money=1,
    fatigue_cost=1,
):
    def tick_effect(gs):
        if random.randint(1, 3) % 3 == 0:
            print("Вы нашли на дороге 5 рублей! Поздравляем!")
            gs_api.mod_vital(gs, "money", +earn_money)
        if random.randint(1, 3) % 3 == 1:
            print(
                "Онет! Вы врезались в Ландера, пока опаздывали на дискру. Он расстроен."
            )
            gs_api.mod_vital(gs, "money", -fatigue_cost)
        else:
            print("Вы проспорили деньги на свой накоп по дискре (он меньше 3)")
            gs_api.mod_vital(gs, "money", +earn_money)

    return activities_api.base_activity(hold_required, tick_effect, name="random_event")


activities = [work, rest, rest_hard, work_and_rest, cry, random_event]
# Раскомментируйте эту строчку, чтобы добавить в игру демо-активности
