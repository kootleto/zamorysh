import random

from interface import ui

ALPHABET = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
DIGITS = list("0123456789")


async def ask_word(message):
    options = ALPHABET.copy()
    letter = ""
    word = ""
    while letter != "->":
        word += letter
        if not word:
            button_message = message
        else:
            button_message = word
        letter = await ui.ask_option(options, button_message, cols=10)
        if "->" not in options:
            options.append("->")
    return word.lower()


async def ask_number(message, length, max_number=None, allow_escape=False):
    options = DIGITS.copy()

    number = ""
    for i in range(length):
        if not number:
            button_message = message
        else:
            button_message = str(number)
            if allow_escape and "->" not in options:
                options.append("->")
        option = await ui.ask_option(options, button_message, cols=5)
        if option == "->":
            break
        number += str(option)
        if max_number and int(number) >= max_number:
            break
    return number


async def anagram():
    ui.display("Игра «Анаграммы»!")
    my_list = ["морфология", "фонетика", "синтаксис", "прагматика", "семантика"]
    slovo = random.choice(my_list)
    slovo_list = list(slovo)
    abrakadabra = random.sample(slovo_list, len(slovo_list))
    ui.display("".join(abrakadabra))
    guess = await ask_word("Введите расшифровку анаграммы")
    if guess in my_list:
        ui.display("Правильно!")
        return True
    else:
        ui.display("Неправильно!")
        return False


async def hangman():
    ui.display("Игра «Виселица»!")
    words = ["синтаксис", "морфология", "лингвистика", "семантика", "прагматика"]
    word = random.choice(words)
    guessed_letters = []
    attempts = 6

    ui.display("Угадайте слово: ")

    while attempts > 0:
        display_word = [letter if letter in guessed_letters else "_" for letter in word]
        ui.display(" ".join(display_word))

        if "_" not in display_word:
            ui.display("Поздравляем! Вы выиграли")
            return True

        guess = (await ui.ask_option(ALPHABET, "Введите букву", cols=10)).lower()

        if guess in guessed_letters:
            ui.display("Вы уже вводили эту букву.")
        elif guess in word:
            guessed_letters.append(guess)
            ui.display("Верно!")
        else:
            attempts -= 1
            guessed_letters.append(guess)
            ui.display(f"Неверно! Осталось попыток: {attempts}")

    ui.display(f"Игра окончена! Слово было: {word}")
    return False


async def bulls_and_cows():
    ui.display("Игра «Быки и коровы»!")
    secret = random.sample("123456789", 4)
    attempts = 0
    ui.display(
        "Угадай число! Я даю тебе подсказки в виде «быков» (цифра угадана и стоит на месте) и «коров» (цифра угадана, но стоит не на месте)."
    )

    while True:
        if attempts > 10:
            ui.display("Попытки закончились, вы проиграли.")
            return False
        guess = await ask_number("Введите 4-значное число", 4)
        ui.display(f"Ваше предположение: {guess}")
        guess = list(str(guess))
        if len(guess) != 4:
            continue
        attempts += 1
        bulls = 0
        cows = 0

        for i in range(4):
            if guess[i] == secret[i]:
                bulls += 1
            elif guess[i] in secret:
                cows += 1

        ui.display(f"Быков: {bulls}, Коров: {cows}")

        if bulls == 4:
            ui.display(f"Победа за {attempts} попыток!")
            return True


async def ugaiday_chislo():
    ui.display("Игра «Угадай число»!")
    ui.display("Загадано число от 1 до 100. Попробуйте угадать.")

    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(
            await ask_number("Введите ваше число", 3, allow_escape=True, max_number=100)
        )
        attempts += 1

        if guess < 1 or guess > 100:
            ui.display("Пожалуйста, введите число от 1 до 100.")
            continue

        if guess < secret_number:
            ui.display("Больше!")
        elif guess > secret_number:
            ui.display("Меньше!")
        else:
            ui.display(
                f"Поздравляю! Вы угадали число {secret_number} за {attempts} попыток!"
            )
            return True


async def kamen_nozhnitsy_bumaga():
    ui.display("Игра «Камень-Ножницы-Бумага»!")
    ui.display("Побеждает тот, кто первым выиграет 3 раунда.")
    ui.display()

    player_wins = 0
    computer_wins = 0
    round_num = 1

    win_rules = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}

    while player_wins < 3 and computer_wins < 3:
        ui.display("Раунд", round_num)
        ui.display("Счёт:", player_wins, "-", computer_wins)

        # Ввод пользователя
        options = ["камень", "ножницы", "бумага"]

        player_choice = await ui.ask_option(options, "Выберите предмет")

        # Выбор компьютера
        computer_choice = random.choice(["камень", "ножницы", "бумага"])

        ui.display("Ваш выбор:", player_choice)
        ui.display("Выбор противника:", computer_choice)

        # Определение победителя раунда
        if player_choice == computer_choice:
            ui.display("Ничья")
        elif win_rules[player_choice] == computer_choice:
            ui.display("Вы выиграли раунд")
            player_wins += 1
        else:
            ui.display("Вы проиграли раунд")
            computer_wins += 1

        ui.display()
        round_num += 1

    ui.display("Игра окончена")
    ui.display("Финальный счёт: ", player_wins, "-", computer_wins)
    if player_wins == 3:
        ui.display("Вы выиграли")
        return True
    else:
        ui.display("Вы проиграли")
        return False


async def yazyki_i_semi():
    ui.display("Игра «Языки и семьи»!")
    languages = {
        "русский": "индоевропейская",
        "английский": "индоевропейская",
        "китайский": "сино-тибетская",
        "японский": "японо-рюкюская",
        "арабский": "афразийская",
        "турецкий": "тюркская",
        "финский": "уральская",
    }

    selected = random.sample(list(languages.items()), 3)

    families = []
    for _, fam in selected:
        families.append(fam)

    if len(set(families)) < 3:
        all_families = list(set(languages.values()))
        while len(set(families)) < 3:
            extra = random.choice(all_families)
            if extra not in families:
                families.append(extra)

    random.shuffle(families)

    answer = []
    for i in range(3):
        family = await ui.ask_option(
            families, f"К какой семье относится {selected[i][0]} язык?"
        )
        answer.append(family)

    correct = 0

    for i in range(3):
        if selected[i][1] == answer[i]:
            correct += 1

    if correct == 3:
        ui.display("Правильно")
        return True
    else:
        ui.display("Неправильно")
        return False


def main():
    print("Доступные игры:")
    print("1. Угадай число")
    print("2. Камень-ножницы-бумага")
    print("3. Языки и их семьи")
    print("")

    while True:
        choice = input("Введи номер игры ")

        if choice == "1":
            ugaiday_chislo()
        elif choice == "2":
            kamen_nozhnitsy_bumaga()
        elif choice == "3":
            yazyki_i_semi()
        elif choice == "4":
            anagram()
        elif choice == "5":
            hangman()
        elif choice == "6":
            bulls_and_cows()


# Запуск меню
if __name__ == "__main__":
    main()
