def calculate_quality(scan):

    if scan.get("status") == "REJECTED":
        return {
            "quality_score": 0,
            "quality_status": "REJECTED"
        }

    score = 100

    rows = scan.get("rows", 0)

    missing = scan.get(
        "missing_percentage",
        100
    )

    duplicates = scan.get(
        "duplicate_percentage",
        100
    )

    # Dataset size
    if rows < 10:
        score -= 40

    elif rows < 100:
        score -= 20

    # Missing values
    if missing > 50:
        score -= 40

    elif missing > 25:
        score -= 25

    elif missing > 10:
        score -= 10

    # Duplicate rows
    if duplicates > 50:
        score -= 30

    elif duplicates > 20:
        score -= 15

    elif duplicates > 5:
        score -= 5

    score = max(
        0,
        min(100, score)
    )

    if score >= 75:
        status = "GOOD"

    elif score >= 50:
        status = "REVIEW"

    else:
        status = "POOR"

    return {
        "quality_score": score,
        "quality_status": status
    }