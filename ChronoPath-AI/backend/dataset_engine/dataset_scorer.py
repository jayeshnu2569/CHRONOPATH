from datetime import datetime, timezone


# ============================================================
# CHRONOPATH AI
# DATASET SCORING ENGINE
# ============================================================


# ------------------------------------------------------------
# CATEGORY KEYWORDS
# ------------------------------------------------------------

CATEGORY_KEYWORDS = {

    "career": [
        "career",
        "job",
        "employment",
        "salary",
        "occupation",
        "profession",
        "placement",
        "workforce",
        "resume",
        "skill"
    ],

    "education": [
        "education",
        "student",
        "school",
        "college",
        "university",
        "academic",
        "learning",
        "course",
        "exam"
    ],

    "finance": [
        "finance",
        "financial",
        "stock",
        "investment",
        "bank",
        "loan",
        "money",
        "market",
        "revenue",
        "income"
    ],

    "business": [
        "business",
        "company",
        "startup",
        "sales",
        "customer",
        "marketing",
        "entrepreneur",
        "profit",
        "industry"
    ],

    "technology": [
        "technology",
        "software",
        "computer",
        "programming",
        "developer",
        "ai",
        "machine learning",
        "data science",
        "cybersecurity",
        "hardware"
    ]
}


# ------------------------------------------------------------
# TEXT EXTRACTION
# ------------------------------------------------------------

def get_dataset_text(dataset):

    title = getattr(
        dataset,
        "title",
        ""
    )

    ref = getattr(
        dataset,
        "ref",
        ""
    )

    return (
        f"{title} {ref}"
    ).lower()


# ------------------------------------------------------------
# CATEGORY DETECTION
# ------------------------------------------------------------

def detect_category(dataset):

    text = get_dataset_text(
        dataset
    )

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword.lower() in text:
                score += 1

        scores[category] = score

    if not scores:
        return "other"

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:
        return "other"

    return best_category


# ------------------------------------------------------------
# RELEVANCE SCORE
# ------------------------------------------------------------

def calculate_relevance(
    dataset,
    target_category=None
):

    detected_category = detect_category(
        dataset
    )

    if target_category:

        target_category = (
            target_category.lower()
        )

        if detected_category == target_category:
            return 100

        return 40

    if detected_category != "other":
        return 80

    return 30


# ------------------------------------------------------------
# POPULARITY SCORE
# ------------------------------------------------------------

def calculate_popularity(dataset):

    downloads = getattr(
        dataset,
        "download_count",
        0
    ) or 0

    votes = getattr(
        dataset,
        "vote_count",
        0
    ) or 0

    try:
        downloads = int(
            downloads
        )
    except (ValueError, TypeError):
        downloads = 0

    try:
        votes = int(
            votes
        )
    except (ValueError, TypeError):
        votes = 0

    download_score = min(
        60,
        downloads / 500
    )

    vote_score = min(
        40,
        votes / 5
    )

    return round(
        download_score + vote_score,
        2
    )


# ------------------------------------------------------------
# USABILITY SCORE
# ------------------------------------------------------------

def calculate_usability(dataset):

    usability = getattr(
        dataset,
        "usability_rating",
        0
    ) or 0

    try:
        usability = float(
            usability
        )
    except (ValueError, TypeError):
        usability = 0

    return round(
        max(
            0,
            min(
                100,
                usability * 100
            )
        ),
        2
    )


# ------------------------------------------------------------
# DECISION SUPPORT SCORE
# ------------------------------------------------------------

def calculate_decision_value(dataset):

    text = get_dataset_text(
        dataset
    )

    decision_keywords = [

        "prediction",
        "recommendation",
        "decision",
        "success",
        "risk",
        "choice",
        "outcome",
        "career",
        "salary",
        "investment",
        "education",
        "performance",
        "forecast",
        "selection",
        "opportunity"
    ]

    matches = 0

    for keyword in decision_keywords:

        if keyword in text:
            matches += 1

    score = min(
        100,
        30 + (matches * 10)
    )

    return score


# ------------------------------------------------------------
# FRESHNESS SCORE
# ------------------------------------------------------------

def calculate_freshness(dataset):

    updated = getattr(
        dataset,
        "last_updated",
        None
    )

    if not updated:
        return 50

    try:

        if isinstance(
            updated,
            str
        ):

            updated = datetime.fromisoformat(
                updated.replace(
                    "Z",
                    "+00:00"
                )
            )

        if updated.tzinfo is None:

            updated = updated.replace(
                tzinfo=timezone.utc
            )

        now = datetime.now(
            timezone.utc
        )

        age_days = (
            now - updated
        ).days

        if age_days <= 365:
            return 100

        if age_days <= 730:
            return 80

        if age_days <= 1095:
            return 60

        if age_days <= 1825:
            return 40

        return 20

    except Exception:

        return 50


# ------------------------------------------------------------
# FINAL SCORE
# ------------------------------------------------------------

def calculate_final_score(
    relevance,
    popularity,
    usability,
    freshness,
    decision_value
):

    score = (

        relevance * 0.30 +

        popularity * 0.10 +

        usability * 0.20 +

        freshness * 0.10 +

        decision_value * 0.30

    )

    return round(
        score,
        2
    )


# ------------------------------------------------------------
# COMPLETE DATASET ANALYSIS
# ------------------------------------------------------------

def score_dataset(
    dataset,
    target_category=None
):

    category = detect_category(
        dataset
    )

    relevance = calculate_relevance(
        dataset,
        target_category
    )

    popularity = calculate_popularity(
        dataset
    )

    usability = calculate_usability(
        dataset
    )

    freshness = calculate_freshness(
        dataset
    )

    decision_value = calculate_decision_value(
        dataset
    )

    final_score = calculate_final_score(

        relevance,

        popularity,

        usability,

        freshness,

        decision_value
    )

    if final_score >= 80:

        status = "SHORTLIST"

    elif final_score >= 60:

        status = "REVIEW"

    else:

        status = "REJECT"

    return {

        "title": getattr(
            dataset,
            "title",
            "Unknown"
        ),

        "ref": getattr(
            dataset,
            "ref",
            "Unknown"
        ),

        "category": category,

        "relevance": relevance,

        "popularity": popularity,

        "usability": usability,

        "freshness": freshness,

        "decision_value": decision_value,

        "final_score": final_score,

        "status": status
    }


# ------------------------------------------------------------
# SCORE MULTIPLE DATASETS
# ------------------------------------------------------------

def score_datasets(
    datasets,
    target_category=None
):

    results = []

    for dataset in datasets:

        result = score_dataset(
            dataset,
            target_category
        )

        results.append(
            result
        )

    results.sort(
        key=lambda item: item[
            "final_score"
        ],
        reverse=True
    )

    return results