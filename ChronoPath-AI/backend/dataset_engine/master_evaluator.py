from dataset_engine.dataset_quality import analyze_dataset
from dataset_engine.decision_classifier import classify_dataset
from dataset_engine.semantic_analyzer import analyze_dataset_semantics


# ============================================================
# CHRONOPATH AI
# MASTER DATASET EVALUATION ENGINE
# ============================================================

METADATA_WEIGHT = 0.20
QUALITY_WEIGHT = 0.30
DECISION_WEIGHT = 0.30
SEMANTIC_WEIGHT = 0.20


# ============================================================
# SAFE NUMBER
# ============================================================

def safe_number(value, default=0):

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ============================================================
# METADATA SCORE
# ============================================================

def calculate_metadata_score(metadata):

    """
    Calculate the ChronoPath metadata score.

    Preferred input:
        metadata_score

    Fallback:
        decision_value

    Legacy compatibility:
        final_score
        score
    """

    if not metadata:

        return 0

    # --------------------------------------------------------
    # Preferred: already calculated ChronoPath metadata score
    # --------------------------------------------------------

    if "metadata_score" in metadata:

        value = safe_number(
            metadata["metadata_score"]
        )

        return round(
            max(
                0,
                min(
                    value,
                    100
                )
            ),
            2
        )

    # --------------------------------------------------------
    # Decision value fallback
    # --------------------------------------------------------

    if "decision_value" in metadata:

        value = safe_number(
            metadata["decision_value"]
        )

        return round(
            max(
                0,
                min(
                    value,
                    100
                )
            ),
            2
        )

    # --------------------------------------------------------
    # Legacy compatibility
    # --------------------------------------------------------

    for field in [
        "final_score",
        "score"
    ]:

        if field in metadata:

            value = safe_number(
                metadata[field]
            )

            return round(
                max(
                    0,
                    min(
                        value,
                        100
                    )
                ),
                2
            )

    return 0

# ============================================================
# QUALITY SCORE
# ============================================================

def calculate_quality_score(
    quality_result
):

    return max(
        0,
        min(
            safe_number(
                quality_result.get(
                    "quality_score",
                    0
                )
            ),
            100
        )
    )


# ============================================================
# DECISION SCORE
# ============================================================

def calculate_decision_score(
    decision_result
):

    return max(
        0,
        min(
            safe_number(
                decision_result.get(
                    "decision_relevance_score",
                    0
                )
            ),
            100
        )
    )


# ============================================================
# SEMANTIC SCORE
# ============================================================

def calculate_semantic_score(
    semantic_result
):

    return max(
        0,
        min(
            safe_number(
                semantic_result.get(
                    "semantic_score",
                    0
                )
            ),
            100
        )
    )


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(
    metadata_score,
    quality_score,
    decision_score,
    semantic_score
):

    final_score = (

        metadata_score
        * METADATA_WEIGHT

        +

        quality_score
        * QUALITY_WEIGHT

        +

        decision_score
        * DECISION_WEIGHT

        +

        semantic_score
        * SEMANTIC_WEIGHT

    )

    return round(
        final_score,
        2
    )


# ============================================================
# FINAL STATUS
# ============================================================

def determine_status(
    final_score,
    quality_result,
    decision_score,
    semantic_score
):

    # --------------------------------------------------------
    # Hard rejection rules
    # --------------------------------------------------------

    if quality_result.get(
        "status"
    ) == "REJECT":

        return "REJECT"

    if decision_score < 30:

        return "REJECT"

    if semantic_score < 30:

        return "REJECT"

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    if final_score >= 75:

        return "SHORTLIST"

    if final_score >= 55:

        return "REVIEW"

    return "REJECT"


# ============================================================
# MASTER EVALUATION
# ============================================================

def evaluate_dataset(
    file_path,
    title="",
    description="",
    category="other",
    metadata=None
):
    if metadata is None:

        metadata = {}

    # ========================================================
    # 1. QUALITY
    # ========================================================

    quality_result = analyze_dataset(
        file_path
    )

    # ========================================================
    # 2. DECISION CLASSIFICATION
    # ========================================================

    column_names = quality_result.get(
        "column_names",
        []
    )

    decision_result = classify_dataset(

        title=title,

        description=description,

        column_names=column_names

    )

    # ========================================================
    # 3. SEMANTIC ANALYSIS
    # ========================================================

    semantic_result = (
        analyze_dataset_semantics(

            file_path,

            title=title,

            description=description

        )
    )

    # ========================================================
    # 4. SCORES
    # ========================================================

    metadata_score = (
        calculate_metadata_score(
            metadata
        )
    )

    quality_score = (
        calculate_quality_score(
            quality_result
        )
    )

    decision_score = (
        calculate_decision_score(
            decision_result
        )
    )

    semantic_score = (
        calculate_semantic_score(
            semantic_result
        )
    )

    # ========================================================
    # 5. FINAL SCORE
    # ========================================================

    final_score = calculate_final_score(

        metadata_score,

        quality_score,

        decision_score,

        semantic_score

    )

    # ========================================================
    # 6. FINAL STATUS
    # ========================================================

    status = determine_status(

        final_score,

        quality_result,

        decision_score,

        semantic_score

    )

    # ========================================================
    # 7. MASTER RESULT
    # ========================================================

    result = {

        # ----------------------------------------------------
        # Dataset
        # ----------------------------------------------------

        "dataset": title,

        "file": str(
            file_path
        ),

        # ----------------------------------------------------
        # Classification
        # ----------------------------------------------------

        "category": category,

        # ----------------------------------------------------
        # Individual scores
        # ----------------------------------------------------

        "metadata_score":
            metadata_score,

        "quality_score":
            quality_score,

        "decision_score":
            decision_score,

        "semantic_score":
            semantic_score,

        # ----------------------------------------------------
        # Final
        # ----------------------------------------------------

        "final_score":
            final_score,

        "status":
            status,

        # ----------------------------------------------------
        # Quality information
        # ----------------------------------------------------

        "quality_status":
            quality_result.get(
                "status"
            ),

        "rows":
            quality_result.get(
                "rows"
            ),

        "columns":
            quality_result.get(
                "columns"
            ),

        "missing_percentage":
            quality_result.get(
                "missing_percentage"
            ),

        "duplicate_percentage":
            quality_result.get(
                "duplicate_percentage"
            ),

        # ----------------------------------------------------
        # Decision information
        # ----------------------------------------------------

        "decision_relevance":
            decision_result.get(
                "decision_relevance"
            ),

        "decision_variables":
            decision_result.get(
                "decision_variables",
                []
            ),

        "possible_decisions":
            decision_result.get(
                "possible_decisions",
                []
            ),

        # ----------------------------------------------------
        # Semantic information
        # ----------------------------------------------------

        "numeric_variables":
            semantic_result.get(
                "numeric_variables",
                []
            ),

        "categorical_variables":
            semantic_result.get(
                "categorical_variables",
                []
            ),

        "low_value_domains":
            semantic_result.get(
                "low_value_domains",
                []
            )

    }

    return result


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_master_result(
    result
):

    print()

    print("=" * 80)

    print(
        "        CHRONOPATH AI - MASTER EVALUATION"
    )

    print("=" * 80)

    print()

    print(
        f"Dataset: "
        f"{result['dataset']}"
    )

    print(
        f"Category: "
        f"{result['category']}"
    )

    print()

    print(
        "SCORES"
    )

    print("-" * 80)

    print(
        f"Metadata Score:       "
        f"{result['metadata_score']}/100"
    )

    print(
        f"Quality Score:        "
        f"{result['quality_score']}/100"
    )

    print(
        f"Decision Score:       "
        f"{result['decision_score']}/100"
    )

    print(
        f"Semantic Score:       "
        f"{result['semantic_score']}/100"
    )

    print("-" * 80)

    print(
        f"FINAL SCORE:          "
        f"{result['final_score']}/100"
    )

    print(
        f"FINAL STATUS:         "
        f"{result['status']}"
    )

    print()

    print(
        "DATASET QUALITY"
    )

    print("-" * 80)

    print(
        f"Rows:                 "
        f"{result['rows']}"
    )

    print(
        f"Columns:              "
        f"{result['columns']}"
    )

    print(
        f"Missing Data:         "
        f"{result['missing_percentage']}%"
    )

    print(
        f"Duplicate Data:       "
        f"{result['duplicate_percentage']}%"
    )

    print()

    print(
        "DECISION VARIABLES"
    )

    print("-" * 80)

    for variable in result[
        "decision_variables"
    ]:

        print(
            f"  - {variable}"
        )

    print()

    print(
        "POSSIBLE DECISIONS"
    )

    print("-" * 80)

    for decision in result[
        "possible_decisions"
    ]:

        print(
            f"  - {decision}"
        )

    print()

    print("=" * 80)

    print(
        "        MASTER EVALUATION COMPLETE"
    )

    print("=" * 80)