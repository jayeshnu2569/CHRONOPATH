from dataset_engine.master_evaluator import (
    evaluate_dataset,
    display_master_result
)


# ============================================================
# CHRONOPATH AI
# MASTER ENGINE TEST
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


# Simulated Kaggle metadata score
#
# Later this will come directly from
# the Kaggle fetcher.

METADATA = {

    "final_score": 78.0

}


# ============================================================
# RUN MASTER ENGINE
# ============================================================

result = evaluate_dataset(

    file_path=FILE_PATH,

    title=TITLE,

    description=DESCRIPTION,

    metadata=METADATA

)


# ============================================================
# DISPLAY
# ============================================================

display_master_result(
    result
)