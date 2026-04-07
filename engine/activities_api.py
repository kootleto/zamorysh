from inspect import signature
from typing import Callable, Iterable

from tools.logger import log
from tools.utils import call_with_gs
from . import gs_api
from . import state_api


def base_activity(
    tick_effect: Callable[[dict], None] | Callable[[], None] = lambda gs: None,
    can_continue: bool | Callable[[dict], bool] | Callable[[], bool] = lambda gs: True,
    hold_required: bool | Callable[[], bool] = False,
    is_stackable: bool | Callable[[], bool] = False,
    is_background: bool | Callable[[], bool] = False,
    name: str = "default",
) -> dict:
    """
    Создать активность с указанными свойствами и методами.

    Базовое определение (definition) активности.

    Args:
        tick_effect: Функция, которая выполняется каждый тик, пока активность запущена. Принимает `gs`.
        can_continue: Условие, при котором активность может выполняться в следующем тике. Принимает `gs`.
        hold_required: Нужно ли игроку удерживать клавишу для продолжения активности.
        is_stackable: При добавлении не-stackable в список текущих активностей
            из него удаляются все остальные не-stackable.
        is_background: Фоновая активность не предлагается игроку при выборе, и, если запущены только фоновые активности,
            игрок должен выбрать любую не фоновую (из возможных), чтобы игра продолжилась.
        name: Название активности для отображения в UI.

    Returns:
        Активность, то есть словарь, который следует передавать в функции API,
        чтобы вызвать методы активности или узнать ее свойства.

    """
    # Все параметры активности, кроме имени и param_space,
    # хранятся как callable, чтобы их можно было изменять динамически
    # Например, в композитных активностях hold_required и is_stackable совпадают с соответствующими свойствами
    # текущей подактивности
    if not callable(can_continue):
        can_continue = lambda v=can_continue: v
    if not callable(hold_required):
        hold_required = lambda v=hold_required: v
    if not callable(is_stackable):
        is_stackable = lambda v=is_stackable: v
    if not callable(is_background):
        is_background = lambda v=is_background: v

    return {
        "tick_effect": tick_effect,
        "can_continue": can_continue,
        "hold_required": hold_required,
        "is_stackable": is_stackable,
        "is_background": is_background,
        "name": name,
    }


def apply_tick_effect(gs, activity):
    call_with_gs(gs, activity["tick_effect"])


def check_can_continue(gs, activity):
    return call_with_gs(gs, activity["can_continue"])


def check_hold_required(activity):
    return activity["hold_required"]()


def check_is_stackable(activity):
    return activity["is_stackable"]()


def check_is_background(activity):
    return activity["is_background"]()


def get_activity_name(activity):
    return activity["name"]


# Это обертка над декоратором: у нее есть параметр param_space, и его может использовать сам декоратор.
# Она возвращает декоратор
def with_param_space(param_space: Iterable | Callable[[dict], Iterable]):
    # Это декоратор, то есть обертка над definition. Он принимает definition,
    # присваивает ему указанную область параметра в качестве атрибута
    # и возвращает definition
    def wrapper(definition):
        # Функции в Python - это объекты, и им можно присваивать атрибуты. Мы используем это,
        # чтобы узнать область параметра можно было из определения активности, не создавая саму активность
        # (ведь для создания активности уже нужно будет указать параметр)
        definition.param_space = param_space
        return definition

    return wrapper


def get_param_space(gs, definition):
    # Атрибут функции можно узнать, не вызывая ее, чем мы и пользуемся
    param_space = getattr(definition, "param_space", None)

    # param_space может быть как функцией, которая принимает gs и возвращает Iterable, так и просто Iterable
    # (то есть чем-то, по чему можно пройтись в цикле for)
    if callable(param_space):
        return call_with_gs(gs, param_space)
    else:
        return param_space


# Это декоратор. Он делает то же, что и with_param_space: присваивает объекту атрибут
def with_auto_start(definition):
    """Запустить активность в начале игры."""
    definition.auto_start = True
    return definition


def check_auto_start(definition):
    # Если такого атрибута присвоено не было, то автозапуск нам не нужен
    return getattr(definition, "auto_start", False)


def override_activity(activity: dict, **overrides) -> dict:
    """
    Заменить любые элементы словаря активности: `tick_effect`, `can_continue`, `hold_required`,
    `is_stackable`, `param_space`, `name`.

    Это позволяет заменять отдельные элементы определений, создавая на их основе новое определение,
    и не хранить все свойства и методы активности в аргументах.
    Например, по умолчанию параметр `hold_required` композитной активности равен `hold_required` текущей подактивности.
    Сделав override с `hold_required = False`, мы сможем изменить ее поведение.
    """
    new_data = {**activity, **overrides}
    return base_activity(**new_data)


def create_activity_entry(definition, param=None) -> dict:
    """
    Создать запись активности (entry).

    Это словарь, в котором хранятся определение (definition) активности, параметр (если есть) и
    локальное состояние активности (если есть).
    """

    # Получаем имя функции-определения в формате модуль.имя (по этому ключу в definitions хранится сама функция)
    activity_name = f"{definition.__module__}.{definition.__name__}"

    # Если активности нужен state, создаем пустой словарь. При первом создании активности
    # пройдет инициализация, и в этом словаре окажутся значения по умолчанию.
    # Иначе явно показываем, что state активности не нужен.
    # Чтобы понять, нужен ли активности state, смотрим, есть ли среди аргументов функции аргумент с именем `state`
    sig = signature(definition)
    state = None
    if "state" in sig.parameters:
        state = {}

    return {
        "activity_name": activity_name,
        "param": param,
        "state": state,
    }


def configure_activity(definitions: dict, entry: dict) -> dict:
    """
    Создать активность на основе definitions (списка определений) и entry.

    Definition — логика активности, entry — данные о ней. Совместив их, мы получаем активность, то есть
    объект в виде словаря, у которого есть методы и свойства. Их можно вызывать или читать через API.

    Если `param` в entry равен `None`, то в definition ничего не передается, и будет использован параметр,
    указанный в definition по умолчанию. Поэтому не используйте `None` в качестве значения параметра!
    """
    log(f"Activity entry: {entry}", log_type="config")

    # Собираем данные из entry
    definition = definitions[entry["activity_name"]]
    param = entry["param"]
    state = entry["state"]

    # Даем определению аргументы только в том случае, если они ему нужны.
    # Чтобы понять, нужны ли аргументы, смотрим сигнатуру функции
    sig = signature(definition)
    kwargs = {}

    # Если в качестве параметра при создании entry передано None,
    # мы считаем это отсутствием параметра и, следовательно,
    # definition будет использовать параметр по умолчанию
    if "param" in sig.parameters and param is not None:
        kwargs["param"] = param
    # Передаем state из entry, если он нужен definition
    if "state" in sig.parameters:
        kwargs["state"] = state
    # Definition могут быть нужны определения, если оно внутри себя вызывает другие активности.
    # Например, это нужно композитным активностям
    if "definitions" in sig.parameters:
        kwargs["definitions"] = definitions

    return definition(**kwargs)


# Используется движком в pick_activity, чтобы предложить игроку все доступные активности
# со всеми доступными параметрами на выбор
def get_allowed_activity_entries(gs, definitions):
    allowed_entries = []
    # Проходим по всем определениям
    for definition in definitions.values():
        # Если активности нужны definitions (например, если это композитная активность), передадим их
        sig = signature(definition)
        kwargs = {}
        if "definitions" in sig.parameters:
            kwargs["definitions"] = definitions

        # Смотрим, есть ли у активности параметр
        # Если параметра нет, просто проверяем, можем ли мы выполнить активность в следующем тике
        # Если параметр есть, создаем по варианту активности на каждый параметр и проверяем каждый из вариантов
        # Чтобы не дублировать логику, представляем отсутствие параметра как параметр с одним вариантом None
        param_space = get_param_space(gs, definition)
        params_to_check = [None] if param_space is None else param_space
        # None не может быть значением параметра, поэтому мы можем использовать это как флаг
        # и передавать параметр только если он не None
        for param in params_to_check:
            activity = (
                definition(**kwargs)
                if param is None
                else definition(**kwargs, param=param)
            )
            if not check_is_background(activity) and check_can_continue(gs, activity):
                # В create_activity_entry param=None по умолчанию, так что мы спокойно можем
                # передать туда None без риска получить исключение
                entry = create_activity_entry(definition, param)
                allowed_entries.append(entry)

    # Возвращаем все доступные варианты в виде списка entries.
    # State там сейчас не инициализирован, то есть это None или {},
    # потому что мы создаем entry уже после создания активности,
    # и, следовательно, не передаем активности ссылку на state.
    # Но это не так уж и важно. State будет инициализирован при первом создании активности
    return allowed_entries


def start_activity(gs: dict, definitions: dict, entry: dict):
    """
    Добавить entry в список текущих активностей.
    Если активность не-stackable, остановить другие не-stackable активности.
    """
    # Создаем активность, чтобы понять, стакается ли она
    activity = configure_activity(definitions, entry)
    if not check_is_stackable(activity):
        gs["activity_entries"] = [
            entry
            for entry in gs["activity_entries"]
            if check_is_stackable(configure_activity(definitions, entry))
        ]
    # При добавлении в gs любому объекту нужен ID, чтобы мы могли запомнить его или обратиться к нему.
    # До добавления в gs такой необходимости нет
    entry_with_id = gs_api.with_id(gs, entry)
    gs["activity_entries"].append(entry_with_id)


def composite_activity(
    definitions: dict,
    init_queue: Callable[[], list],
    state: dict = None,
    name="default",
):
    """
    Создать композитную активность, состояющую из нескольких подактивностей, выполняющихся последовательно.
    Следующая подактивность начинает выполняться, как только `can_continue` предыдущей подактивности становится `False`.


    Каждая поадктивность должна выполняться хотя бы тик, иначе композитная активность завершается досрочно.

    Args:
        definitions: Определения активностей. Нужны, чтобы создать активности из entries в очереди.
        init_queue: Функция, которая вычисляет очередь — список entries.
        state: Локальное состояние активности.
        name: Название активности для отображения в UI.

    Returns:
        dict: Композитная активность. `hold_required` и `is_stackable` равны соответствующим свойствам
            текущей подактивности.

    """

    # Если state еще не инициализирован, проводим инициализацию.
    # Мы можем создать активность на этапе перебора возможных активностей.
    # В таком случае нам нужно обозначить, что первая подактивность еще не прожила ни одного тика,
    # чтобы при проверке мы не могли решить, что пора переходить к следующей подактивности.
    # Поэтому next_index инициализируется как None и превращается в 0 только при успешной проверке can_continue

    def init():
        return {"queue": init_queue(), "current_index": 0, "next_index": None}

    state = state_api.init_fn(state, init)

    # В очереди хранятся не activities (это логика),
    # а entries, поэтому в качестве аргумента нам нужны definitions.
    # Чтобы узнать текущую или следующую подактивность, мы проводим конфигурацию

    def get_current():
        return configure_activity(definitions, state["queue"][state["current_index"]])

    def get_next():
        return configure_activity(definitions, state["queue"][state["next_index"]])

    def tick_effect(gs):
        # 0. На всякий случай повторная проверка: мы могли запустить активность, не выполняя can_continue
        if state["next_index"] is None:
            state["next_index"] = 0

        # 1. Если надо перейти к следующей подактивности, переходим
        state["current_index"] = state["next_index"]

        # 2. Выполняем эффект текущей подактивности
        current = get_current()
        apply_tick_effect(gs, current)

    def can_continue(gs):
        # 0. Защита от пустой очереди
        if len(state["queue"]) == 0:
            return False

        # 1. Если мы больше не можем выполнять текущую подактивность, в следующем тике надо перейти к следующей.
        # Если индекс следующей None, то есть мы еще не выполнили ни одного тика, вся активность не может начаться
        current = get_current()
        if not check_can_continue(gs, current):
            if state["next_index"] is None:
                return False
            else:
                state["next_index"] = state["current_index"] + 1

        # 2. Если мы можем начать первую подактивность, в следующем тике будем выполнять ее.
        # Можно воспринимать это так: если мы можем прожить один тик в настоящем, мы имеем право смотреть в будущее
        if state["next_index"] is None:
            state["next_index"] = 0

        # 3. Если очередь закончилась, композитная активность завершается
        if state["next_index"] >= len(state["queue"]):
            return False

        # 4. То, может ли выполняться вся композитная активность, зависит от того, может ли выполняться подактивность,
        # которая должна выполняться в следующем тике
        next_activity = get_next()
        return check_can_continue(gs, next_activity)

    # Свойства hold_required и is_stackable равны свойствам текущей подактивности

    def hold_required():
        current = get_current()
        return check_hold_required(current)

    def is_stackable():
        current = get_current()
        return check_is_stackable(current)

    def is_background():
        current = get_current()
        return check_is_background(current)

    return base_activity(
        tick_effect, can_continue, hold_required, is_stackable, is_background, name=name
    )
