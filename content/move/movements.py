from engine import activities_api, data_api
from gameplay.api import location, floors
from gameplay.api.location import Place
from interface import ui

DIRECTIONS = {"север": (0, 1), "юг": (0, -1), "восток": (1, 0), "запад": (-1, 0)}


@activities_api.with_params_space(direction=location.get_directions)
@activities_api.on_finish(
    lambda gs, entry: ui.display_at(gs, f"Вы пошли на {entry["params"]["direction"]}.")
)
def move(params):

    direction = data_api.get_params(params, "direction")

    def tick_effect(gs):
        location.mod(gs, location.X, DIRECTIONS[direction][0])
        location.mod(gs, location.Y, DIRECTIONS[direction][1])

    def can_continue(gs):
        return (
            location.WEST_BORDER
            <= location.get(gs, location.X) + DIRECTIONS[direction][0]
            <= location.EAST_BORDER
            and location.SOUTH_BORDER
            <= location.get(gs, location.Y) + DIRECTIONS[direction][1]
            <= location.NORTH_BORDER
            and not (
                location.get_place(gs) == Place.UNIVERSITY
                and floors.get(gs, floors.FLOOR) != 1
                and floors.get(gs, floors.CLASSROOM) == 0
            )
        )

    return activities_api.base_activity(
        tick_effect, can_continue, True, name=f"пойти на {direction}"
    )


ACTIVITIES = [move]
