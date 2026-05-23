import random

from interface import ui


async def anagram():
    ui.display("Игра «Анаграммы»!")
    my_list = ["морфология", "фонетика", "синтаксис", "прагматика", "семантика"]
    slovo = random.choice(my_list)
    slovo_list = list(slovo)
    abrakadabra = random.sample(slovo_list, len(slovo_list))
    ui.display(abrakadabra)
    guess = (await ui.prompt("Введите расшифровку анаграммы: ")).lower()
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

        guess = (await ui.prompt("Введите букву: ")).lower()

        if guess in guessed_letters:
            ui.display("Вы уже вводили эту букву.")
        elif guess in word:
            guessed_letters.append(guess)
            ui.display("Верно!")
        else:
            attempts -= 1
            guessed_letters.append(guess)
            ui.display(f"Неверно! Осталось попыток: {attempts}")

    if attempts == 0:
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
        guess = await ui.prompt("Введите 4-значное число: ")
        ui.display(f"Ваше предположение: {guess}")
        guess = list(guess)
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
        try:

            guess = int(await ui.prompt("Введите ваше число: "))
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

        except ValueError:
            ui.display("Ошибка: пожалуйста, введите целое число.")


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
        player_choice = (
            (await ui.prompt("Выберите предмет (камень, ножницы, бумага): "))
            .lower()
            .strip()
        )

        # Проверка корректности ввода
        if player_choice not in ["камень", "ножницы", "бумага"]:
            ui.display("Ошибка: введите камень, ножницы или бумага")
            ui.display()
            continue

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

    ui.display("Языки:")
    for i, (lang, _) in enumerate(selected, 1):
        ui.display(f"{i}. {lang}")

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

    ui.display("Семьи:")
    ui.display("а.", families[0])
    ui.display("б.", families[1])
    ui.display("в.", families[2])

    answer = await ui.prompt("Ваш ответ (пример: 1а,2б,3в): ")

    correct = 0
    pairs = answer.replace(" ", "").split(",")

    for pair in pairs:
        if len(pair) == 2:
            num = int(pair[0]) - 1
            letter = pair[1]

            if letter == "а":
                family_by_letter = families[0]
            elif letter == "б":
                family_by_letter = families[1]
            elif letter == "в":
                family_by_letter = families[2]
            else:
                continue

            if selected[num][1] == family_by_letter:
                correct += 1

    if correct == 3:
        ui.display("Правильно")
        return True
    else:
        await ui.display("Неправильно")
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
