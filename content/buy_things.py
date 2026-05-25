from engine import activities_api
from gameplay.activity_wrappers import single_tick_activity
from gameplay.api import location, time
from gameplay.api import vitals, stats
from gameplay.api.location import Place
from interface import ui

SURF_MENU = {
    "Латте": 9,
    "Американо": 8,
    "Капучино": 11,
}

SURF_LUCKY = {"Раф кокосовая свежесть на миндальном молоке с инжиром": 19}

ANOTHER_MENU = {
    "Латте": 8,
    "Американо": 9,
    "Капучино": 12,
}

ANOTHER_LUCKY = {"Сырный латте с базиликом": 20}

CLUB_MENU = {
    "Коктейль <<Нулевая аффиксация>>": 25,
    "Коктейль <<Singularia Tantum>>": 21,
    "Виски": 20,
}

CLUB_LUCKY = {"Коктейль <<Универсальная дробилка>>": 30}


def _render_menu_item(product, price):
    return f"{product} | {price} кредит{"ов" if not (price > 20 and price % 10 == 1) else ""}"


def _get_menu(menu, special, show_special=False):
    menu = [_render_menu_item(product, price) for product, price in menu.items()]
    special = [_render_menu_item(product, price) for product, price in special.items()]
    if show_special:
        menu.extend(special)
    return menu


def read_menu_surf(state=None):
    def tick_effect(gs):
        menu_lines = [
            "Добро пожаловать в Surf Coffee!",
            "На данный момент в меню доступны следующие позиции:",
        ]
        menu_lines.extend(
            _get_menu(SURF_MENU, SURF_LUCKY, time.get_minute(gs) % 2 == 0)
        )

        ui.display(*menu_lines, sep="\n")

    def can_continue(gs):
        return (
            6 < time.get_hour(gs) < 23 and location.get_place(gs) == Place.SURF_COFFEE
        )

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect=tick_effect,
            can_continue=can_continue,
            name="прочитать меню",
        ),
        state,
    )


def buy_drink_surf(hold_required=False, state=None):

    async def tick_effect(gs):
        menu = _get_menu(SURF_MENU, SURF_LUCKY, time.get_minute(gs) % 2 == 1)
        index = menu.index(
            await ui.ask_option(
                menu,
                "Выберите напиток",
                cols=2,
            )
        )
        if index == 0 and stats.get(gs, stats.MONEY) > 9:
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            vitals.mod(gs, vitals.MENTAL, +15)
            stats.mod(gs, stats.MONEY, -9)
            ui.display(
                "Вы купили латте. Сахар в нем делает вас довольнее, но вам все еще хочется спать!"
            )
        elif index == 1 and stats.get(gs, stats.MONEY) > 7:
            stats.mod(gs, stats.MONEY, -8)
            vitals.mod(gs, vitals.SLEEPINESS, -15)
            ui.display(
                "Вы знаете, как хорошо бодрит американо... Но он такой горький! Вас это совсем не радует."
            )
        elif index == 2 and stats.get(gs, stats.MONEY) > 10:
            vitals.mod(gs, vitals.FATIGUE, -15)
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            stats.mod(gs, stats.MONEY, -11)
            ui.display("Капучино всегда помогает вам от усталости!")
        elif index == 3 and stats.get(gs, stats.MONEY) > 18:
            vitals.mod(gs, vitals.FATIGUE, -10)
            vitals.mod(gs, vitals.SLEEPINESS, -10)
            vitals.mod(gs, vitals.MENTAL, +10)
            ui.display(
                "Ваша любимая позиция в сезонном меню... Кажется, что спасает от всего!"
            )
        else:
            ui.display("Кажется, вы слишком бедны для вашего выбора... Подумайте еще.")

    def can_continue(gs):
        return stats.get(gs, stats.MONEY) > 8 and (
            (location.get_place(gs) == Place.SURF_COFFEE) and 6 < time.get_hour(gs) < 23
        )

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required,
            name="купить кофе",
        ),
        state,
    )


def read_menu_another(state=None):
    def tick_effect(gs):
        menu_lines = [
            "Добро пожаловать в Другую кофейню!",
            "На данный момент в меню доступны следующие позиции:",
        ]
        menu_lines.extend(
            _get_menu(ANOTHER_MENU, ANOTHER_LUCKY, time.get_minute(gs) % 2 == 0)
        )

        ui.display(*menu_lines, sep="\n")

    def can_continue(gs):
        return (
            6 < time.get_hour(gs) < 23
            and location.get_place(gs) == Place.ANOTHER_COFFEE
        )

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect=tick_effect,
            can_continue=can_continue,
            name="прочитать меню",
        ),
        state,
    )


def buy_drink_another(hold_required=False, state=None):

    async def tick_effect(gs):
        menu = _get_menu(ANOTHER_MENU, ANOTHER_LUCKY, time.get_minute(gs) % 2 == 1)
        index = menu.index(
            await ui.ask_option(
                menu,
                "Выберите напиток",
                cols=2,
            )
        )

        if index == 0 and stats.get(gs, stats.MONEY) > 7:
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            vitals.mod(gs, vitals.MENTAL, +15)
            stats.mod(gs, stats.MONEY, -9)
            ui.display(
                "Вы купили латте. Сахар в нем делает вас довольнее, но вам все еще хочется спать!"
            )
        elif index == 1 and stats.get(gs, stats.MONEY) > 8:
            stats.mod(gs, stats.MONEY, -8)
            vitals.mod(gs, vitals.SLEEPINESS, -15)
            ui.display(
                "Вы знаете, как хорошо бодрит американо... Но он такой горький! Вас это совсем не радует."
            )
        elif index == 2 and stats.get(gs, stats.MONEY) > 11:
            vitals.mod(gs, vitals.FATIGUE, -15)
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            stats.mod(gs, stats.MONEY, -11)
            ui.display("Капучино всегда помогает вам от усталости!")
        elif index == 3 and stats.get(gs, stats.MONEY) > 19:
            vitals.mod(gs, vitals.FATIGUE, -10)
            vitals.mod(gs, vitals.SLEEPINESS, -10)
            vitals.mod(gs, vitals.MENTAL, +10)
            ui.display(
                "Ваша любимая позиция в сезонном меню... Кажется, что спасает от всего!"
            )
        else:
            ui.display("Похоже, вам не хватает. Выберите что-то еще?")

    def can_continue(gs):
        return stats.get(gs, stats.MONEY) > 8 and (
            (location.get_place(gs) == Place.ANOTHER_COFFEE)
            and 6 < time.get_hour(gs) < 23
        )

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required,
            name="купить кофе",
        ),
        state,
    )


def read_menu_club(state=None):
    def tick_effect(gs):
        menu_lines = [
            "Добро пожаловать в Другую кофейню!",
            "На данный момент в меню доступны следующие позиции:",
        ]
        menu_lines.extend(
            _get_menu(CLUB_MENU, CLUB_LUCKY, time.get_minute(gs) % 2 == 0)
        )

        ui.display(*menu_lines, sep="\n")

    def can_continue(gs):
        return (
            21 < time.get_hour(gs) <= 23 or 0 <= time.get_hour(gs) <= 5
        ) and location.get_place(gs) == Place.CLUB

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect=tick_effect,
            can_continue=can_continue,
            name="прочитать меню",
        ),
        state,
    )


def buy_drink_club(hold_required=False, state=None):

    async def tick_effect(gs):
        menu = _get_menu(CLUB_MENU, CLUB_LUCKY, time.get_minute(gs) % 2 == 1)
        index = menu.index(
            await ui.ask_option(
                menu,
                "Выберите напиток",
                cols=2,
            )
        )

        if index == 0 and stats.get(gs, stats.MONEY) > 24:
            vitals.mod(gs, vitals.SLEEPINESS, +15)
            vitals.mod(gs, vitals.MENTAL, +15)
            stats.mod(gs, stats.MONEY, -25)
            ui.display(
                "От этого коктейля вы всегда расслабляетесь и начинаете клевать носом... Но он ужасно вкусный."
            )
        elif index == 1 and stats.get(gs, stats.MONEY) > 20:
            stats.mod(gs, stats.MONEY, -21)
            vitals.mod(gs, vitals.MENTAL, +5)
            stats.mod(gs, stats.SOCIAL, +15)
            ui.display("От этого напитка вас так и тянет общаться с людьми!")
        elif index == 2 and stats.get(gs, stats.MONEY) > 19:
            vitals.mod(gs, vitals.MENTAL, +2)
            vitals.mod(gs, vitals.SLEEPINESS, +2)
            stats.mod(gs, stats.MONEY, -20)
            stats.mod(gs, stats.KNOWLEDGE, +10)
            ui.display(
                "Виски напоминает вам о чувстве долга, и вы снова открываете конспекты и учитесь..."
            )
        elif index == 3 and stats.get(gs, stats.MONEY) > 29:
            vitals.mod(gs, vitals.FATIGUE, +10)
            vitals.mod(gs, vitals.SLEEPINESS, +50)
            vitals.mod(gs, vitals.MENTAL, +10)
            ui.display("Голова потяжелела...Это было слишком крепко.")
        else:
            ui.display("Вам это не по карману.")

    def can_continue(gs):
        return stats.get(gs, stats.MONEY) > 8 and (
            (location.get_place(gs) == Place.CLUB) and 6 < time.get_hour(gs) < 23
        )

    return single_tick_activity(
        activities_api.base_activity(
            tick_effect,
            can_continue,
            hold_required,
            name="купить коктейль",
        ),
        state,
    )


ACTIVITIES = [
    read_menu_surf,
    buy_drink_surf,
    read_menu_another,
    buy_drink_another,
    read_menu_club,
    buy_drink_club,
]
