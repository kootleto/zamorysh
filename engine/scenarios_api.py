from inspect import signature
from typing import Any, Callable

from tools.logger import log
from tools.utils import call_with_gs
from . import gs_api


def base_transition(
    node_from: Any,
    node_to: Any,
    trigger: Callable[[dict], bool] | Callable[[], bool],
    effect: Callable[[dict], None] | Callable[[], None],
) -> dict:
    """
    Создать переход из одного node сценария в другой.

    Начальный и конечный node могут совпадать.

    Args:
        node_from: Node, из которого совершается переход.
        node_to: Node, в который совершается переход.
        trigger: Условие перехода.
        effect: Функция, которая выполняется при переходе. Принимает `gs`.
    """
    return {
        "from": node_from,
        "to": node_to,
        "trigger": trigger,
        "effect": effect,
    }


def get_node_from(transition):
    return transition["from"]


def get_node_to(transition):
    return transition["to"]


def check_trigger(gs, transition):
    return call_with_gs(gs, transition["trigger"])


def apply_effect(gs, transition):
    call_with_gs(gs, transition["effect"])


def base_scenario(transitions: list[dict] = None, start_node: Any = 0) -> dict:
    """
    Создать сценарий с указанными переходами и стартовым состоянием.
    Базовое определение (definition) сценария.

    Сценарий — это конечный автомат / машина состояний / ориентированный граф.

    Вершины этого графа — node, или состояния. Они могут быть представлены любым типом данных, не только числами.

    Ребра этого графа — переходы между nodes. Триггеры переходов проверяются каждый тик. Если срабатывают сразу
    несколько триггеров, выбирается триггер первого перехода по порядку в списке переходов.

    Помните об этом! Например, не ставьте переход из node в себя (петлю) до перехода из этого же node в другой,
    если хотите при срабатывании обоих триггеров делать переход в другой node, а не петлю.
    """
    return {
        "start_node": start_node,
        "transitions": transitions,
    }


def get_start_node(scenario):
    return scenario["start_node"]


def get_transitions(scenario):
    return scenario["transitions"]


def create_scenario_entry(definition) -> dict:
    """
    Создать запись сценария (entry).

    Это словарь, в котором хранятся определение (definition) сценария, текущий node и
    локальное состояние сценария (если есть).
    """
    # Получаем имя функции-определения в формате модуль.имя (по этому ключу в definitions хранится сама функция)
    scenario_name = f"{definition.__module__}.{definition.__name__}"

    # Если сценарию нужен state, создаем пустой словарь. При создании сценария в начале игры
    # пройдет инициализация, и в этом словаре окажутся значения по умолчанию.
    # Иначе явно показываем, что state сценарию не нужен.
    # Чтобы понять, нужен ли сценарию state, смотрим, есть ли среди аргументов функции аргумент с именем `state`
    sig = signature(definition)
    state = None
    if "state" in sig.parameters:
        state = {}

    # Node будет инициализирован в start_scenario
    return {
        "scenario_name": scenario_name,
        "node": None,
        "state": state,
    }


def get_node(entry):
    return entry["node"]


def set_node(entry, node):
    entry["node"] = node


def configure_scenario(definitions, entry):
    """
    Создать сценарий на основе definitions (списка определений) и entry.

    Definition — логика сценария, entry — данные о нем. Совместив их, мы получаем сценарий, то есть
    объект, у которого есть список переходов и начальное состояние.
    """
    log(f"Scenario entry: {entry}", log_type="config")

    # Собираем данные из entry
    definition = definitions[entry["scenario_name"]]
    state = entry["state"]

    # Даем определению state только в том случае, если он ему нужен.
    # Чтобы понять, нужен ли, смотрим сигнатуру функции
    sig = signature(definition)
    kwargs = {}
    if "state" in sig.parameters:
        kwargs["state"] = state

    return definition(**kwargs)


def start_scenario(gs, definitions, scenario_entry):
    """Добавить entry в список текущих сценариев."""
    scenario = configure_scenario(definitions, scenario_entry)
    set_node(scenario_entry, get_start_node(scenario))
    # При добавлении в gs любому объекту нужен ID, чтобы мы могли запомнить его или обратиться к нему
    entry_with_id = gs_api.with_id(gs, scenario_entry)
    gs["scenario_entries"].append(entry_with_id)


# В начале игры движок запускает все сценарии
def start_all_scenarios(gs, definitions):
    for definition in definitions.values():
        entry = create_scenario_entry(definition)
        start_scenario(gs, definitions, entry)
