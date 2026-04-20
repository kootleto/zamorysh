from engine import gs_api, activities_api
from gameplay.api import location


@activities_api.with_param_space(location.get_directions)
def move(param=None):

    def tick_effect(gs):
        direction = param
        if direction == "east":
            location.mod(gs, location.y, 1)
        elif direction == "west":
            location.mod(gs, location.y, -1)
        elif direction == "north":
            location.mod(gs, location.x, 1)
        elif direction == "south":
            location.mod(gs, location.x, -1)

    def can_continue(gs):


    return activities_api.base_activity(
tick_effect, can_continue, name=f"move to {param}"
    )


activities = [move]
