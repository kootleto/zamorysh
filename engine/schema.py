from typing import Callable, TypedDict, Any, Literal, Protocol

# Состояние игры


class SystemState(TypedDict):
    time: int
    activity_entries: list[ActivityEntry]
    scenario_entries: list[ScenarioEntry]
    intents: list[Intent]
    next_id: int
    is_end: bool


GameplayState = dict[str, dict[str, Any]]


class GameState(TypedDict):
    gameplay: GameplayState
    system: SystemState


# Активности


class Activity(TypedDict):
    tick_effect: Callable[[dict], None] | Callable[[], None]
    can_continue: Callable[[dict], bool] | Callable[[], bool]
    hold_required: Callable[[], bool]
    is_stackable: Callable[[], bool]
    is_background: Callable[[], bool]
    name: str


class ActivityEntry(TypedDict):
    activity_name: str
    param: Any
    state: dict[str, Any] | None


class ActivityDefinition(Protocol):
    __name__: str
    __module__: str
    __call__: Callable[..., Activity]


ActivityDefinitions = dict[str, ActivityDefinition]


# Сценарии


Transition = TypedDict(
    "Transition",
    {
        "from": Any,
        "to": Any,
        "trigger": Callable[[GameState], bool] | Callable[[], bool],
        "effect": Callable[[GameState], None] | Callable[[], None],
    },
)


class Scenario(TypedDict):
    start_node: Any
    transitions: list[Transition]


class ScenarioEntry(TypedDict):
    scenario_name: str
    node: Any
    state: dict[str, Any] | None


class ScenarioDefinition(Protocol):
    __name__: str
    __module__: str
    __call__: Callable[..., Scenario]


ScenarioDefinitions = dict[str, ScenarioDefinition]


# Интенты

Operation = Literal["set", "mod"]


class Intent(TypedDict):
    domain: str
    target: str
    op: Operation
    value: Any


Resolver = Callable[[GameState, list[Intent]], None]
