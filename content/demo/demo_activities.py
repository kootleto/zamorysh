from engine import activities_api, state_api
from gameplay.api import vitals, stats


# Параметрами активности может быть что угодно.
# Вынос конкретных значений в параметры позволит легко менять их
# при использовании определений в других определениях.
# Не рекомендуется выносить в параметры базовые свойства активности вроде hold_required,
# потому что их легко можно переопределить с помощью override_activity
def work(fatigue_cost=1, earn_money=1):
    def tick_effect(gs):
        vitals.mod(gs, vitals.FATIGUE, +fatigue_cost)
        stats.mod(gs, stats.MONEY, +earn_money)

    def can_continue(gs):
        return vitals.get(gs, vitals.FATIGUE) < 10

    return activities_api.base_activity(tick_effect, can_continue, False, name="work")


# Параметров может и не быть
# Однострочные функции можно прописывать через lambda, то есть анонимные функции.
# Если операций больше одной, выносите в отдельную функцию внутри определения, как в примере выше
def rest():
    return activities_api.base_activity(
        lambda gs: vitals.mod(gs, vitals.FATIGUE, -1),
        True,
        True,
        name="rest",
    )


# Пример использования override_activity
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
        vitals.mod(gs, vitals.FATIGUE, +1)
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
        if amount <= stats.get(gs, stats.MONEY)
    ]
)
def waste_money(param, state=None):
    state = state_api.init_defaults(state, wasted=0)

    def tick_effect(gs):
        stats.mod(gs, stats.MONEY, -1)
        state["wasted"] += 1

    def can_continue(gs):
        return state["wasted"] < param and stats.get(gs, stats.MONEY) > 0

    return activities_api.base_activity(
        tick_effect, can_continue, name=f"waste {param} money"
    )


@activities_api.with_auto_start
def get_tired():
    def tick_effect(gs):
        vitals.mod(gs, vitals.SLEEPINESS, 1)

    return activities_api.base_activity(
        tick_effect, True, is_stackable=True, is_background=True
    )


activities = [
    work,
    rest,
    rest_hard,
    work_and_rest,
    cry,
    waste_money,
    get_tired,
]
