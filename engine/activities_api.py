import itertools
from typing import Callable, Iterable

from tools.utils import (
    call_with_gs,
    ensure_callable,
    call_with_gs_async,
    accepts,
)
from . import data_api
from . import gs_api, gs_core
from .schema import (
    Activity,
    ActivityDefinition,
    ActivityEntry,
    ActivityDefinitions,
    GameState,
    Effect,
    FinishCallback,
    ParamsSpace,
    Params,
)


# Все параметры активности, кроме имени и params_space,
# хранятся как callable, чтобы их можно было изменять динамически
# Например, в композитных активностях hold_required и is_stackable совпадают с соответствующими свойствами
# текущей подактивности


def base_activity(
    tick_effect: Effect = lambda gs: None,
    can_continue: (
        bool | Callable[[GameState], bool] | Callable[[], bool]
    ) = lambda gs: True,
    hold_required: bool | Callable[[], bool] = False,
    is_stackable: bool | Callable[[], bool] = False,
    is_background: bool | Callable[[], bool] = False,
    name: str = "default",
) -> Activity:
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

    return {
        "tick_effect": tick_effect,
        "can_continue": ensure_callable(can_continue),
        "hold_required": ensure_callable(hold_required),
        "is_stackable": ensure_callable(is_stackable),
        "is_background": ensure_callable(is_background),
        "name": name,
    }


async def apply_tick_effect(gs: GameState, activity: Activity):
    await call_with_gs_async(gs, activity["tick_effect"])


def check_can_continue(gs: GameState, activity: Activity) -> bool:
    return call_with_gs(gs, activity["can_continue"])


def check_hold_required(activity: Activity) -> bool:
    return activity["hold_required"]()


def check_is_stackable(activity: Activity) -> bool:
    return activity["is_stackable"]()


def check_is_background(activity: Activity) -> bool:
    return activity["is_background"]()


def get_activity_name(activity: Activity) -> str:
    return activity["name"]


# Это обертка над декоратором: у нее есть параметр params_space, и его может использовать сам декоратор.
# Она возвращает декоратор
def with_params_space(**params_space: Iterable | Callable[[dict], Iterable]):
    # Это декоратор, то есть обертка над definition. Он принимает definition,
    # присваивает ему указанную область параметра в качестве атрибута
    # и возвращает definition
    def wrapper(definition):
        # Функции в Python - это объекты, и им можно присваивать атрибуты. Мы используем это,
        # чтобы узнать область параметра можно было из определения активности, не создавая саму активность
        # (ведь для создания активности уже нужно будет указать параметр)
        definition.params_space = params_space
        return definition

    return wrapper


def get_params_space(gs: GameState, definition: ActivityDefinition) -> ParamsSpace:
    # Атрибут функции можно узнать, не вызывая ее, чем мы и пользуемся
    params_space = getattr(definition, "params_space", dict()).copy()

    # space может быть как функцией, которая принимает gs и возвращает Iterable, так и просто Iterable
    # (то есть чем-то, по чему можно пройтись в цикле for)
    for param, space in params_space.items():
        if callable(space):
            params_space[param] = call_with_gs(gs, space)
    return params_space


# Это декоратор. Он делает то же, что и with_params_space: присваивает объекту атрибут
def with_auto_start(definition: ActivityDefinition):
    """Запустить активность в начале игры."""
    definition.auto_start = True
    return definition


def check_auto_start(definition: ActivityDefinition) -> bool:
    # Если такого атрибута присвоено не было, то автозапуск нам не нужен
    return getattr(definition, "auto_start", False)


def system_only(definition: ActivityDefinition):
    definition.system_only = True
    return definition


def check_system_only(definition: ActivityDefinition) -> bool:
    return getattr(definition, "system_only", False)


def on_finish(callback: FinishCallback):
    """Сделать что-то после того, как активность завершится. То, что внутри, будет вызвано после окончания тика.
    Функция может принимать в качестве аргументов `gs` и `entry` (оба аргумента опциональны,
    писать именно в таком порядке).

    Эта функция НЕ МОЖЕТ менять gs, но может что-то выводить на экран."""

    def wrapper(definition):
        definition.on_finish = callback
        return definition

    return wrapper


def call_on_finish(
    gs: GameState, definitions: ActivityDefinitions, entry: ActivityEntry
):
    definition = definitions[entry["activity_name"]]
    callback = getattr(definition, "on_finish", None)

    if callback:
        args = [entry] if accepts("entry", callback) else []
        call_with_gs(gs, callback, *args)


def override_activity(activity: Activity, **overrides) -> Activity:
    """
    Заменить любые элементы словаря активности: `tick_effect`, `can_continue`, `hold_required`,
    `is_stackable`, `is_background`, `name`.

    Это позволяет заменять отдельные элементы определений, создавая на их основе новое определение,
    и не хранить все свойства и методы активности в аргументах.
    Например, по умолчанию параметр `hold_required` композитной активности равен `hold_required` текущей подактивности.
    Сделав override с `hold_required = False`, мы сможем изменить ее поведение.
    """
    new_data = {**activity, **overrides}
    return base_activity(**new_data)


def create_activity_entry(
    definition: ActivityDefinition, params: Params | None = None
) -> ActivityEntry:
    """
    Создать запись активности (entry).

    Это словарь, в котором хранятся определение (definition) активности, параметры (если есть) и
    локальное состояние активности (если есть).
    """

    # Получаем имя функции-определения в формате модуль.имя (по этому ключу в definitions хранится сама функция)
    activity_name = f"{definition.__module__}.{definition.__name__}"

    # Если активности нужен state, создаем пустой словарь. При первом создании активности
    # пройдет инициализация, и в этом словаре окажутся значения по умолчанию.
    # Иначе явно показываем, что state активности не нужен.
    # Чтобы понять, нужен ли активности state, смотрим, есть ли среди аргументов функции аргумент с именем `state`
    state = None
    entry_params = None
    if accepts("state", definition):
        state = {}
    if accepts("params", definition):
        entry_params = params if params is not None else {}

    return {
        "activity_name": activity_name,
        "params": entry_params,
        "state": state,
    }


def configure_activity(
    definitions: ActivityDefinitions, entry: ActivityEntry
) -> Activity:
    """
    Создать активность на основе definitions (списка определений) и entry.

    Definition — логика активности, entry — данные о ней. Совместив их, мы получаем активность, то есть
    объект в виде словаря, у которого есть методы и свойства. Их можно вызывать или читать через API.
    """
    # log(f"Activity entry: {entry}", log_type="config")

    # Собираем данные из entry
    definition = definitions[entry["activity_name"]]
    params = entry["params"]
    state = entry["state"]

    # Даем определению аргументы только в том случае, если они ему нужны.
    # Чтобы понять, нужны ли аргументы, смотрим сигнатуру функции
    kwargs = {}

    # Если в качестве параметров при создании entry передано None,
    # мы считаем это отсутствием параметров и, следовательно,
    # definition будет использовать параметры по умолчанию
    if accepts("params", definition):
        kwargs["params"] = params
    # Передаем state из entry, если он нужен definition
    if accepts("state", definition):
        kwargs["state"] = state
    # Definition могут быть нужны определения, если оно внутри себя вызывает другие активности.
    # Например, это нужно композитным активностям
    if accepts("definitions", definition):
        kwargs["definitions"] = definitions

    return definition(**kwargs)


def _generate_param_combinations(params_space: ParamsSpace) -> list[Params]:
    params_names = params_space.keys()
    spaces = params_space.values()

    combinations = []
    for combination in itertools.product(*spaces):
        combinations.append(dict(zip(params_names, combination)))

    return combinations


# Используется движком в pick_activity, чтобы предложить игроку все доступные активности
# со всеми доступными параметрами на выбор
def get_allowed_activity_entries(
    gs: GameState, definitions: ActivityDefinitions
) -> list[ActivityEntry]:
    allowed_entries = []
    # Проходим по всем определениям
    for definition in definitions.values():
        if check_system_only(definition):
            continue

        # Если активности нужны definitions (например, если это композитная активность), передадим их
        kwargs = {}
        if accepts("definitions", definition):
            kwargs["definitions"] = definitions

        # Смотрим, есть ли у активности параметры
        # Если параметров нет, просто проверяем, можем ли мы выполнить активность в следующем тике
        # Если параметры есть, создаем по варианту активности на каждую комбинацию и проверяем каждый из вариантов
        params_space = get_params_space(gs, definition)
        if not params_space:
            combinations = [None]
        else:
            combinations = _generate_param_combinations(params_space)

        for combination in combinations:
            if combination is None:
                activity = definition(**kwargs)
            else:
                activity = definition(**kwargs, params=combination)
            if not check_is_background(activity) and check_can_continue(gs, activity):
                entry = create_activity_entry(definition, combination)
                allowed_entries.append(entry)

    # Возвращаем все доступные варианты в виде списка entries.
    # State там сейчас не инициализирован, то есть это None или {},
    # потому что мы создаем entry уже после создания активности,
    # и, следовательно, не передаем активности ссылку на state.
    # Но это не так уж и важно. State будет инициализирован при первом создании активности
    return allowed_entries


def start_activity(
    gs: GameState, definitions: ActivityDefinitions, entry: ActivityEntry
):
    """
    Добавить entry в список текущих активностей.
    Если активность не-stackable, остановить другие не-stackable активности.
    """
    # Создаем активность, чтобы понять, стакается ли она
    activity = configure_activity(definitions, entry)
    # Удаляем из списка запущенных все не стакающиеся
    if not check_is_stackable(activity):
        new_entries = []
        for active_entry in gs_core.get_activity_entries(gs):
            if check_is_stackable(configure_activity(definitions, active_entry)):
                new_entries.append(active_entry)
            else:
                gs_core.add_finished_entry(gs, active_entry)
        gs_core.set_activity_entries(gs, new_entries)
    # При добавлении в gs любому объекту нужен ID, чтобы мы могли запомнить его или обратиться к нему.
    # До добавления в gs такой необходимости нет
    entry_with_id = gs_api.with_id(gs, entry)
    gs_core.add_activity_entry(gs, entry_with_id)


def start_activity_by_definition(
    gs: GameState,
    definitions: ActivityDefinitions,
    definition: ActivityDefinition,
    params=None,
):
    """Создать entry активности из определения и параметра и запустить эту активность."""
    entry = create_activity_entry(definition, params)
    start_activity(gs, definitions, entry)


def composite_activity(
    definitions: ActivityDefinitions,
    init_queue: Callable[[], list[ActivityEntry]],
    state: dict = None,
    name="default",
) -> Activity:
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

    state = data_api.init_fn(state, init)

    # В очереди хранятся не activities (это логика),
    # а entries, поэтому в качестве аргумента нам нужны definitions.
    # Чтобы узнать текущую или следующую подактивность, мы проводим конфигурацию

    def get_current():
        return configure_activity(definitions, state["queue"][state["current_index"]])

    def get_next():
        return configure_activity(definitions, state["queue"][state["next_index"]])

    async def tick_effect(gs):
        # 0. На всякий случай повторная проверка: мы могли запустить активность, не выполняя can_continue
        if state["next_index"] is None:
            state["next_index"] = 0

        # 1. Если надо перейти к следующей подактивности, переходим
        state["current_index"] = state["next_index"]

        # 2. Выполняем эффект текущей подактивности
        current = get_current()
        await apply_tick_effect(gs, current)

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
        tick_effect,
        can_continue,
        hold_required,
        is_stackable,
        is_background,
        name=name,
    )
