from dataset_engine.kaggle_fetcher import (
    search_kaggle,
    display_results
)


# ============================================================
# CHRONOPATH AI - KAGGLE API TEST
# ============================================================

KEYWORD = "career"


print()
print("=" * 80)
print(
    "        CHRONOPATH AI - KAGGLE API SEARCH"
)
print("=" * 80)

print()
print(
    f"Searching Kaggle for: {KEYWORD}"
)
print()


datasets = search_kaggle(
    KEYWORD,
    limit=20
)


display_results(
    datasets
)