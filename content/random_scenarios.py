import random

from engine import scenarios_api, gs_api, data_api
from engine.data_api import init_fn
from gameplay.api import stats, vitals, location, time
from gameplay.api.location import Place
from interface import ui


def random_scenario_somewhere(events, hours, place, cooldown, state=None):
    def init():
        return {
            "minutes": random.randint(0, 9),
            "cooldown": random.randint(0, cooldown - 1),
        }

    state = init_fn(state, init)

    def tr(gs):
        return (
            location.get_place(gs) == place
            and time.get_hour(gs) in hours
            and time.get_minute(gs) % 10 == state["minutes"]
        )

    def eff(gs):
        chs = random.choice(events)
        state.update(init())
        chs(gs)

    def tr1(gs):
        return time.get_minute(gs) % cooldown != state["cooldown"]

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, tr, eff),
            scenarios_api.base_transition(1, 0, tr1, None),
        ]
    )


def random_scenario(state=None):
    def check_tick():
        return {"tick": random.randint(1, 3)}

    state = data_api.init_fn(state, check_tick)

    def ti(gs):
        return gs_api.get_time(gs) == state["tick"]

    def eff(gs):
        vitals.mod(gs, vitals.FATIGUE, +5)
        ui.display_at(gs, "Вы РАНДОМНО устали")

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, ti, eff),
        ]
    )


def random_university_day_scenario(state=None):

    def f1(gs):
        stats.mod(gs, stats.MONEY, +5)
        ui.display_at(gs, "Вы радуетесь тому, что нашли 5 кредитов под лестницей.")

    def f2(gs):
        vitals.mod(gs, vitals.SLEEPINESS, +1)
        ui.display_at(
            gs,
            "Одногруппник, сидящий рядом с вами, зевнул. Вы тоже зевнули и захотели спать.",
        )

    def f3(gs):
        vitals.mod(gs, vitals.MENTAL, -30)
        ui.display_at(
            gs, "Онет. Вы увидели свою оценку за домашку по Линде. Она меньше 4,7."
        )

    def f4(gs):
        stats.mod(gs, stats.KNOWLEDGE, +5)
        ui.display_at(
            gs,
            "Вы искали что-то в Википедии и случайно перешли по ссылке на статью языка тигринья. Вы чувствуете себя умнее.",
        )

    def f5(gs):
        ui.display_at(gs, "ВЫ ПРОИГРАЛИ")

    def f6(gs):
        stats.mod(gs, stats.SOCIAL, -10)
        ui.display_at(gs, "Вам пришлось говорить о СОПе с одногруппниками. Это тяжело.")

    def f7(gs):
        ui.display_at(
            gs,
            "Вы вспомнили, что не сделали домашку, дедлайн по которой был вчера. ААА!",
        )
        stats.mod(gs, stats.KNOWLEDGE, -5)
        vitals.mod(gs, vitals.MENTAL, -20)

    def f8(gs):
        if random.choice([True, False]):
            ui.display_at(gs, "Ваша одногруппница купила вам кофе! Как мило!")
        else:
            ui.display_at(gs, "Ваш одногруппник купил вам кофе! Как мило!")
        vitals.mod(gs, vitals.MENTAL, +5)
        vitals.mod(gs, vitals.SLEEPINESS, -5)

    hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    events = [f1, f2, f3, f4, f5, f6, f7, f8]
    place = Place.UNIVERSITY
    cooldown = 30
    return random_scenario_somewhere(events, hours, place, cooldown, state)


def random_home_day_scenario(state=None):
    def f1(gs):
        stats.mod(gs, stats.SOCIAL, -5)
        ui.display_at(gs, "Вы разбили любимую чашку. Жалко.")

    def f2(gs):
        stats.mod(gs, stats.MONEY, +2)
        ui.display_at(gs, "Вы нашли 2 кредита под подушкой.")

    def f3(gs):
        ui.display_at(gs, "Ничего не произошло")

    def f4(gs):
        vitals.mod(gs, vitals.SLEEPINESS, -10)
        stats.mod(gs, stats.KNOWLEDGE, -5)
        ui.display_at(
            gs,
            "Вы уснули лицом в стол, хотя собирались делать домашку... Это негативно скажется на учебе, но вы поспали",
        )

    def f5(gs):
        vitals.mod(gs, vitals.MENTAL, +5)
        ui.display_at(
            gs, "Вы решили пообнимать свою плюшевую птицу. Вам стало полегче."
        )

    def f6(gs):
        stats.mod(gs, stats.SOCIAL, +5)
        stats.mod(gs, stats.KNOWLEDGE, -5)
        ui.display_at(
            gs, "Вы проговорили в чате с одногруппниками вместо того, чтобы учить ЯРы."
        )

    def f7(gs):
        ui.display_at(
            gs,
            "Вы включили свой любимый плейлист с НТР и хорошо поботали. Правда, это было громко и соседи не оценили...",
        )
        stats.mod(gs, stats.KNOWLEDGE, +5)

    def f8(gs):
        ui.display_at(gs, "Never gonna give you up...")

    def f9(gs):
        vitals.mod(gs, vitals.SLEEPINESS, +10)
        ui.display_at(gs, "Вы чувствуете себя устало. Вам бы поспать...")

    def f10(gs):
        ui.display_at(
            gs,
            "Вода из стиральной машины резко стала капать на пол. Вы долго вытирали ее и так и не поняли, что случилось.",
        )
        vitals.mod(gs, vitals.FATIGUE, +7)
        vitals.mod(gs, vitals.MENTAL, -7)

    hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    events = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    place = Place.HOME
    cooldown = 25
    return random_scenario_somewhere(events, hours, place, cooldown, state)


def random_park_day_scenario(state=None):
    def f1(gs):
        vitals.mod(gs, vitals.MENTAL, -5)
        stats.mod(gs, stats.SOCIAL, +5)
        ui.display_at(
            gs, "Вы столкнулись с одногруппником. Вам пришлось разговаривать."
        )

    def f2(gs):
        ui.display_at(gs, "Вы наступили в лужу и простудились.")
        vitals.mod(gs, vitals.FATIGUE, -7)

    def f3(gs):
        ui.display_at(gs, "Вы встретили Ландера. Вам ужасно неловко.")
        stats.mod(gs, stats.SOCIAL, -5)
        vitals.mod(gs, vitals.MENTAL, -5)

    def f4(gs):
        ui.display_at(
            gs, "Вам всучили брошюрку о вреде алкоголя. Вы и не собирались..."
        )
        stats.mod(gs, stats.KNOWLEDGE, +5)

    def f5(gs):
        ui.display_at(gs, "Вы нашли траву и ПОТРОГАЛИ ее.")
        vitals.mod(gs, vitals.MENTAL, +15)
        vitals.mod(gs, vitals.FATIGUE, -10)

    def f6(gs):
        ui.display_at(
            gs,
            "Собака, гуляющая в парке, украла ваш студак. Пока вы бежали за ней и отнимали его, вы очень устали.",
        )
        vitals.mod(gs, vitals.FATIGUE, -5)

    def f7(gs):
        ui.display_at(
            gs,
            "Вода в парке очень красиво плещется. Вы засмотрелись на нее, и она убаюкала вас... ",
        )
        vitals.mod(gs, vitals.SLEEPINESS, +7)

    def f8(gs):
        ui.display_at(
            gs,
            "С вами завел беседу бомж. Вы рассказали ему о своей курсовой. Он расстроился и дал вам 5 рублей.",
        )
        stats.mod(gs, stats.MONEY, +5)

    def f9(gs):
        ui.display_at(
            gs,
            "Вы увидели уведомление от тгк <<на старой басманной все спокойно>> и обрадовались!",
        )
        vitals.mod(gs, vitals.MENTAL, +5)

    def f10(gs):
        ui.display_at(
            gs,
            "Солнце светило ярко, и вы решили поботать на природе... но ветер унес листы из вашего конспекта по дискре!",
        )
        stats.mod(gs, stats.KNOWLEDGE, -10)

    events = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    cooldown = 30
    place = Place.PARK

    return random_scenario_somewhere(events, hours, place, cooldown, state)


def random_park_night_scenario(state=None):
    def f1(gs):
        vitals.mod(gs, vitals.MENTAL, -5)
        ui.display_at(gs, "Фонарь резко заморгал. Вы испугались.")

    def f2(gs):
        ui.display_at(
            gs,
            "Огни бара напротив вас призывно мерцают, но вы не можете зайти внутрь из-за ваших дедлайнов.",
        )
        vitals.mod(gs, vitals.MENTAL, -4)

    def f3(gs):
        ui.display_at(
            gs,
            "Вы уютно устроились на скамейке и не заметили, как задремали на несколько секунд. Осторожно, это может быть опасно.",
        )
        vitals.mod(gs, vitals.FATIGUE, -2)
        vitals.mod(gs, vitals.SLEEPINESS, -2)
        vitals.mod(gs, vitals.MENTAL, -10)

    def f4(gs):
        ui.display_at(gs, "Здесь очень темно. Вам страшно и хочется уйти.")
        vitals.mod(gs, vitals.MENTAL, -7)

    def f5(gs):
        ui.display_at(
            gs,
            "Свет от фонарей так красиво ложится на воду... Вас очень обрадовал этот вид.",
        )
        vitals.mod(gs, vitals.MENTAL, +5)

    def f6(gs):
        ui.display_at(
            gs,
            "В темноте вы оставили какие-то важные записи на скамейке. (Вы не разглядели, какие.)",
        )
        stats.mod(gs, stats.KNOWLEDGE, -10)

    def f7(gs):
        ui.display_at(gs, "Упс! Ноут внезапно рарядился! Поботать не получилось...")
        stats.mod(gs, stats.KNOWLEDGE, -2)
        vitals.mod(gs, vitals.MENTAL, -2)

    def f8(gs):
        ui.display_at(
            gs,
            "Вам внезапно очень грустно... вы не спите ночью в парке... в одиночестве.",
        )
        vitals.mod(gs, vitals.MENTAL, -2)

    def f9(gs):
        ui.display_at(
            gs,
            "Вы качаетесь на качелях, и они зловеще скрипят... Зато качели наконец-то не заняты!",
        )
        vitals.mod(gs, vitals.MENTAL, +1)

    def f10(gs):
        ui.display_at(
            gs,
            "Мимо вас пробегает маленькая крыса... Вы не понимаете, чувствуете ли вы жалость или дискомфорт.",
        )
        stats.mod(gs, stats.SOCIAL, +1)

    events = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    hours = [0, 1, 2, 3, 4, 5, 6, 22, 23]
    cooldown = 20
    place = Place.PARK

    return random_scenario_somewhere(events, hours, place, cooldown, state)


def random_metro_day_scenario(state=None):
    def f1(gs):
        stats.mod(gs, stats.SOCIAL, -5)
        ui.display_at(gs, "С вами кто-то столкнулся в метро. Ауч.")

    def f2(gs):
        stats.mod(gs, stats.MONEY, -5)
        ui.display_at(
            gs, "Вы забыли карту москвича дома. Хорошо, что можно проехать по деньгам."
        )

    def f3(gs):
        stats.mod(gs, stats.KNOWLEDGE, +5)
        ui.display_at(gs, "Вы увидели знак Т1 и порадовались, что знаете, что это.")

    def f4(gs):
        ui.display_at(
            gs, "Вам все еще грустно из-за того, что ваш рюкзак досматривали."
        )
        vitals.mod(gs, vitals.MENTAL, -2)

    def f5(gs):
        ui.display_at(gs, "Вы успели сесть на освободившееся место!")
        vitals.mod(gs, vitals.FATIGUE, -5)
        vitals.mod(gs, vitals.MENTAL, +2)

    def f6(gs):
        ui.display_at(
            gs,
            "Вы прочитали википедию про строительство новой Архангельско-Рублевской ветки!",
        )
        stats.mod(gs, stats.KNOWLEDGE, +3)

    def f7(gs):
        if random.choice([True, False]):
            ui.display_at(gs, "Вы похвалили значки незнакомой девушки в вагоне... Вау.")
        else:
            ui.display_at(gs, "Вы похвалили значки незнакомого парня в вагоне... Вау.")
        stats.mod(gs, stats.SOCIAL, +7)

    def f8(gs):
        ui.display_at(
            gs,
            "Вы насвистываете мелодию, которую играл скрипач в вестибюле. Вы чувствуете себя лучше.",
        )
        vitals.mod(gs, vitals.MENTAL, +3)
        vitals.mod(gs, vitals.SLEEPINESS, -3)

    def f9(gs):
        ui.display_at(gs, "Кофе в термосе протек... Сил вам.")
        vitals.mod(gs, vitals.MENTAL, -8)
        vitals.mod(gs, vitals.FATIGUE, +5)

    def f10(gs):
        ui.display_at(
            gs, "Слишком много людей... Вы чувствуете, что голова кружится..."
        )
        vitals.mod(gs, vitals.MENTAL, -5)

    hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    events = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    place = Place.METRO
    cooldown = 25
    return random_scenario_somewhere(events, hours, place, cooldown, state)


def random_surf_coffee_scenario(state=None):
    def f1(gs):
        ui.display_at(
            gs,
            "О боже мой. С вами, кажется, флиртует бариста. Или нет?... Какой кошмар.",
        )
        stats.mod(gs, stats.SOCIAL, -10)

    def f2(gs):
        ui.display_at(
            gs, "Вы поздоровались с кем-то с потока. Приятно, что вас помнят!"
        )
        stats.mod(gs, stats.SOCIAL, +4)

    def f3(gs):
        ui.display_at(gs, "Запах кофе приятно подрит...")
        vitals.mod(gs, vitals.FATIGUE, -2)
        vitals.mod(gs, vitals.MENTAL, +4)

    def f4(gs):
        ui.display_at(gs, "Играет знакомая песня, вы еле слышно подпеваете!")
        vitals.mod(gs, vitals.MENTAL, +3)
        stats.mod(gs, stats.KNOWLEDGE, +2)

    def f5(gs):
        ui.display_at(
            gs,
            "В заказе человека перед вами что-то настолько дорогое, что глаза на лоб лезут... Вам грустно.",
        )
        vitals.mod(gs, vitals.MENTAL, -3)

    hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    events = [f1, f2, f3, f4, f5]
    place = Place.SURF_COFFEE
    cooldown = 40
    return random_scenario_somewhere(events, hours, place, cooldown, state)


SCENARIOS = [
    random_scenario,
    random_university_day_scenario,
    random_park_day_scenario,
    random_home_day_scenario,
    random_metro_day_scenario,
    random_park_night_scenario,
    random_surf_coffee_scenario,
]
