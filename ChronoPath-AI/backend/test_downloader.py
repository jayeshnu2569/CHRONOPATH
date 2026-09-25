from dataset_engine.kaggle_downloader import (
    fetch_dataset
)


# ============================================================
# FIRST DOWNLOAD TEST
# ============================================================

KAGGLE_REFERENCE = (
    "shambhurajejagadale/"
    "student-placement-and-career-success-dataset-2026"
)


result = fetch_dataset(
    KAGGLE_REFERENCE
)


print()
print("=" * 80)

print(
    "DOWNLOAD TEST COMPLETE"
)

print("=" * 80)

print()

print(
    f"Reference: "
    f"{result['kaggle_reference']}"
)

print(
    f"Directory: "
    f"{result['directory']}"
)

print()

print(
    "Files:"
)

for file in result["files"]:

    print(
        f"  - {file}"
    )