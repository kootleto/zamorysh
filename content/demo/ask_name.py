from engine import scenarios_api
from interface import ui


def ask_name():

    async def display_a_lot():
        alphabet = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
        alphabet.append("->")
        letter = ""
        word = ""
        while letter != "->" or not word:
            word += letter
            if not word:
                message = "Введите ваше имя"
            else:
                message = word
            letter = await ui.ask_option(alphabet, message, cols=10)
        ui.display(word)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(
                0,
                1,
                True,
                display_a_lot,
            )
        ]
    )


SCENARIOS = [ask_name]
