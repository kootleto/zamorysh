import datetime
import random

from engine import scenarios_api, gs_api
from gameplay.api import stats, vitals, time, floors
from interface import ui


def exam(gs):
    knowledge = stats.get(gs, stats.KNOWLEDGE)
    mental = vitals.get(gs, vitals.MENTAL)
    fatigue = vitals.get(gs, vitals.FATIGUE)
    sleepiness = vitals.get(gs, vitals.SLEEPINESS)
    social = stats.get(gs, stats.SOCIAL)

    all_parameters = {
        "knowledge": knowledge,
        "mental": mental,
        "fatigue": fatigue,
        "sleepiness": sleepiness,
        "social": social,
    }

    exam_triplets = [
        ["knowledge", "mental", "fatigue"],
        ["social", "sleepiness", "knowledge"],
        ["mental", "social", "knowledge"],
    ]

    parameter_weights = [0.3, 0.3, 0.3]
    luck_weight = 0.1

    results = {"marks": [], "total": 0, "passed": False}

    for i, triplet in enumerate(exam_triplets, 1):
        values = [all_parameters[p] for p in triplet]

        normalized = []
        for param_name, val in zip(triplet, values):
            if param_name == "fatigue":
                normalized.append(max(0, min(1, (100 - val) / 100)))
            if param_name == "sleepiness":
                normalized.append(max(0, min(1, (100 - val) / 100)))
            else:
                normalized.append(max(0, min(1, val / 100)))

        luck_score = random.randint(0, 100)
        luck_normalized = luck_score / 100

        total = 0
        for w, norm_val in zip(parameter_weights, normalized):
            total += w * norm_val
        total += luck_weight * luck_normalized

        results["marks"].append(round(total * 10, 2))

    results["total"] = round(sum(results["marks"]) / 3, 2)
    if results["total"] >= 4:
        results["passed"] = True
    return results


def exam_scenario():
    def reminder_trigger(gs):
        return time.get_day(gs) == 7 and time.get_time(gs) == datetime.time(19, 00)

    def reminder(gs):
        ui.display_at(
            gs,
            "Вам на почту пришло письмо об экзамене: он пройдёт 8 сентября в аудитории 501 в 17:00. "
            "По результатам экзамена вы поймёте, насколько успешно вы прожили эту неделю.",
        )

    def skip(gs):
        ui.display_at(gs, "Игра окончена: вы не пришли на экзамен и были отчислены.")
        gs_api.stop(gs)

    def check_exam(gs):
        return (
            time.get_day(gs) == 8
            and time.get_time(gs) == datetime.time(17, 00)
            and floors.get(gs, floors.CLASSROOM) == 501
        )

    def start_exam(gs):
        ui.display_at(gs, "Экзамен начинается...")

        ui.display(
            f"Ваш результат\nOценки за каждую часть: {', '.join(map(str, exam(gs)["marks"]))}\nИтоговая оценка: {exam(gs)["total"]}"
        )

        if exam(gs)["passed"]:
            ui.display(
                "Ура, у вас получилось сдать экзамен! Вы успешно прожили первую неделю на ФиКЛе!"
            )
        else:
            ui.display(
                "К сожалению, вам не удалось сдать экзамен... Наверное, учёба на ФиКЛе вам не подходит."
            )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, reminder_trigger, reminder),
            scenarios_api.base_transition(1, 3, lambda gs: not check_exam(gs), skip),
            scenarios_api.base_transition(1, 2, check_exam, start_exam),
        ]
    )


SCENARIOS = [exam_scenario]
