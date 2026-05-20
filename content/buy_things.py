from engine import activities_api
from gameplay.activity_wrappers import single_tick_activity
from gameplay.api import location, time
from gameplay.api import vitals, stats
from gameplay.api.location import Place
from interface import ui


def buy_drink1(hold_required=False, state=None):
    # def can_continue(gs):
    # return stats.get(gs, stats.money) < 0
    # state = state_api.init_defaults(state, counter=1)

    async def tick_effect(gs):
        # ui.display("Купить латте? (Нажмите a + Enter)")
        # ui.display("Купить американо?  (Нажмите b + Enter)")
        ui.display("Введите букву позиции в меню + Enter")
        vv = await ui.prompt("Выбирайте: ")
        if vv == "a" and stats.get(gs, stats.MONEY) > 9:
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            vitals.mod(gs, vitals.MENTAL, +15)
            stats.mod(gs, stats.MONEY, -9)
            ui.display(
                "Вы купили латте. Сахар в нем делает вас довольнее, но вам все еще хочется спать!"
            )
        if vv == "b" and stats.get(gs, stats.MONEY) > 7:
            stats.mod(gs, stats.MONEY, -8)
            vitals.mod(gs, vitals.SLEEPINESS, -15)
            ui.display(
                "Вы знаете, как хорошо бодрит американо... Но он такой горький! Вас это совсем не радует."
            )
        if vv == "c" and stats.get(gs, stats.MONEY) > 10:
            vitals.mod(gs, vitals.FATIGUE, -15)
            vitals.mod(gs, vitals.SLEEPINESS, -2)
            stats.mod(gs, stats.MONEY, -11)
            ui.display("Капучино всегда помогает вам от усталости!")
        if vv == "d" and stats.get(gs, stats.MONEY) > 18:
            vitals.mod(gs, vitals.FATIGUE, -10)
            vitals.mod(gs, vitals.SLEEPINESS, -10)
            vitals.mod(gs, vitals.MENTAL, +10)
            ui.display(
                "Ваша любимая позиция в сезонном меню... Кажется, что спасает от всего!"
            )
        else:
            ui.display("Кажется, вы слишком бедны для вашего выбора...Подумайте еще.")

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


def read_menu(state=None):
    def tick_effect(gs):
        ui.display("Добро пожаловать в Surf Coffee!")
        ui.display("На данный момент в меню доступны следующие позиции:")
        ui.display("a. Латте | 9 кредитов")
        ui.display("b. Американо | 8 кредитов")
        ui.display("c. Капучино | 11 кредитов")
        if time.get_minute(gs) % 2 == 0:
            ui.display(
                "d. Раф кокосовая свежесть на миндальном молоке с инжиром | 19 кредитов"
            )

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


ACTIVITIES = [read_menu, buy_drink1]
