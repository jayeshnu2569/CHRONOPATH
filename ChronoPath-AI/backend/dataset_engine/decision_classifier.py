from pathlib import Path


# ============================================================
# CHRONOPATH AI
# DECISION RELEVANCE CLASSIFIER
# ============================================================

CATEGORIES = {
    "career",
    "education",
    "finance",
    "business",
    "technology",
    "other"
}


# ============================================================
# KEYWORD DEFINITIONS
# ============================================================

CATEGORY_KEYWORDS = {

    "career": [
        "career",
        "job",
        "employment",
        "occupation",
        "profession",
        "salary",
        "wage",
        "placement",
        "work experience",
        "promotion",
        "employee",
        "workforce",
        "resume",
        "recruitment",
        "skills"
    ],

    "education": [
        "education",
        "student",
        "school",
        "college",
        "university",
        "exam",
        "grade",
        "marks",
        "academic",
        "learning",
        "course",
        "degree",
        "attendance",
        "teacher",
        "placement"
    ],

    "finance": [
        "finance",
        "financial",
        "investment",
        "investor",
        "stock",
        "market",
        "bank",
        "banking",
        "loan",
        "credit",
        "debt",
        "income",
        "expense",
        "profit",
        "loss",
        "revenue",
        "budget",
        "insurance",
        "interest"
    ],

    "business": [
        "business",
        "company",
        "customer",
        "sales",
        "marketing",
        "product",
        "revenue",
        "profit",
        "startup",
        "enterprise",
        "retail",
        "commerce",
        "market",
        "employee",
        "operations"
    ],

    "technology": [
        "technology",
        "software",
        "hardware",
        "computer",
        "programming",
        "developer",
        "machine learning",
        "artificial intelligence",
        "ai",
        "data science",
        "cloud",
        "cybersecurity",
        "network",
        "database",
        "app",
        "application",
        "internet"
    ]
}


# ============================================================
# DECISION KEYWORDS
# ============================================================

DECISION_KEYWORDS = {

    "career": [
        "job",
        "career",
        "salary",
        "employment",
        "skill",
        "promotion",
        "placement"
    ],

    "education": [
        "education",
        "course",
        "degree",
        "college",
        "university",
        "exam",
        "student",
        "learning"
    ],

    "finance": [
        "investment",
        "loan",
        "credit",
        "profit",
        "return",
        "risk",
        "income",
        "expense",
        "budget",
        "stock"
    ],

    "business": [
        "customer",
        "sales",
        "marketing",
        "profit",
        "revenue",
        "product",
        "business",
        "company"
    ],

    "technology": [
        "software",
        "hardware",
        "technology",
        "computer",
        "developer",
        "performance",
        "application",
        "programming"
    ]
}


# ============================================================
# LOW-VALUE / IRRELEVANT KEYWORDS
# ============================================================

LOW_VALUE_KEYWORDS = [
    "sports",
    "football",
    "soccer",
    "cricket",
    "basketball",
    "nba",
    "nfl",
    "ufc",
    "boxing",
    "wrestling",
    "celebrity",
    "movie",
    "actor",
    "actress",
    "music",
    "song",
    "pokemon",
    "game scores"
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    if text is None:
        return ""

    return str(text).lower().strip()


# ============================================================
# CATEGORY DETECTION
# ============================================================

def detect_category(
    title="",
    description="",
    column_names=None
):

    if column_names is None:
        column_names = []

    text_parts = [

        normalize_text(title),

        normalize_text(description),

        " ".join(
            normalize_text(column)
            for column in column_names
        )

    ]

    text = " ".join(text_parts)

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:

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


# ============================================================
# DECISION RELEVANCE
# ============================================================

def calculate_decision_relevance(
    title="",
    description="",
    column_names=None,
    category=None
):

    if column_names is None:
        column_names = []

    text = " ".join([

        normalize_text(title),

        normalize_text(description),

        " ".join(
            normalize_text(column)
            for column in column_names
        )

    ])

    decision_hits = 0

    for keywords in DECISION_KEYWORDS.values():

        for keyword in keywords:

            if keyword in text:

                decision_hits += 1

    # --------------------------------------------------------
    # Negative relevance
    # --------------------------------------------------------

    low_value_hits = 0

    for keyword in LOW_VALUE_KEYWORDS:

        if keyword in text:

            low_value_hits += 1

    # --------------------------------------------------------
    # Calculate base score
    # --------------------------------------------------------

    score = min(
        decision_hits * 12,
        100
    )

    # Category bonus
    if category in CATEGORIES and category != "other":

        score += 10

    # Low-value penalty
    score -= low_value_hits * 20

    score = max(
        0,
        min(score, 100)
    )

    return round(
        score,
        2
    )


# ============================================================
# DECISION VARIABLES
# ============================================================

def identify_decision_variables(
    column_names
):

    variables = []

    for column in column_names:

        column_text = normalize_text(
            column
        )

        for category, keywords in DECISION_KEYWORDS.items():

            for keyword in keywords:

                if keyword in column_text:

                    variables.append(
                        str(column)
                    )

                    break

            if str(column) in variables:

                break

    return list(
        dict.fromkeys(variables)
    )


# ============================================================
# POSSIBLE DECISION TYPES
# ============================================================

def identify_decision_types(
    category,
    decision_variables
):

    decisions = []

    if category == "career":

        decisions.extend([
            "career selection",
            "job selection",
            "skill development",
            "career planning"
        ])

    elif category == "education":

        decisions.extend([
            "course selection",
            "education planning",
            "academic planning",
            "study strategy"
        ])

    elif category == "finance":

        decisions.extend([
            "investment decision",
            "financial planning",
            "budget planning",
            "risk evaluation"
        ])

    elif category == "business":

        decisions.extend([
            "business strategy",
            "customer strategy",
            "product strategy",
            "sales planning"
        ])

    elif category == "technology":

        decisions.extend([
            "technology selection",
            "software selection",
            "technology planning",
            "performance comparison"
        ])

    # Only return decisions if useful variables exist
    if not decision_variables:

        return []

    return decisions


# ============================================================
# FINAL CLASSIFICATION
# ============================================================

def classify_dataset(
    title="",
    description="",
    column_names=None
):

    if column_names is None:
        column_names = []

    category = detect_category(

        title=title,

        description=description,

        column_names=column_names

    )

    relevance_score = calculate_decision_relevance(

        title=title,

        description=description,

        column_names=column_names,

        category=category

    )

    decision_variables = identify_decision_variables(

        column_names
    )

    decision_types = identify_decision_types(

        category,

        decision_variables

    )

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    if relevance_score >= 75:

        relevance_status = "HIGH"

    elif relevance_score >= 50:

        relevance_status = "MEDIUM"

    elif relevance_score >= 30:

        relevance_status = "LOW"

    else:

        relevance_status = "VERY LOW"

    return {

        "category":
            category,

        "decision_relevance_score":
            relevance_score,

        "decision_relevance":
            relevance_status,

        "decision_variables":
            decision_variables,

        "possible_decisions":
            decision_types

    }


# ============================================================
# DATASET RESULT COMBINER
# ============================================================

def classify_quality_result(
    quality_result,
    title="",
    description=""
):

    column_names = quality_result.get(
        "column_names",
        []
    )

    classification = classify_dataset(

        title=title,

        description=description,

        column_names=column_names

    )

    combined = dict(
        quality_result
    )

    combined.update(
        classification
    )

    # --------------------------------------------------------
    # Final ChronoPath relevance status
    # --------------------------------------------------------

    quality_score = quality_result.get(
        "quality_score",
        0
    )

    relevance_score = classification[
        "decision_relevance_score"
    ]

    # Weighted combined score
    final_score = (

        quality_score * 0.45 +

        relevance_score * 0.55

    )

    combined[
        "chronopath_final_score"
    ] = round(
        final_score,
        2
    )

    # --------------------------------------------------------
    # Final decision
    # --------------------------------------------------------

    if quality_result.get(
        "status"
    ) == "REJECT":

        combined[
            "chronopath_status"
        ] = "REJECT"

    elif relevance_score < 30:

        combined[
            "chronopath_status"
        ] = "REJECT"

    elif final_score >= 75:

        combined[
            "chronopath_status"
        ] = "SHORTLIST"

    elif final_score >= 55:

        combined[
            "chronopath_status"
        ] = "REVIEW"

    else:

        combined[
            "chronopath_status"
        ] = "REJECT"

    return combined