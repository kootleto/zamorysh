from engine import activities_api
from gameplay.api import location

DIRECTIONS = {"north": (1, 0), "south": (-1, 0), "east": (0, 1), "west": (0, -1)}


@activities_api.with_param_space(location.get_directions)
def move(param=None):

    def tick_effect(gs):
        location.mod(gs, location.x, DIRECTIONS[param][0])
        location.mod(gs, location.y, DIRECTIONS[param][1])

    def can_continue(gs):
        return (
            0 <= location.get(gs, location.x) + DIRECTIONS[param][0] <= 5
            and 0 <= location.get(gs, location.y) + DIRECTIONS[param][1] <= 60
        )

    return activities_api.base_activity(
        tick_effect, can_continue, name=f"move to {param}"
    )


activities = [move]
