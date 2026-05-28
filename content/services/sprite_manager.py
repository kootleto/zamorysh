from engine import gs_api, scenarios_api
from gameplay.api import scenes


def sprite_manager(activity_definitions):
    def update_sprite(gs):
        if "sleep" in gs_api.get_active_tags(gs, activity_definitions):
            scenes.set_sprite(gs, "sleep.png")
        else:
            scenes.set_sprite(gs, "idle.png")

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, True, update_sprite)]
    )


SCENARIOS = [sprite_manager]
