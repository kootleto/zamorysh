import random


def ugaiday_chislo():
    print("Игра «Угадай число»!")
    print("Я загадал число от 1 до 100. Попробуй угадать.")

    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:

            guess = int(input("\nВведите ваше число: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Пожалуйста, введите число от 1 до 100.")
                continue

            if guess < secret_number:
                print("Больше!")
            elif guess > secret_number:
                print("Меньше!")
            else:
                print(
                    f"\nПоздравляю! Вы угадали число {secret_number} за {attempts} попыток!"
                )
                break

        except ValueError:
            print("Ошибка: пожалуйста, введите целое число.")


def kamen_nozhnitsy_bumaga():
    print("Игра Камень-Ножницы-Бумага")
    print("Побеждает тот, кто первым выиграет 3 раунда.")
    print()

    player_wins = 0
    computer_wins = 0
    round_num = 1

    win_rules = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}

    while player_wins < 3 and computer_wins < 3:
        print("Раунд", round_num)
        print("Счёт: Вы", player_wins, "-", computer_wins, "Я")

        # Ввод пользователя
        player_choice = (
            input("Выбери предмет (камень, ножницы, бумага): ").lower().strip()
        )

        # Проверка корректности ввода
        if player_choice not in ["камень", "ножницы", "бумага"]:
            print("Ошибка: введи камень, ножницы или бумага")
            print()
            continue

        # Выбор компьютера
        computer_choice = random.choice(["камень", "ножницы", "бумага"])

        print("Твой выбор:", player_choice)
        print("Мой выбор:", computer_choice)

        # Определение победителя раунда
        if player_choice == computer_choice:
            print("Ничья")
        elif win_rules[player_choice] == computer_choice:
            print("Ты выиграл раунд")
            player_wins += 1
        else:
            print("Я выиграл раунд")
            computer_wins += 1

        print()
        round_num += 1

    print("Игра окончена")
    print("Финальный счёт: Вы", player_wins, "-", computer_wins, "Я")
    if player_wins == 3:
        print("Ты выиграл игру")
    else:
        print("Я выиграл игру")


def yazyki_i_semi():
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

    print("Языки:")
    for i, (lang, _) in enumerate(selected, 1):
        print(f"{i}. {lang}")

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

    print("\nСемьи:")
    print("а.", families[0])
    print("б.", families[1])
    print("в.", families[2])

    answer = input("\nТвой ответ (пример: 1а,2б,3в): ")

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

    print("\nПравильно" if correct == 3 else "Неправильно")


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


# Запуск меню
if __name__ == "__main__":
    main()
