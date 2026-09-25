from dataset_engine.master_evaluator import (
    evaluate_dataset
)

from dataset_engine.dataset_registry import (
    add_dataset,
    display_registry,
    get_registry_path
)


# ============================================================
# CHRONOPATH AI
# MASTER + REGISTRY TEST
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

KAGGLE_REFERENCE = (
    "example/student-career-success"
)


# ============================================================
# METADATA
# ============================================================

METADATA = {

    "final_score": 78.0

}


print()
print("=" * 80)

print(
    "        CHRONOPATH AI - REGISTRY TEST"
)

print("=" * 80)

print()


# ============================================================
# MASTER EVALUATION
# ============================================================

result = evaluate_dataset(

    file_path=FILE_PATH,

    title=TITLE,

    description=DESCRIPTION,

    metadata=METADATA

)


# ============================================================
# ADD TO REGISTRY
# ============================================================

record = add_dataset(

    master_result=result,

    kaggle_reference=KAGGLE_REFERENCE

)


print(
    "Dataset successfully added to registry."
)

print()

print(
    f"Registry location:"
)

print(
    get_registry_path()
)


# ============================================================
# DISPLAY
# ============================================================

display_registry()