from time import sleep
from . import gs_api
from . import resolver_api
from . import activities_api
from . import scenarios_api
from interface import ui
from tools import logger, definitions_loader


def update(gs, activity_definitions, scenario_definitions):
    # Применяем tick_effect всех текущих активностей
    for entry in gs_api.get_activity_entries(gs):
        logger.log(f"Applying effect for {entry["activity_name"]}", log_type="activity")
        activity = activities_api.configure_activity(activity_definitions, entry)
        activities_api.apply_tick_effect(gs, activity)
    resolver_api.resolve_intents(gs)

    # Проверяем trigger для всех актуальных переходов сценариев
    for entry in gs_api.get_scenario_entries(gs):
        scenario = scenarios_api.configure_scenario(scenario_definitions, entry)
        node = scenarios_api.get_node(entry)
        for transition in scenarios_api.get_transitions(scenario):
            node_matches = scenarios_api.get_node_from(transition) == node
            trigger_ok = scenarios_api.check_trigger(gs, transition)
            if node_matches and trigger_ok:
                logger.log(
                    f"Condition met for {entry["scenario_name"]}. Moving node {scenarios_api.get_node_from(transition)} -> {scenarios_api.get_node_to(transition)}",
                    log_type="scenario",
                )
                scenarios_api.apply_effect(gs, transition)
                scenarios_api.set_node(entry, scenarios_api.get_node_to(transition))
    resolver_api.resolve_intents(gs)

    gs_api.tick(gs)

    # Обновляем activity_entries
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
            logger.log(
                f"Stopped {entry["activity_name"]} (can_continue: {can_continue}, hold_ok: {hold_ok})",
                log_type="activity",
            )

    gs_api.set_activity_entries(gs, new_entries)

    logger.log(
        f"Activity entries: {gs_api.get_activity_entries(gs)}", log_type="status"
    )


def pick_activity(gs, definitions):
    allowed_entries = activities_api.get_allowed_activity_entries(gs, definitions)
    activities_ui_info = []
    for entry in allowed_entries:
        activity = activities_api.configure_activity(definitions, entry)
        activities_ui_info.append(
            (
                activities_api.get_activity_name(activity),
                activities_api.check_hold_required(activity),
            )
        )
    selected_index = ui.handle_input(activities_ui_info)
    entry_to_start = allowed_entries[selected_index]
    activities_api.add_activity_entry(gs, definitions, entry_to_start)


def main():
    game_state = gs_api.get_initial_gs()
    definitions = definitions_loader.load_definitions("content")

    scenarios_api.start_all_scenarios(game_state, definitions["scenarios"])
    while not gs_api.get_flag(game_state, "is_end"):
        ui.show_stats(game_state)
        if len(gs_api.get_activity_entries(game_state)) == 0:
            pick_activity(game_state, definitions["activities"])
        logger.log(f"------ TICK {gs_api.get_time(game_state)} ------", log_type="tick")
        sleep(0.15)
        update(game_state, definitions["activities"], definitions["scenarios"])
    print("--- GAME FINISHED ---")
    input("Press Enter to exit")


if __name__ == "__main__":
    main()
