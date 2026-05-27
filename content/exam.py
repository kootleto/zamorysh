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

    results = []

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

        result = {"exam_score": total * 10, "passed": total * 10 >= 4}

        return result

    #     results.append(
    #         {
    #             "exam": i,
    #             "used_parameters": triplet,
    #             "parameter_values": values,
    #             "luck_score": luck_score,
    #             "total_fraction": total,
    #             "score_0_to_10": round(exam_score, 2),
    #             "passed": passed,
    #         }
    #     )
    #
    # log("=== EXAM RESULTS ===\n")
    # for res in results:
    #     log(f"Exam {res['exam']}:")
    #     log(f"  Parameters: {res['used_parameters']} = {res['parameter_values']}")
    #     log(f"  Luck: {res['luck_score']} points")
    #     log(f"  Total fraction: {res['total_fraction']:.3f}")
    #     log(f"  Score (0-10): {res['score_0_to_10']}")
    #     log(f"  Result: {'PASSED' if res['passed'] else 'FAILED'}\n")
    #
    # return results
    return


def exam_scenario():
    def reminder_trigger(gs):
        return time.get_day(gs) == 7 and time.get_time(gs) == datetime.time(19, 00)

    def reminder(gs):
        ui.display_at(
            gs,
            "Вам на почту пришло письмо об экзамене: он пройдёт 8 сентября в аудитории 501 в 17:00. "
            "По результатам экзамена вы поймёте, насколько успешно вы прожили эту неделю.",
        )

    def check_exam(gs):
        return (
            time.get_day(gs) == 8
            and time.get_time(gs) == datetime.time(17, 00)
            and floors.get(gs, floors.CLASSROOM) == 501
        )

    def start_exam(gs):
        ui.display_at(gs, "Экзамен начинается...")

    def finish_exam(gs):
        ui.display(f"Ваша оценка за экзамен: {exam(gs)["exam_score"]}")

    def check_passed(gs):
        if exam(gs)["passed"]:
            ui.display(
                "Ура, у вас получилось сдать экзамен! Вы успешно прожили первую неделю на ФиКЛе!"
            )
        else:
            ui.display(
                "К сожалению, вам не удалось сдать экзамен... Наверное, учёба на ФиКЛе вам не подходит :("
            )
        gs_api.stop(gs)

    return scenarios_api.base_scenario(
        [
            scenarios_api.base_transition(0, 1, reminder_trigger, reminder),
            scenarios_api.base_transition(1, 2, check_exam, start_exam),
            scenarios_api.base_transition(2, 3, True, finish_exam),
            scenarios_api.base_transition(4, 5, True, check_passed),
        ]
    )


SCENARIOS = [exam_scenario]
