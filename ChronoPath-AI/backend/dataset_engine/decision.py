from .quality import calculate_quality
from .classifier import classify_dataset


def evaluate_dataset(scan):

    quality = calculate_quality(scan)

    classification = classify_dataset(
        scan
    )

    quality_score = quality[
        "quality_score"
    ]

    classification_score = classification[
        "classification_score"
    ]

    if scan.get("status") == "REJECTED":

        final_status = "REJECTED"

        reason = scan.get(
            "reason",
            "Invalid dataset"
        )

    elif quality_score < 50:

        final_status = "REJECTED"

        reason = (
            "Dataset quality is too low"
        )

    elif classification_score == 0:

        final_status = "REVIEW"

        reason = (
            "Unable to confidently "
            "classify dataset"
        )

    elif quality_score < 75:

        final_status = "REVIEW"

        reason = (
            "Dataset requires manual "
            "quality review"
        )

    else:

        final_status = "APPROVED"

        reason = (
            "Dataset passed automated "
            "quality and classification checks"
        )

    return {
        **scan,
        **quality,
        **classification,
        "final_status": final_status,
        "decision_reason": reason
    }