from engine import activities_api
from gameplay.api import location

DIRECTIONS = {"север": (0, 1), "юг": (0, -1), "восток": (1, 0), "запад": (-1, 0)}


@activities_api.with_param_space(location.get_directions)
def move(param=None):

    def tick_effect(gs):
        location.mod(gs, location.X, DIRECTIONS[param][0])
        location.mod(gs, location.Y, DIRECTIONS[param][1])

    def can_continue(gs):
        return (
            location.WEST_BORDER
            <= location.get(gs, location.X) + DIRECTIONS[param][0]
            <= location.EAST_BORDER
            and location.SOUTH_BORDER
            <= location.get(gs, location.Y) + DIRECTIONS[param][1]
            <= location.NORTH_BORDER
        )

    return activities_api.base_activity(
        tick_effect, can_continue, True, name=f"пойти на {param}"
    )


ACTIVITIES = [move]
