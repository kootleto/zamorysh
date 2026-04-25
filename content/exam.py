import random


def exam(gs):
    knowledge = gs_api.get_stat(gs, "knowledge")
    mental = gs_api.get_stat(gs, "mental")
    fatigue = gs_api.get_stat(gs, "fatigue")
    sleepiness = gs_api.get_stat(gs, "sleepiness")
    social = gs_api.get_stat(gs, "social")

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

        exam_score = total * 10
        passed = exam_score >= 4

        results.append(
            {
                "exam": i,
                "used_parameters": triplet,
                "parameter_values": values,
                "luck_score": luck_score,
                "total_fraction": total,
                "score_0_to_10": round(exam_score, 2),
                "passed": passed,
            }
        )

    print("=== EXAM RESULTS ===\n")
    for res in results:
        print(f"Exam {res['exam']}:")
        print(f"  Parameters: {res['used_parameters']} = {res['parameter_values']}")
        print(f"  Luck: {res['luck_score']} points")
        print(f"  Total fraction: {res['total_fraction']:.3f}")
        print(f"  Score (0-10): {res['score_0_to_10']}")
        print(f"  Result: {'PASSED' if res['passed'] else 'FAILED'}\n")

    return results
