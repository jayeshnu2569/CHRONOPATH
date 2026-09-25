from dataset_engine.kaggle_downloader import fetch_dataset


# ============================================================
# CHRONOPATH AI
# FIVE DATASET DOWNLOAD TEST
# ============================================================

DATASETS = [

    # 1. CAREER
    {
        "category": "career",
        "reference": (
            "shambhurajejagadale/"
            "student-placement-and-career-success-dataset-2026"
        )
    },

    # 2. EDUCATION
    {
        "category": "education",
        "reference": (
            "adilshamim8/"
            "education-and-career-success"
        )
    },

    # 3. FINANCE
    {
        "category": "finance",
        "reference": (
            "jealousleopard/"
            "loan-prediction-problem-dataset"
        )
    },

    # 4. BUSINESS
    {
        "category": "business",
        "reference": (
            "olistbr/"
            "brazilian-ecommerce"
        )
    },

    # 5. TECHNOLOGY
    {
        "category": "technology",
        "reference": (
            "shreyasur965/"
            "mobile-phone-price-prediction"
        )
    }
]


# ============================================================
# RESULTS
# ============================================================

successful = []
failed = []


print()
print("=" * 80)

print(
    "        CHRONOPATH AI - FIVE DATASET TEST"
)

print("=" * 80)

print()


# ============================================================
# DOWNLOAD DATASETS
# ============================================================

for number, dataset in enumerate(
    DATASETS,
    start=1
):

    category = dataset["category"]
    reference = dataset["reference"]

    print()
    print("=" * 80)

    print(
        f"DATASET {number}/5"
    )

    print(
        f"Category: {category}"
    )

    print(
        f"Kaggle: {reference}"
    )

    print("=" * 80)

    try:

        result = fetch_dataset(
            reference
        )

        successful.append({

            "category": category,

            "reference": reference,

            "result": result

        })

        print()
        print(
            f"SUCCESS: {category}"
        )

    except Exception as error:

        failed.append({

            "category": category,

            "reference": reference,

            "error": str(error)

        })

        print()
        print(
            f"FAILED: {category}"
        )

        print(
            f"Reason: {error}"
        )

        print(
            "Continuing to next dataset..."
        )


# ============================================================
# FINAL REPORT
# ============================================================

print()
print("=" * 80)

print(
    "        FIVE DATASET TEST COMPLETE"
)

print("=" * 80)

print()

print(
    f"Successful: {len(successful)}/5"
)

print(
    f"Failed:     {len(failed)}/5"
)

print()


# ============================================================
# SUCCESSFUL DATASETS
# ============================================================

if successful:

    print(
        "SUCCESSFUL DATASETS"
    )

    print("-" * 80)

    for item in successful:

        result = item["result"]

        print(
            f"[✓] "
            f"{item['category'].upper()} "
            f"- "
            f"{item['reference']}"
        )

        print(
            f"    Location: "
            f"{result['directory']}"
        )

        print(
            f"    Files found: "
            f"{len(result['files'])}"
        )

        for file in result["files"]:

            print(
                f"      - {file}"
            )

        print()


# ============================================================
# FAILED DATASETS
# ============================================================

if failed:

    print(
        "FAILED DATASETS"
    )

    print("-" * 80)

    for item in failed:

        print(
            f"[✗] "
            f"{item['category'].upper()} "
            f"- "
            f"{item['reference']}"
        )

        print(
            f"    Reason: "
            f"{item['error']}"
        )

        print()


print("=" * 80)

print(
    "DOWNLOAD BATCH TEST FINISHED"
)

print("=" * 80)