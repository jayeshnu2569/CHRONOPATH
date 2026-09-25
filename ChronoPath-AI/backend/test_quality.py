from dataset_engine.dataset_quality import (
    analyze_dataset
)


# ============================================================
# CHRONOPATH AI
# DATASET QUALITY SCANNER TEST
# ============================================================

FILE_PATH = (
    r".\data\quality_test\test_dataset.csv"
)


print()
print("=" * 80)
print(
    "        CHRONOPATH AI - DATASET QUALITY SCANNER"
)
print("=" * 80)

print()

print(
    f"Scanning: {FILE_PATH}"
)

print()


result = analyze_dataset(
    FILE_PATH
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print(
    "=" * 80
)

print(
    f"File: "
    f"{result['file']}"
)

print(
    f"Readable: "
    f"{result['readable']}"
)

print()

print(
    f"Rows: "
    f"{result.get('rows', 'N/A')}"
)

print(
    f"Columns: "
    f"{result.get('columns', 'N/A')}"
)

print()

print(
    f"Missing Cells: "
    f"{result.get('missing_cells', 'N/A')}"
)

print(
    f"Missing Percentage: "
    f"{result.get('missing_percentage', 'N/A')}%"
)

print()

print(
    f"Duplicate Rows: "
    f"{result.get('duplicate_rows', 'N/A')}"
)

print(
    f"Duplicate Percentage: "
    f"{result.get('duplicate_percentage', 'N/A')}%"
)

print()

print(
    f"Empty Columns: "
    f"{result.get('empty_column_count', 'N/A')}"
)

print(
    f"Constant Columns: "
    f"{result.get('constant_column_count', 'N/A')}"
)

print()

print(
    f"Usable Columns: "
    f"{result.get('usable_columns', 'N/A')}"
)

print(
    f"Unusable Columns: "
    f"{result.get('unusable_columns', 'N/A')}"
)

print(
    f"Column Usability: "
    f"{result.get('column_usability_percentage', 'N/A')}%"
)

print()

print(
    f"QUALITY SCORE: "
    f"{result.get('quality_score', 'N/A')}/100"
)

print(
    f"STATUS: "
    f"{result.get('status', 'N/A')}"
)

if result.get("error"):

    print()

    print(
        f"ERROR: "
        f"{result['error']}"
    )

print()

print("=" * 80)

print(
    "        SCAN COMPLETE"
)

print("=" * 80)