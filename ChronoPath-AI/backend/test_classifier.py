from dataset_engine.dataset_quality import (
    analyze_dataset
)

from dataset_engine.decision_classifier import (
    classify_quality_result
)


# ============================================================
# CHRONOPATH AI
# DECISION CLASSIFIER TEST
# ============================================================

FILE_PATH = (
    r".\data\quality_test\test_dataset.csv"
)


TITLE = "Student Career Success Dataset"

DESCRIPTION = """
Dataset containing student education,
skills, career choices, job placement,
salary and employment information.
"""


print()
print("=" * 80)
print(
    "        CHRONOPATH AI - DECISION CLASSIFIER"
)
print("=" * 80)

print()


# ============================================================
# QUALITY ANALYSIS
# ============================================================

quality_result = analyze_dataset(
    FILE_PATH
)


# ============================================================
# CLASSIFICATION
# ============================================================

result = classify_quality_result(

    quality_result,

    title=TITLE,

    description=DESCRIPTION

)


# ============================================================
# DISPLAY
# ============================================================

print(
    f"Dataset: {TITLE}"
)

print()

print(
    f"Category: "
    f"{result['category']}"
)

print(
    f"Decision Relevance: "
    f"{result['decision_relevance']}"
)

print(
    f"Decision Relevance Score: "
    f"{result['decision_relevance_score']}/100"
)

print()

print(
    "Decision Variables:"
)

for variable in result[
    "decision_variables"
]:

    print(
        f"  - {variable}"
    )

print()

print(
    "Possible Decisions:"
)

for decision in result[
    "possible_decisions"
]:

    print(
        f"  - {decision}"
    )

print()

print(
    f"Quality Score: "
    f"{result['quality_score']}/100"
)

print(
    f"ChronoPath Final Score: "
    f"{result['chronopath_final_score']}/100"
)

print(
    f"ChronoPath Status: "
    f"{result['chronopath_status']}"
)

print()

print("=" * 80)

print(
    "        CLASSIFICATION COMPLETE"
)

print("=" * 80)