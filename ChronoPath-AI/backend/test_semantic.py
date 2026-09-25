from dataset_engine.semantic_analyzer import (
    analyze_dataset_semantics
)


# ============================================================
# CHRONOPATH AI
# SEMANTIC DATASET ANALYZER TEST
# ============================================================

FILE_PATH = (
    r".\data\quality_test\test_dataset.csv"
)

TITLE = "Student Career Success Dataset"

DESCRIPTION = """
Dataset containing student education,
career choices, job placement and salary
information.
"""


print()
print("=" * 80)

print(
    "        CHRONOPATH AI - SEMANTIC ANALYZER"
)

print("=" * 80)

print()


result = analyze_dataset_semantics(

    FILE_PATH,

    title=TITLE,

    description=DESCRIPTION

)


print(
    f"Dataset: {result['file']}"
)

print()

print(
    f"Category: "
    f"{result.get('category')}"
)

print(
    f"Semantic Score: "
    f"{result.get('semantic_score')}/100"
)

print(
    f"Decision Relevance: "
    f"{result.get('decision_relevance')}"
)

print(
    f"Semantic Status: "
    f"{result.get('semantic_status')}"
)

print()

print(
    "Decision Variables:"
)

for variable in result.get(
    "decision_variables",
    []
):

    print(
        f"  - {variable}"
    )

print()

print(
    "Numeric Variables:"
)

for variable in result.get(
    "numeric_variables",
    []
):

    print(
        f"  - {variable}"
    )

print()

print(
    "Categorical Variables:"
)

for variable in result.get(
    "categorical_variables",
    []
):

    print(
        f"  - {variable}"
    )

print()

print(
    "Possible Decisions:"
)

for decision in result.get(
    "possible_decisions",
    []
):

    print(
        f"  - {decision}"
    )

print()

print(
    "Low-Value Domains:"
)

for domain in result.get(
    "low_value_domains",
    []
):

    print(
        f"  - {domain}"
    )

print()

print(
    f"Rows: "
    f"{result.get('rows')}"
)

print(
    f"Columns: "
    f"{result.get('columns')}"
)

print()

if result.get("error"):

    print(
        f"ERROR: "
        f"{result['error']}"
    )

print("=" * 80)

print(
    "        SEMANTIC ANALYSIS COMPLETE"
)

print("=" * 80)