from engine import gs_api, scenarios_api
from gameplay.api import scenes, location, time, floors

LOCATION_SCENES = {
    location.Place.ANOTHER_COFFEE: {"default": "another_coffee.jpg"},
    location.Place.CLUB: {"default": "club.jpg"},
    location.Place.HOME: {"day": "home_day.jpg", "night": "home_night.jpg"},
    location.Place.METRO: {"default": "metro.jpg"},
    location.Place.OUTSIDE: {"day": "outside_day.jpg", "night": "outside_night.jpg"},
    location.Place.PARK: {"day": "park_day.jpg", "night": "park_night.jpg"},
    location.Place.SURF_COFFEE: {"default": "surf_coffee.jpg"},
}


def scene_manager(activity_definitions):
    def update_scene(gs):
        if "sleep" in gs_api.get_active_tags(gs, activity_definitions):
            scenes.set_scene(gs, "sleep.jpg")
        elif location.get_place(gs) in LOCATION_SCENES:
            is_day = 7 <= time.get_hour(gs) <= 17
            config = LOCATION_SCENES[location.get_place(gs)]
            if "day" in config and is_day:
                scenes.set_scene(gs, config["day"])
            elif "night" in config and not is_day:
                scenes.set_scene(gs, config["night"])
            elif "default" in config:
                scenes.set_scene(gs, config["default"])
        elif location.get_place(gs) == location.Place.UNIVERSITY:
            if floors.get(gs, floors.CLASSROOM) == 0:
                scenes.set_scene(gs, "university_out.jpg")
            else:
                scenes.set_scene(gs, "university_in.jpg")

    return scenarios_api.base_scenario(
        [scenarios_api.base_transition(0, 0, True, update_scene)]
    )


SCENARIOS = [scene_manager]
