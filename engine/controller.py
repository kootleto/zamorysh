from typing import Callable

from engine.schema import (
    GameState,
    Definitions,
    ActivityDefinitions,
    ScenarioDefinitions,
    ActivityOptions,
    ActivityEntry,
)
from gameplay.api import resolvers, initial_state
from tools.loader import load_definitions
from tools.logger import log
from . import activities_api, gs_core
from . import gs_api
from . import resolver_api
from . import scenarios_api


def _activity_definitions(definitions: Definitions) -> ActivityDefinitions:
    return definitions["activities"]


def _scenario_definitions(definitions: Definitions) -> ScenarioDefinitions:
    return definitions["scenarios"]


def init_game():
    game_state = gs_core.init_gs(initial_state)
    definitions = load_definitions("content")
    return game_state, definitions


async def start_game(gs: GameState, definitions: Definitions):
    scenarios_api.start_all_scenarios(
        gs, _activity_definitions(definitions), _scenario_definitions(definitions)
    )
    # Обновление, чтобы проверить триггеры сценариев (какие-то триггеры могут сработать уже при initial_gs)
    await update(gs, definitions, is_initial=True)


async def update(
    gs: GameState,
    definitions: Definitions,
    is_initial: bool = False,
    check_button_pressed: Callable[[], bool] = None,
):

    log(f"------ TICK {gs_api.get_time(gs)} ------", log_type="tick")
    log(
        f"vitals: {gs["gameplay"]["vitals"]},",
        f"stats: {gs["gameplay"]["stats"]},",
        f"activity entries: {gs_core.get_activity_entries(gs)}",
        log_type="status",
    )

    # 0. Очищаем массив с информацией завершенных в предыдущем тике активностях
    gs_core.clear_just_finished(gs)

    # 1. Применяем tick_effect всех текущих активностей
    for entry in gs_core.get_activity_entries(gs):
        log(f"Applying effect for {entry["activity_name"]}", log_type="activity")
        activity = activities_api.configure_activity(
            _activity_definitions(definitions), entry
        )
        await activities_api.apply_tick_effect(gs, activity)

    # 2. Применяем изменения и разрешаем конфликты до проверки сценариев,
    # чтобы сценарии могли отреагировать на изменения в этом же тике
    resolver_api.resolve_intents(gs, resolvers)

    # 3. Увеличиваем игровое время на 1, если это не часть инициализации
    if not is_initial:
        gs_core.tick(gs)

    # 4. Проверяем trigger для всех переходов сценариев, исходящих из их текущего node
    # Если триггер срабатывает, применяем effect и меняем node
    # Каждый сценарий за тик может совершить только один переход. Порядок проверки зависит от того,
    # в каком порядке указаны переходы в definition сценария
    for entry in gs_core.get_scenario_entries(gs):
        scenario = scenarios_api.configure_scenario(
            _activity_definitions(definitions),
            _scenario_definitions(definitions),
            entry,
        )
        node = scenarios_api.get_node(entry)
        for transition in scenarios_api.get_transitions(scenario):
            node_matches = scenarios_api.get_node_from(transition) == node
            trigger_ok = scenarios_api.check_trigger(gs, transition)
            if node_matches and trigger_ok:
                log(
                    f"Condition met for {entry["scenario_name"]}. "
                    f"Moving node {scenarios_api.get_node_from(transition)} "
                    f"-> {scenarios_api.get_node_to(transition)}",
                    log_type="scenario",
                )
                await scenarios_api.apply_effect(gs, transition)
                scenarios_api.set_node(entry, scenarios_api.get_node_to(transition))
                break

    # 5. Применяем изменения и разрешаем конфликты до остановки лишних активностей,
    # чтобы условия были такими же, как в начале следующего тика
    resolver_api.resolve_intents(gs, resolvers)

    # 6. Останавливаем активности, которые больше не могут продолжаться
    # (игрок отпустил кнопку или не выполняется can_continue)
    # Кладем entries в новый список, потому что нельзя менять список во время прохода по нему в цикле
    new_entries = []
    for entry in gs_core.get_activity_entries(gs):
        activity = activities_api.configure_activity(
            _activity_definitions(definitions), entry
        )
        hold_ok = (
            not activities_api.check_hold_required(activity) or check_button_pressed()
        )
        can_continue = activities_api.check_can_continue(gs, activity)

        if hold_ok and can_continue:
            new_entries.append(entry)
        else:
            log(
                f"Stopped {entry["activity_name"]} (can_continue: {can_continue}, hold_ok: {hold_ok})",
                log_type="activity",
            )
            # Если активность останавливается, кладем entry в специальный массив - это позволит потом как-то
            # отреагировать на остановку уже вне движка
            gs_core.add_finished_entry(gs, entry)
    gs_core.set_activity_entries(gs, new_entries)


# Если не запущена ни одна не-фоновая активность, игрок должен выбрать какую-то
def prompt_required(gs: GameState, definitions: Definitions) -> bool:
    entries = gs_core.get_activity_entries(gs)
    for entry in entries:
        activity = activities_api.configure_activity(
            _activity_definitions(definitions), entry
        )
        if not activities_api.check_is_background(activity):
            return False
    return True


def get_activity_options(gs: GameState, definitions: Definitions) -> ActivityOptions:
    # Получаем все активности со всеми вариантами параметров (то есть все entries),
    # которые сейчас можно начать
    allowed_entries = activities_api.get_allowed_activity_entries(
        gs, _activity_definitions(definitions)
    )

    # Получаем нужные для UI свойства активностей
    options = []
    for entry in allowed_entries:
        # Для этого создаем активность
        activity = activities_api.configure_activity(
            _activity_definitions(definitions), entry
        )
        # Храним свойства в формате (имя, требуется ли удержание)
        options.append(
            {
                "label": activities_api.get_activity_name(activity),
                "hold_required": activities_api.check_hold_required(activity),
            }
        )

    return options


def start_selected_activity(gs: GameState, definitions: Definitions, index: int):
    allowed_entries = activities_api.get_allowed_activity_entries(
        gs, _activity_definitions(definitions)
    )
    activities_api.start_activity(
        gs, _activity_definitions(definitions), allowed_entries[index]
    )


def is_running(gs: GameState) -> bool:
    return gs_core.is_running(gs)


def get_tick_interval(gs: GameState) -> float:
    return gs_core.get_tick_interval(gs)


def get_just_finished(gs: GameState) -> list[ActivityEntry]:
    return gs_core.get_just_finished(gs)


def call_on_finish(gs: GameState, definitions: Definitions, entry: ActivityEntry):
    activities_api.call_on_finish(gs, _activity_definitions(definitions), entry)
