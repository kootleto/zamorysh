from engine import activities_api, gs_api, state_api


# Параметрами активности может быть что угодно.
# Вынос конкретных значений в параметры позволит легко менять их
# при использовании определений в другие определения.
# Не рекомендуется выносить в параметры базовые свойства активности вроде hold_required,
# потому что их легко можно переопределить с помощью override_activity
def work(fatigue_cost=1, earn_money=1):
    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +fatigue_cost)
        gs_api.mod_stat(gs, "money", +earn_money)

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") < 10

    return activities_api.base_activity(tick_effect, can_continue, False, name="work")


# Параметров может и не быть
# Однострочные функции можно прописывать через lambda, то есть анонимные функции
# Если операций больше одной, выносите в отдельную функцию внутри определения, как в примере выше
def rest():
    return activities_api.base_activity(
        lambda gs: gs_api.mod_vital(gs, "fatigue", -1),
        True,
        True,
        name="rest",
    )


# Пример использования override_activity
def rest_hard():
    return activities_api.override_activity(
        rest(), hold_required=False, name="rest in peace"
    )


# Пример композитной активности.
# Здесь мы используем override, чтобы изменить поведение hold_required. По умолчанию это свойство
# равно соответствующему свойству текущей подактивности, но мы хотим,
# чтобы на протяжении всей композитной активности надо было удерживать клавишу
def work_and_rest(definitions=None, state=None):
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


# Пример использования state.
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


def drink_coffee(state=None, hold_required=True):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "sleepiness", -1)
        gs_api.mod_vital(gs, "mental", -1)
        state["counter"] -= 1

    def can_continue(gs):
        return gs_api.get_vital(gs, "fatigue") > 0

    return activities_api.base_activity(
        tick_effect,
        can_continue,
        hold_required,
        name="drink coffee",
    )


def socialize(hold_required=False, earn_fatigue=1, earn_mental=1, state=None):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_vital(gs, "fatigue", +earn_fatigue)
        gs_api.mod_vital(gs, "mental", +earn_mental)
        state["counter"] -= 1

    def can_continue(gs):
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        hold_required,
        can_continue,
        name="socialize",
    )


def listen_to_music(hold_required=False, earn_mental=-5, earn_sleepiness=1, state=None):
    state = activities_api.init_defaults(state, counter=10)

    def tick_effect(gs):
        gs_api.mod_stat(gs, "mental", +earn_mental)
        gs_api.mod_stat(gs, "sleepiness", +earn_sleepiness)
        state["counter"] -= 1

    def can_continue(gs):
        return state["counter"] > 0

    return activities_api.base_activity(
        tick_effect,
        hold_required,
        can_continue,
        name="listen to music",
    )


activities = [
    work,
    rest,
    rest_hard,
    work_and_rest,
    cry,
    socialize,
    drink_coffee,
    listen_to_music,
]
# Раскомментируйте эту строчку, чтобы добавить в игру демо-активности
