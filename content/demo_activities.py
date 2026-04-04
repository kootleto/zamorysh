from engine import activities_api, gs_api, state_api

import random

# Параметрами активности может быть что угодно.
# Вынос конкретных значений в параметры позволит легко менять их
# при использовании определений в других определениях.
# Не рекомендуется выносить в параметры базовые свойства активности вроде hold_required,
# потому что их легко можно переопределить с помощью override_activity
def work(fatigue_cost=1, earn_money=1):
    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +fatigue_cost)
        # gs_api.mod_vital(gs, "mental", -mental_cost)
        gs_api.mod_stat(gs, "money", +earn_money)

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") < 10

    return activities_api.base_activity(tick_effect, can_continue, False, name="work")


# Параметров может и не быть
# Однострочные функции можно прописывать через lambda, то есть анонимные функции.
# Если операций больше одной, выносите в отдельную функцию внутри определения, как в примере выше
def rest():
    return activities_api.base_activity(
        lambda gs: gs_api.mod_vital(gs, "fatigue", -1),
        True,
        True,
        name="rest",
    )


# Пример использования override_activity
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
    return activities_api.override_activity(
        rest(), hold_required=False, name="rest in peace"
    )


# Пример композитной активности
# Здесь мы используем override, чтобы изменить поведение hold_required. По умолчанию это свойство
# равно соответствующему свойству текущей подактивности, но мы хотим,
# чтобы на протяжении всей композитной активности надо было удерживать клавишу
def work_and_rest(definitions, state=None):
    return activities_api.override_activity(
        activities_api.composite_activity(
            definitions,
            lambda: [
                activities_api.create_activity_entry(work),
                activities_api.create_activity_entry(rest),
            ],
            state,
            name="work then rest",
        ),
        hold_required=True,
    )


# Пример использования state
# По умолчанию state, если он есть, должен быть None. Не забывайте прописывать это!
# Это значит, что, если мы не передадим в определение никакой словарь, определение не сломается,
# а просто увидит, что ему ничего не передано, и создаст словарь самостоятельно,
# не изменяя никакие данные по ссылке
def cry(state=None):
    # Присваивание (state =) имеет смысл только в том случае, если state=None
    # Python хранит словари как ссылки, а init_defaults мутирует словарь, так что в остальных случаях
    # достаточно вызова функции. Но переприсваивание не повредит, а код так становится короче
    state = state_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +1)
        state["counter"] -= 1

    # Если функции не нужен gs, его можно не передавать как параметр
    # благодаря обертке call_with_gs в tools/utils: если gs нет в параметрах, он не будет передан
    def can_continue():
        return state["counter"] > 0

    return activities_api.base_activity(tick_effect, can_continue, True, name="cry")


# Пример активности с параметром
# Сначала мы указываем область параметра - по этой области будет проходить
# get_allowed_activity_entries и проверять для каждого параметра из этой области, можно ли начать такую активность.
# Область параметра мы указываем в обертке для декоратора with_param_space. Эта обертка возвращает уже сам декоратор,
# который в качестве аргумента принимает определение (в данном случае waste_money), присваивает ему указанную
# область параметра в качестве атрибута и возвращает обратно
@activities_api.with_param_space(
    lambda gs: [
        # list comprehension: из 5, 10 и 15 выбираем то, что не больше, чем у нас есть денег
        amount
        for amount in [5, 10, 15]
        if amount <= gs_api.get_stat(gs, "money")
    ]
)
def waste_money(param, state=None):
    state = state_api.init_defaults(state, wasted=0)

    def tick_effect(gs):
        gs_api.mod_stat(gs, "money", -1)
        state["wasted"] += 1

    def can_continue(gs):
        return state["wasted"] < param and gs_api.get_stat(gs, "money") > 0

    return activities_api.base_activity(
        tick_effect, can_continue, name=f"waste {param} money"
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
activities = [work, rest, rest_hard, work_and_rest, cry, waste_money]
# Раскомментируйте эту строчку, чтобы добавить в игру демо-активности
