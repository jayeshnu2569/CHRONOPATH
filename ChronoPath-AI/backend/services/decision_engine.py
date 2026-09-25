def calculate_scores(criteria, option_scores):

    results = []

    total_weight = sum(c.weight for c in criteria)

    if abs(total_weight - 1.0) > 0.001:
        raise ValueError("Criterion weights must add up to 1.0")

    for option in option_scores:

        final_score = 0

        for index, criterion in enumerate(criteria):

            score = option.scores[index]
            weight = criterion.weight

            final_score += score * weight

        results.append({
            "option": option.option,
            "score": round(final_score, 3)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    for index, result in enumerate(results):

        result["rank"] = index + 1

    return results