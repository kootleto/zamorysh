from engine import activities_api


def process_auto_start(gs, activity_definitions):
    for definition in activity_definitions.values():
        if activities_api.check_auto_start(definition):
            entry = activities_api.create_activity_entry(definition)
            activities_api.start_activity(gs, activity_definitions, entry)
