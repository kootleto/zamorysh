"""
Главный цикл игры.
"""

from time import sleep

from gameplay.api import initial_state, resolvers
from interface import ui
from tools.loader import load_definitions
from tools.logger import log
from . import activities_api
from . import gs_api
from . import resolver_api
from . import scenarios_api


def pick_activity(gs, definitions):
    # Получаем все активности со всеми вариантами параметров (то есть все entries),
    # которые сейчас можно начать
    allowed_entries = activities_api.get_allowed_activity_entries(gs, definitions)

    # Получаем нужные для UI свойства активностей
    activities_ui_info = []
    for entry in allowed_entries:
        # Для этого создаем активность
        activity = activities_api.configure_activity(definitions, entry)
        # Храним свойства в формате (имя, требуется ли удержание)
        activities_ui_info.append(
            (
                activities_api.get_activity_name(activity),
                activities_api.check_hold_required(activity),
            )
        )

    # Получаем индекс entry для запуска и запускаем активность
    selected_index = ui.handle_input(activities_ui_info)
    entry_to_start = allowed_entries[selected_index]
    activities_api.start_activity(gs, definitions, entry_to_start)


def update(gs, activity_definitions, scenario_definitions, is_initial=False):
    # 1. Применяем tick_effect всех текущих активностей
    for entry in gs_api.get_activity_entries(gs):
        log(f"Applying effect for {entry["activity_name"]}", log_type="activity")
        activity = activities_api.configure_activity(activity_definitions, entry)
        activities_api.apply_tick_effect(gs, activity)

    # 2. Применяем изменения и разрешаем конфликты до проверки сценариев,
    # чтобы сценарии могли отреагировать на изменения в этом же тике
    resolver_api.resolve_intents(gs, resolvers)

    # 3. Увеличиваем игровое время на 1, если это не часть инициализации
    if not is_initial:
        gs_api.tick(gs)

    # 4. Проверяем trigger для всех переходов сценариев, исходящих из их текущего node
    # Если триггер срабатывает, применяем effect и меняем node
    # Каждый сценарий за тик может совершить только один переход. Порядок проверки зависит от того,
    # в каком порядке указаны переходы в definition сценария
    for entry in gs_api.get_scenario_entries(gs):
        scenario = scenarios_api.configure_scenario(
            activity_definitions, scenario_definitions, entry
        )
        node = scenarios_api.get_node(entry)
        for transition in scenarios_api.get_transitions(scenario):
            node_matches = scenarios_api.get_node_from(transition) == node
            trigger_ok = scenarios_api.check_trigger(gs, transition)
            if node_matches and trigger_ok:
                log(
                    f"Condition met for {entry["scenario_name"]}. Moving node {scenarios_api.get_node_from(transition)} -> {scenarios_api.get_node_to(transition)}",
                    log_type="scenario",
                )
                scenarios_api.apply_effect(gs, transition)
                scenarios_api.set_node(entry, scenarios_api.get_node_to(transition))
                break

    # 5. Применяем изменения и разрешаем конфликты до остановки лишних активностей,
    # чтобы условия были такими же, как в начале следующего тика
    resolver_api.resolve_intents(gs, resolvers)

    # 6. Останавливаем активности, которые больше не могут продолжаться
    # (игрок отпустил кнопку или не выполняется can_continue)
    # Кладем entries в новый список, потому что нельзя менять список во время прохода по нему в цикле
    new_entries = []
    for entry in gs_api.get_activity_entries(gs):
        activity = activities_api.configure_activity(activity_definitions, entry)
        hold_ok = (
            not activities_api.check_hold_required(activity) or ui.check_key_pressed()
        )
        can_continue = activities_api.check_can_continue(gs, activity)

        if hold_ok and can_continue:
            new_entries.append(entry)
        else:
            log(
                f"Stopped {entry["activity_name"]} (can_continue: {can_continue}, hold_ok: {hold_ok})",
                log_type="activity",
            )
    gs_api.set_activity_entries(gs, new_entries)


def check_foreground_activities_running(gs, definitions):
    entries = gs_api.get_activity_entries(gs)
    for entry in entries:
        activity = activities_api.configure_activity(definitions, entry)
        if not activities_api.check_is_background(activity):
            return True
    return False


def main():
    # Инициализация
    game_state = gs_api.get_initial_gs(initial_state)
    definitions = load_definitions("content")
    scenarios_api.start_all_scenarios(
        game_state, definitions["activities"], definitions["scenarios"]
    )
    # Обновление, чтобы проверить триггеры сценариев (какие-то триггеры могут сработать уже при initial_gs)
    update(
        game_state, definitions["activities"], definitions["scenarios"], is_initial=True
    )

    while gs_api.is_running(game_state):
        log(
            f"time: {gs_api.get_time(game_state)}, vitals: {game_state["gameplay"]["vitals"]},",
            f"stats: {game_state["gameplay"]["stats"]},",
            f"activity entries: {gs_api.get_activity_entries(game_state)}",
            log_type="status",
        )
        ui.show_stats(game_state)
        # Если не запущена ни одна не фоновая, игрок должен выбрать активность
        if not check_foreground_activities_running(
            game_state, definitions["activities"]
        ):
            pick_activity(game_state, definitions["activities"])
        log(f"------ TICK {gs_api.get_time(game_state)} ------", log_type="tick")
        sleep(0.15)
        update(game_state, definitions["activities"], definitions["scenarios"])

    # Ожидаем нажатия Enter, чтобы при запуске в системном терминале игра не закрылась сразу после выхода из цикла
    ui.display("--- GAME FINISHED ---")
    ui.prompt("Press Enter to exit")


if __name__ == "__main__":
    main()
