from engine import gs_api, activities_api
from interface import ui
from gameplay.api import location


def move():
    def tick_effect(gs):
        for i in range(len(location.get_directions(gs))):
            ui.display(i, location.get_directions(gs)[i])

        selected_direction = int(ui.prompt("Введите номер направления: "))
        if location.get_directions(gs)[selected_direction] == "north":
            location.mod(gs, location.ycoordinate, 1)
        elif location.get_directions(gs)[selected_direction] == "south":
            location.mod(gs, location.ycoordinate, -1)
        elif location.get_directions(gs)[selected_direction] == "east":
            location.mod(gs, location.xcoordinate, 1)
        elif location.get_directions(gs)[selected_direction] == "west":
            location.mod(gs, location.xcoordinate, -1)

    def can_continue():
        return True

    return activities_api.base_activity(tick_effect, can_continue, True, name="move")
