from pathlib import Path
import pandas as pd


# ============================================================
# CHRONOPATH AI
# SEMANTIC DATASET ANALYZER
#
# Purpose:
# Analyze the actual contents of a dataset and determine:
# - What the dataset represents
# - Which categories it belongs to
# - Which columns are decision-relevant
# - What decisions it could potentially support
#
# IMPORTANT:
# This module does NOT invent information.
# It only uses information actually present in:
# - column names
# - sample values
# - dataset title
# - description
# ============================================================


# ============================================================
# CATEGORY SIGNALS
# ============================================================

CATEGORY_SIGNALS = {

    "career": [
        "career",
        "job",
        "employment",
        "occupation",
        "profession",
        "salary",
        "wage",
        "placement",
        "employee",
        "experience",
        "promotion",
        "skills",
        "work"
    ],

    "education": [
        "student",
        "education",
        "school",
        "college",
        "university",
        "degree",
        "course",
        "exam",
        "grade",
        "marks",
        "attendance",
        "academic",
        "learning",
        "teacher"
    ],

    "finance": [
        "finance",
        "financial",
        "investment",
        "stock",
        "market",
        "bank",
        "loan",
        "credit",
        "debt",
        "income",
        "expense",
        "profit",
        "loss",
        "revenue",
        "budget",
        "interest",
        "return"
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
        "operations"
    ],

    "technology": [
        "technology",
        "software",
        "hardware",
        "computer",
        "programming",
        "developer",
        "machine",
        "learning",
        "artificial",
        "intelligence",
        "cloud",
        "cybersecurity",
        "network",
        "database",
        "application",
        "performance"
    ]
}


# ============================================================
# LOW-VALUE DOMAIN SIGNALS
# ============================================================

LOW_VALUE_SIGNALS = [
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
    "game scores"
]


# ============================================================
# DECISION VARIABLE SIGNALS
# ============================================================

DECISION_VARIABLE_SIGNALS = [

    "salary",
    "income",
    "expense",
    "cost",
    "price",
    "profit",
    "revenue",
    "risk",
    "return",
    "score",
    "grade",
    "marks",
    "education",
    "degree",
    "course",
    "skill",
    "experience",
    "employment",
    "job",
    "career",
    "performance",
    "customer",
    "sales",
    "market",
    "investment",
    "loan",
    "credit",
    "budget",
    "location",
    "age",
    "gender",
    "company",
    "product"
]


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value):

    if value is None:
        return ""

    return str(value).lower().strip()


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(file_path):

    file_path = Path(
        file_path
    )

    extension = file_path.suffix.lower()

    if extension == ".csv":

        return pd.read_csv(
            file_path,
            low_memory=False
        )

    if extension in {
        ".xlsx",
        ".xls"
    }:

        return pd.read_excel(
            file_path
        )

    if extension == ".json":

        return pd.read_json(
            file_path
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


# ============================================================
# CREATE DATASET TEXT
# ============================================================

def create_dataset_text(
    df,
    title="",
    description=""
):

    parts = []

    if title:

        parts.append(
            normalize_text(title)
        )

    if description:

        parts.append(
            normalize_text(description)
        )

    # Column names
    for column in df.columns:

        parts.append(
            normalize_text(column)
        )

    # Sample values
    sample_size = min(
        len(df),
        10
    )

    if sample_size > 0:

        sample = df.head(
            sample_size
        )

        for column in sample.columns:

            values = sample[
                column
            ].dropna().astype(str)

            for value in values:

                parts.append(
                    normalize_text(value)
                )

    return " ".join(parts)


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

def analyze_categories(
    dataset_text
):

    scores = {}

    for category, signals in (
        CATEGORY_SIGNALS.items()
    ):

        score = 0

        for signal in signals:

            if signal in dataset_text:

                score += 1

        scores[
            category
        ] = score

    return scores


# ============================================================
# DETERMINE PRIMARY CATEGORY
# ============================================================

def determine_category(
    category_scores
):

    if not category_scores:

        return "other"

    best_category = max(
        category_scores,
        key=category_scores.get
    )

    best_score = category_scores[
        best_category
    ]

    if best_score == 0:

        return "other"

    return best_category


# ============================================================
# IDENTIFY DECISION VARIABLES
# ============================================================

def identify_decision_variables(
    df
):

    variables = []

    for column in df.columns:

        column_text = normalize_text(
            column
        )

        matched = False

        for signal in (
            DECISION_VARIABLE_SIGNALS
        ):

            if signal in column_text:

                variables.append(
                    str(column)
                )

                matched = True

                break

        if matched:
            continue

    return list(
        dict.fromkeys(
            variables
        )
    )


# ============================================================
# IDENTIFY NUMERIC DECISION VARIABLES
# ============================================================

def identify_numeric_variables(
    df
):

    variables = []

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):

            variables.append(
                str(column)
            )

    return variables


# ============================================================
# IDENTIFY CATEGORICAL VARIABLES
# ============================================================

def identify_categorical_variables(
    df
):

    variables = []

    for column in df.columns:

        if (
            df[column].dtype == "object"
            or
            str(
                df[column].dtype
            ).startswith("category")
        ):

            variables.append(
                str(column)
            )

    return variables


# ============================================================
# DECISION TYPES
# ============================================================

def identify_possible_decisions(
    category,
    decision_variables
):

    if not decision_variables:

        return []

    decisions = []

    if category == "career":

        decisions = [
            "career selection",
            "job selection",
            "skill development",
            "career planning"
        ]

    elif category == "education":

        decisions = [
            "course selection",
            "education planning",
            "academic planning",
            "study strategy"
        ]

    elif category == "finance":

        decisions = [
            "investment decision",
            "financial planning",
            "budget planning",
            "risk evaluation"
        ]

    elif category == "business":

        decisions = [
            "business strategy",
            "customer strategy",
            "product strategy",
            "sales planning"
        ]

    elif category == "technology":

        decisions = [
            "technology selection",
            "software selection",
            "technology planning",
            "performance comparison"
        ]

    return decisions


# ============================================================
# SEMANTIC RELEVANCE
# ============================================================

def calculate_semantic_relevance(
    dataset_text,
    category_scores,
    decision_variables
):

    if not dataset_text:

        return 0

    category_score = max(
        category_scores.values()
    ) if category_scores else 0

    variable_count = len(
        decision_variables
    )

    # Category contribution
    category_component = min(
        category_score * 10,
        50
    )

    # Decision-variable contribution
    variable_component = min(
        variable_count * 10,
        40
    )

    # Dataset has actual information
    structure_component = 10

    score = (
        category_component
        +
        variable_component
        +
        structure_component
    )

    return round(
        min(score, 100),
        2
    )


# ============================================================
# LOW VALUE DETECTION
# ============================================================

def detect_low_value_domain(
    dataset_text
):

    matches = []

    for signal in LOW_VALUE_SIGNALS:

        if signal in dataset_text:

            matches.append(
                signal
            )

    return list(
        dict.fromkeys(
            matches
        )
    )


# ============================================================
# FINAL SEMANTIC ANALYSIS
# ============================================================

def analyze_dataset_semantics(
    file_path,
    title="",
    description=""
):

    file_path = Path(
        file_path
    )

    result = {

        "file":
            file_path.name,

        "semantic_status":
            "ERROR",

        "error":
            None

    }

    try:

        # ----------------------------------------------------
        # Load dataset
        # ----------------------------------------------------

        df = load_dataset(
            file_path
        )

        # ----------------------------------------------------
        # Create text representation
        # ----------------------------------------------------

        dataset_text = create_dataset_text(

            df,

            title=title,

            description=description

        )

        # ----------------------------------------------------
        # Analyze categories
        # ----------------------------------------------------

        category_scores = analyze_categories(
            dataset_text
        )

        category = determine_category(
            category_scores
        )

        # ----------------------------------------------------
        # Decision variables
        # ----------------------------------------------------

        decision_variables = (
            identify_decision_variables(
                df
            )
        )

        numeric_variables = (
            identify_numeric_variables(
                df
            )
        )

        categorical_variables = (
            identify_categorical_variables(
                df
            )
        )

        # ----------------------------------------------------
        # Possible decisions
        # ----------------------------------------------------

        possible_decisions = (
            identify_possible_decisions(

                category,

                decision_variables

            )
        )

        # ----------------------------------------------------
        # Semantic relevance
        # ----------------------------------------------------

        semantic_score = (
            calculate_semantic_relevance(

                dataset_text,

                category_scores,

                decision_variables

            )
        )

        # ----------------------------------------------------
        # Low-value detection
        # ----------------------------------------------------

        low_value_domains = (
            detect_low_value_domain(
                dataset_text
            )
        )

        # ----------------------------------------------------
        # Apply low-value penalty
        # ----------------------------------------------------

        if low_value_domains:

            semantic_score = max(

                0,

                semantic_score
                -
                (
                    len(
                        low_value_domains
                    )
                    *
                    20
                )

            )

        # ----------------------------------------------------
        # Relevance status
        # ----------------------------------------------------

        if semantic_score >= 75:

            relevance = "HIGH"

        elif semantic_score >= 50:

            relevance = "MEDIUM"

        elif semantic_score >= 30:

            relevance = "LOW"

        else:

            relevance = "VERY LOW"

        # ----------------------------------------------------
        # Semantic status
        # ----------------------------------------------------

        if semantic_score >= 75:

            semantic_status = "SHORTLIST"

        elif semantic_score >= 50:

            semantic_status = "REVIEW"

        else:

            semantic_status = "REJECT"

        # ----------------------------------------------------
        # Final result
        # ----------------------------------------------------

        result.update({

            "semantic_status":
                semantic_status,

            "category":
                category,

            "category_scores":
                category_scores,

            "semantic_score":
                semantic_score,

            "decision_relevance":
                relevance,

            "decision_variables":
                decision_variables,

            "numeric_variables":
                numeric_variables,

            "categorical_variables":
                categorical_variables,

            "possible_decisions":
                possible_decisions,

            "low_value_domains":
                low_value_domains,

            "rows":
                len(df),

            "columns":
                len(df.columns),

            "column_names":
                list(df.columns)

        })

    except Exception as error:

        result["error"] = str(
            error
        )

    return result