CATEGORIES = {

    "career": [
        "job",
        "career",
        "salary",
        "employment",
        "occupation",
        "profession",
        "skill"
    ],

    "education": [
        "education",
        "student",
        "college",
        "school",
        "university",
        "exam",
        "degree"
    ],

    "finance": [
        "stock",
        "investment",
        "finance",
        "inflation",
        "interest",
        "market",
        "revenue",
        "profit"
    ],

    "technology": [
        "smartphone",
        "laptop",
        "processor",
        "gpu",
        "cpu",
        "battery",
        "technology",
        "device"
    ],

    "business": [
        "business",
        "customer",
        "sales",
        "company",
        "startup",
        "marketing"
    ],

    "risk": [
        "risk",
        "failure",
        "probability",
        "accident",
        "uncertainty"
    ]
}


def classify_dataset(scan):

    searchable_text = " ".join(
        scan.get("columns", [])
    ).lower()

    filename = scan.get(
        "filename",
        ""
    ).lower()

    searchable_text += " " + filename

    scores = {}

    for category, keywords in CATEGORIES.items():

        score = 0

        for keyword in keywords:

            if keyword in searchable_text:
                score += 1

        scores[category] = score

    if not scores:
        return {
            "category": "unknown",
            "classification_score": 0
        }

    category = max(
        scores,
        key=scores.get
    )

    classification_score = scores[
        category
    ]

    if classification_score == 0:

        category = "unknown"

    return {
        "category": category,
        "classification_score":
            classification_score
    }