from dataset_engine.kaggle_fetcher import (
    search_kaggle
)

from dataset_engine.dataset_scorer import (
    score_datasets
)


# ============================================================
# CHRONOPATH AI
# DATASET SCORING TEST
# ============================================================

KEYWORD = "career"

TARGET_CATEGORY = "career"


print()
print("=" * 90)
print(
    "        CHRONOPATH AI - DATASET INTELLIGENCE ENGINE"
)
print("=" * 90)

print()

print(
    f"Searching Kaggle for: {KEYWORD}"
)

print()


# ------------------------------------------------------------
# SEARCH
# ------------------------------------------------------------

datasets = search_kaggle(
    KEYWORD,
    limit=20
)


print(
    f"Found {len(datasets)} candidate datasets."
)

print()


# ------------------------------------------------------------
# SCORE
# ------------------------------------------------------------

results = score_datasets(
    datasets,
    target_category=TARGET_CATEGORY
)


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------

for index, result in enumerate(
    results,
    start=1
):

    print("=" * 90)

    print(
        f"{index}. {result['title']}"
    )

    print(
        f"   Ref: {result['ref']}"
    )

    print(
        f"   Category: "
        f"{result['category']}"
    )

    print()

    print(
        f"   Relevance:       "
        f"{result['relevance']}/100"
    )

    print(
        f"   Popularity:      "
        f"{result['popularity']}/100"
    )

    print(
        f"   Usability:       "
        f"{result['usability']}/100"
    )

    print(
        f"   Freshness:       "
        f"{result['freshness']}/100"
    )

    print(
        f"   Decision Value:  "
        f"{result['decision_value']}/100"
    )

    print()

    print(
        f"   FINAL SCORE:     "
        f"{result['final_score']}/100"
    )

    print(
        f"   STATUS:          "
        f"{result['status']}"
    )

print()

print("=" * 90)

print(
    "        SCORING COMPLETE"
)

print("=" * 90)