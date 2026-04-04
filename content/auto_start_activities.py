from engine import activities_api
from engine import scenarios_api


def auto_start_activities(activity_definitions):
    def start(gs):
        for definition in activity_definitions.values():
            if activities_api.check_auto_start(definition):
                entry = activities_api.create_activity_entry(definition)
                activities_api.start_activity(gs, activity_definitions, entry)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 1, True, start)]
    )


scenarios = [auto_start_activities]
