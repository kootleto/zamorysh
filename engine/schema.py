from typing import Callable, TypedDict, Any, Literal, Protocol, Awaitable


# Сущности внутри gs
class ActivityEntry(TypedDict):
    activity_name: str
    param: Any
    state: dict[str, Any] | None


class ScenarioEntry(TypedDict):
    scenario_name: str
    node: Any
    state: dict[str, Any] | None


Operation = Literal["set", "mod"]


class Intent(TypedDict):
    domain: str
    target: str
    op: Operation
    value: Any


# Состояние игры
class SystemState(TypedDict):
    time: int
    activity_entries: list[ActivityEntry]
    scenario_entries: list[ScenarioEntry]
    intents: list[Intent]
    next_id: int
    is_running: bool
    tick_interval: float


GameplayState = dict[str, dict[str, Any]]


class GameState(TypedDict):
    gameplay: GameplayState
    system: SystemState


EffectResult = None | Awaitable[None]
Effect = Callable[[GameState], EffectResult] | Callable[[], EffectResult]


# Сценарии
Transition = TypedDict(
    "Transition",
    {
        "from": Any,
        "to": Any,
        "trigger": Callable[[GameState], bool] | Callable[[], bool],
        "effect": Effect,
    },
)


class Scenario(TypedDict):
    start_node: Any
    transitions: list[Transition]


class ScenarioDefinition(Protocol):
    __name__: str
    __module__: str
    __call__: Callable[..., Scenario]


ScenarioDefinitions = dict[str, ScenarioDefinition]


# Активности
class Activity(TypedDict):
    tick_effect: Effect
    can_continue: Callable[[GameState], bool] | Callable[[], bool]
    hold_required: Callable[[], bool]
    is_stackable: Callable[[], bool]
    is_background: Callable[[], bool]
    name: str


class ActivityDefinition(Protocol):
    __name__: str
    __module__: str
    __call__: Callable[..., Activity]


ActivityDefinitions = dict[str, ActivityDefinition]


class Definitions(TypedDict):
    activities: ActivityDefinitions
    scenarios: ScenarioDefinitions


# Резолвер
Resolver = Callable[[GameState, list[Intent]], None]


# Описание активностей для UI
class ActivityOption(TypedDict):
    label: str
    hold_required: bool


ActivityOptions = list[ActivityOption]
