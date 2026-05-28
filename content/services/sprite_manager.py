from content import other_endings
from engine import gs_api, scenarios_api
from gameplay.api import scenes, vitals

ENDING_CONDITIONS = [
    other_endings.breakdown_ending_trigger,
    other_endings.tired_ending_trigger,
    other_endings.rich_ending_trigger,
    other_endings.social_ending_trigger,
    other_endings.clever_ending_trigger,
]


def sprite_manager(activity_definitions):
    def update_sprite(gs):
        if "sleep" in gs_api.get_active_tags(gs, activity_definitions):
            scenes.set_sprite(gs, "sleep.png")
        else:
            fatigue_critical = vitals.get(gs, vitals.FATIGUE) >= 75
            sleepiness_critical = vitals.get(gs, vitals.SLEEPINESS) >= 80
            mental_critical = vitals.get(gs, vitals.MENTAL) <= 25

            if not any([fatigue_critical, sleepiness_critical, mental_critical]):
                scenes.set_sprite(gs, "idle.png")
            else:
                conditions = [f(gs) for f in ENDING_CONDITIONS]
                if any(conditions):
                    return

                file_parts = []
                if fatigue_critical:
                    file_parts.append("tired")
                if sleepiness_critical:
                    file_parts.append("sleepy")
                if mental_critical:
                    file_parts.append("mental")
                file_name = "_".join(file_parts) + ".png"
                scenes.set_sprite(gs, file_name)

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, True, update_sprite)]
    )


SCENARIOS = [sprite_manager]
