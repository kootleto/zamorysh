import datetime

from engine import scenarios_api
from gameplay.api import location, floors, quests, time
from interface import ui


def pass_quest():
    def check_start(gs):
        return location.get_place(gs) == location.Place.UNIVERSITY

    def start(gs):
        quests.set_status(gs, "pass", quests.Status.ACTIVE)
        ui.display(
            "Вам нужно сделать пропуск в здание Вышки за сегодняшний день."
            "\nДля этого сделайте фотографию в фотостудии рядом с клубом, "
            "распечатайте заявление в копировальном центре (107) и отнесите всё в учебный офис (405)."
            "\nДокументы можно приносить в любом порядке."
        )

    def check_print(gs):
        return floors.get(gs, floors.CLASSROOM) == 107

    def print_doc():
        ui.display("Вы распечатали заявление! Теперь отнесите его в учофис.")

    def check_photo(gs):
        return location.get(gs, location.X) == 41 and location.get(gs, location.Y) == 4

    def take_photo():
        ui.display("Вы сделали фотографию! Теперь отнесите её в учофис.")

    def check_office(gs):
        return floors.get(gs, floors.CLASSROOM) == 405

    def office():
        ui.display("Вы занесли часть документов, спасибо!")

    def finish(gs):
        ui.display("Теперь у вас есть пропуск!")
        quests.finish(gs, "pass")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, "start", check_start, start),
            scenarios_api.base_transition("start", "print", check_print, print_doc),
            scenarios_api.base_transition("start", "photo", check_photo, take_photo),
            scenarios_api.base_transition(
                "print", "everything", check_photo, take_photo
            ),
            scenarios_api.base_transition(
                "photo", "everything", check_print, print_doc
            ),
            scenarios_api.base_transition("print", "print_done", check_office, office),
            scenarios_api.base_transition("photo", "photo_done", check_office, office),
            scenarios_api.base_transition(
                "everything", "everything_done", check_office, finish
            ),
            scenarios_api.base_transition(
                "print_done", "everything", check_photo, take_photo
            ),
            scenarios_api.base_transition(
                "photo_done", "everything", check_print, print_doc
            ),
        ]
    )


def incomplete_pass():
    def check_incomplete(gs):
        return (
            time.get_time(gs) == datetime.time(23, 59)
            and quests.get_status(gs, "pass") != quests.Status.FINISHED
        )

    def locking(gs):
        location.lock(gs, location.Place.UNIVERSITY, "incomplete_pass")
        ui.display("Вы вспомнили, что не сделали пропуск...")

    def next_day(gs):
        return time.get_time(gs) == datetime.time(23, 59)

    def restart(gs):
        quests.set_status(gs, "pass", quests.Status.INACTIVE)
        location.unlock(gs, location.Place.UNIVERSITY, "incomplete_pass")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, check_incomplete, locking),
            scenarios_api.base_transition(1, 0, next_day, restart),
        ]
    )


SCENARIOS = [pass_quest, incomplete_pass]
