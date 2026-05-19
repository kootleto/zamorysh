from engine import activities_api


def process_auto_start(gs, activity_definitions):
    for definition in activity_definitions.values():
        if activities_api.check_auto_start(definition):
            activities_api.start_activity_by_definition(
                gs, activity_definitions, definition
            )
