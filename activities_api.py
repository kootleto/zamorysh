import inspect
import gs_api
import ui_api


def base_activity(
    tick_effect=lambda gs: None,
    can_continue=lambda gs: True,
    hold_required=False,
    is_stackable=False,
    param_space=lambda gs: None,
    name="default",
):
    # Храним все параметры активности как callable, потому что в композитных активностях
    # флаги могут меняться при смене подактивности
    if not callable(hold_required):
        hold_required = lambda v=hold_required: v
    if not callable(is_stackable):
        is_stackable = lambda v=is_stackable: v

    return {
        "tick_effect": tick_effect,
        "can_continue": can_continue,
        "hold_required": hold_required,
        "is_stackable": is_stackable,
        "param_space": param_space,
        "name": name,
    }


def apply_tick_effect(gs, activity):
    activity["tick_effect"](gs)


def check_can_continue(gs, activity):
    return activity["can_continue"](gs)


def check_hold_required(activity):
    return activity["hold_required"]()


def check_is_stackable(activity):
    return activity["is_stackable"]()


def get_param_space(gs, activity):
    return activity["param_space"](gs)


def get_activity_name(activity):
    return activity["name"]


def composite_activity(state, definitions, init_queue, name="default"):
    # Если state еще не инициализирован, проводим инициализацию
    # Мы можем создать активность на этапе перебора возможных активностей
    # В таком случае активность не прожила еще ни одного тика,
    # и она не может перейти к следующей подактивности,
    # потому что еще не выполнила предыдущую
    # Поэтому next_index инициализируется как None и превращается в 0 при успешной проверке can_continue
    def init():
        return {"queue": init_queue(), "current_index": 0, "next_index": None}

    state = init_fn(state, init)

    # В очереди хранятся не activities (это логика),
    # а entries, поэтому в качестве аргумента нам нужны definitions
    def get_current():
        return configure_activity(definitions, state["queue"][state["current_index"]])

    def get_next():
        return configure_activity(definitions, state["queue"][state["next_index"]])

    def tick_effect(gs):
        # На всякий случай повторная проверка: мы могли запустить активность,
        # и не выполняя can_continue
        if state["next_index"] is None:
            state["next_index"] = 0

        # Если надо перейти к следующей активности, переходим
        state["current_index"] = state["next_index"]
        current = get_current()
        # Выполняем эффект текущей подактивности
        apply_tick_effect(gs, current)

    def can_continue(gs):
        current = get_current()
        # Если мы больше не можем выполнять текущую подактивность, укажем, что в следующем тике
        # надо перейти к следующей
        if not check_can_continue(gs, current):
            if state["next_index"] is None:
                return False
            else:
                state["next_index"] += 1
        # Если мы можем продолжать текущую активность, установим индекс следующей в 0
        # Можно воспринимать это так: если мы можем прожить один тик в настоящем, мы имеем право смотреть в будущее
        if state["next_index"] is None:
            state["next_index"] = 0

        # Если очередь закончилась, композитная активность завершается
        if state["next_index"] >= len(state["queue"]):
            return False

        # Если подактивность, которая должна выполниться в следующем тике
        # (это может быть как текущая подактивность, так и следующая в очереди), не может выполняться в следующем тике,
        # композитная активность тоже завершается, потому что под композитной активностью мы понимаем,
        # что каждую подактивность мы должны выполнять хотя бы тик
        next_activity = get_next()
        return check_can_continue(gs, next_activity)

    def hold_required():
        current = get_current()
        return check_hold_required(current)

    def is_stackable():
        current = get_current()
        return check_is_stackable(current)

    return base_activity(
        tick_effect, can_continue, hold_required, is_stackable, name=name
    )


def override_activity(definition, **overrides):
    # Так можно изменить любое поле определения
    new_data = {**definition, **overrides}
    return base_activity(**new_data)


def add_activity_entry(gs, definitions, entry):
    # Конфигурируем логику, чтобы понять, стакается ли эта активность
    # Здесь же происходит инициализация state
    activity = configure_activity(definitions, entry)
    # Если не стакается, удаляем остальные не стакающиеся
    if not check_is_stackable(activity):
        gs["activity_entries"] = [
            entry
            for entry in gs["activity_entries"]
            if check_is_stackable(configure_activity(definitions, entry))
        ]
    entry_with_id = gs_api.with_id(gs, entry)
    gs["activity_entries"].append(entry_with_id)


def create_activity_entry(definition, param=None):
    activity_name = f"{definition.__module__}.{definition.__name__}"

    sig = inspect.signature(definition)
    state = None
    if "state" in sig.parameters:
        state = {}

    # Возвращаем entry. Для инициализации state потребуется создать саму activity,
    # поэтому это будет происходить не здесь, а при добавлении в gs
    return {
        "activity_name": activity_name,
        "param": param,
        "state": state,
    }


def configure_activity(definitions, entry):
    ui_api.log(f"Activity Entry: {entry}", log_type="config")

    # На основе данных и определения получаем логику для активности,
    # чье имя указано в этих данных

    definition = definitions[entry["activity_name"]]
    param = entry["param"]
    state = entry["state"]

    # Мы даем определению аргументы только в том случае, если они ему нужны
    # Чтобы понять, нужны ли аргументы, смотрим сигнатуру
    sig = inspect.signature(definition)

    kwargs = {}
    # Если в качестве параметра при создании записи передано None,
    # мы считаем это отсутствием параметра и, следовательно,
    # логика будет использовать не None, а параметр по умолчанию
    if "param" in sig.parameters and param is not None:
        kwargs["param"] = param
    # Передаем state из данных, если он нужен логике
    if "state" in sig.parameters:
        kwargs["state"] = state
    # Логике могут быть нужны определения, если она внутри себя вызывает другие активности
    # Например, это нужно любым композитным активностям
    if "definitions" in sig.parameters:
        kwargs["definitions"] = definitions

    return definition(**kwargs)


def init_defaults(state, **defaults):
    # Этот метод инициализации подходит, если изначальный state всегда одинаковый
    # Он принимает уже готовый словарь, а не логику инициализации
    if state is None:
        return defaults
    for key, val in defaults.items():
        state.setdefault(key, val)
    return state


def init_fn(state, fn):
    # Этот метод инициализации подходит, если изначальный state вычисляется на основе параметра
    # Он позволяет вызывать логику инициализации только в том случае, если state еще не инициализирован
    if state is None:
        return fn()
    elif state == {}:
        state.update(fn())
    return state


def get_allowed_activity_entries(gs, definitions):
    allowed_entries = []
    for definition in definitions.values():
        sig = inspect.signature(definition)
        kwargs = {}
        if "definitions" in sig.parameters:
            kwargs["definitions"] = definitions

        activity = definition(**kwargs)
        param_space = get_param_space(gs, activity)
        if param_space is None:
            if check_can_continue(gs, activity):
                entry = create_activity_entry(definition)
                allowed_entries.append(entry)
        else:
            for param in param_space:
                activity = definition(**kwargs, param=param)
                if check_can_continue(gs, activity):
                    entry = create_activity_entry(definition, param)
                    allowed_entries.append(entry)

    return allowed_entries
