from pathlib import Path

from dataset_engine.kaggle_downloader import (
    find_data_files
)

from dataset_engine.kaggle_fetcher import (
    get_dataset_metadata
)

from dataset_engine.master_evaluator import (
    evaluate_dataset,
    display_master_result
)

from dataset_engine.dataset_registry import (
    add_dataset
)


# ============================================================
# CHRONOPATH AI
# END-TO-END DATASET PIPELINE
# ============================================================

DOWNLOAD_ROOT = Path(
    "./data/kaggle_downloads"
)


# ============================================================
# DATASET INFORMATION
# ============================================================

DATASETS = [

    {
        "category": "career",
        "reference": (
            "shambhurajejagadale/"
            "student-placement-and-career-success-dataset-2026"
        ),
        "title": (
            "Student Placement & Career Success Dataset 2026"
        ),
        "description": (
            "Student education, placement, "
            "career and employment success data."
        )
    },

    {
        "category": "education",
        "reference": (
            "adilshamim8/"
            "education-and-career-success"
        ),
        "title": (
            "Education & Career Success"
        ),
        "description": (
            "Education and career-related "
            "student success information."
        )
    },

    {
        "category": "finance",
        "reference": (
            "jealousleopard/"
            "loan-prediction-problem-dataset"
        ),
        "title": (
            "Loan Prediction Dataset"
        ),
        "description": (
            "Financial and loan application "
            "information used for loan decisions."
        )
    },

    {
        "category": "business",
        "reference": (
            "olistbr/"
            "brazilian-ecommerce"
        ),
        "title": (
            "Brazilian E-Commerce Dataset"
        ),
        "description": (
            "E-commerce orders, customers, "
            "products, payments and reviews."
        )
    },

    {
        "category": "technology",
        "reference": (
            "shreyasur965/"
            "mobile-phone-price-prediction"
        ),
        "title": (
            "Mobile Phone Price Prediction"
        ),
        "description": (
            "Mobile phone specifications and "
            "pricing information."
        )
    }
]


# ============================================================
# FIND DOWNLOAD DIRECTORY
# ============================================================

def get_dataset_directory(
    kaggle_reference
):

    safe_name = (
        kaggle_reference
        .replace("/", "_")
        .replace("\\", "_")
    )

    return DOWNLOAD_ROOT / safe_name


# ============================================================
# SELECT BEST DATA FILE
# ============================================================

def select_data_file(
    files
):

    if not files:

        return None

    preferred_extensions = [
        ".csv",
        ".parquet",
        ".json",
        ".xlsx",
        ".xls"
    ]

    for extension in preferred_extensions:

        for file in files:

            if Path(file).suffix.lower() == extension:

                return Path(file)

    return Path(files[0])


# ============================================================
# RUN ONE DATASET
# ============================================================

def process_dataset(
    dataset
):

    reference = dataset["reference"]
    category = dataset["category"]
    title = dataset["title"]
    description = dataset["description"]

    print()
    print("=" * 80)

    print(
        "PROCESSING DATASET"
    )

    print("=" * 80)

    print(
        f"Category: {category}"
    )

    print(
        f"Dataset: {title}"
    )

    print(
        f"Kaggle: {reference}"
    )

    print()

    # --------------------------------------------------------
    # Locate downloaded dataset
    # --------------------------------------------------------

    directory = get_dataset_directory(
        reference
    )

    if not directory.exists():

        print(
            "STATUS: DOWNLOAD NOT FOUND"
        )

        print(
            f"Expected directory: {directory}"
        )

        return {
            "success": False,
            "reason": "download_not_found"
        }

    # --------------------------------------------------------
    # Find data files
    # --------------------------------------------------------

    files = find_data_files(
        directory
    )

    if not files:

        print(
            "STATUS: NO DATA FILE FOUND"
        )

        return {
            "success": False,
            "reason": "no_data_file"
        }

    print(
        f"Data files found: {len(files)}"
    )

    for file in files:

        print(
            f"  - {file}"
        )

    # --------------------------------------------------------
    # Select primary file
    # --------------------------------------------------------

    data_file = select_data_file(
        files
    )

    if data_file is None:

        print(
            "STATUS: COULD NOT SELECT DATA FILE"
        )

        return {
            "success": False,
            "reason": "file_selection_failed"
        }

    print()

    print(
        f"Primary file: {data_file}"
    )

    # --------------------------------------------------------
    # Get REAL Kaggle metadata
    # --------------------------------------------------------

    try:

        kaggle_metadata = get_dataset_metadata(
            reference,
            category=category
        )

    except Exception as error:

        print()

        print(
            "WARNING: Could not retrieve Kaggle metadata."
        )

        print(
            f"Reason: {error}"
        )

        kaggle_metadata = {
            "metadata_score": 0
        }

    print()
    print(
        "KAGGLE METADATA"
    )

    print("-" * 80)

    print(
        f"Relevance:       "
        f"{kaggle_metadata.get('relevance', 0)}/100"
    )

    print(
        f"Popularity:      "
        f"{kaggle_metadata.get('popularity', 0)}/100"
    )

    print(
        f"Usability:       "
        f"{kaggle_metadata.get('usability', 0)}/100"
    )

    print(
        f"Freshness:       "
        f"{kaggle_metadata.get('freshness', 0)}/100"
    )

    print(
        f"Decision Value:  "
        f"{kaggle_metadata.get('decision_value', 0)}/100"
    )

    print(
        f"Metadata Score:  "
        f"{kaggle_metadata.get('metadata_score', 0)}/100"
    )

    # --------------------------------------------------------
    # Master evaluation
    # --------------------------------------------------------

    try:

       result = evaluate_dataset(
    file_path=str(data_file),
    title=title,
    description=description,
    category=category,
    metadata=kaggle_metadata
)

    except Exception as error:

        print()

        print(
            "STATUS: EVALUATION FAILED"
        )

        print(
            f"Reason: {error}"
        )

        return {
            "success": False,
            "reason": str(error)
        }

    # --------------------------------------------------------
    # Add to registry
    # --------------------------------------------------------

    try:

        add_dataset(

            master_result=result,

            kaggle_reference=reference

        )

    except Exception as error:

        print()

        print(
            "STATUS: REGISTRY FAILED"
        )

        print(
            f"Reason: {error}"
        )

        return {
            "success": False,
            "reason": str(error)
        }

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    display_master_result(
        result
    )

    return {
        "success": True,
        "result": result
    }


# ============================================================
# RUN PIPELINE
# ============================================================

def run_pipeline():

    print()
    print("=" * 80)

    print(
        "        CHRONOPATH AI"
    )

    print(
        "        END-TO-END DATASET PIPELINE"
    )

    print("=" * 80)

    print()

    successful = []
    failed = []

    # --------------------------------------------------------
    # Process datasets
    # --------------------------------------------------------

    for index, dataset in enumerate(
        DATASETS,
        start=1
    ):

        print()
        print(
            f"PIPELINE DATASET "
            f"{index}/{len(DATASETS)}"
        )

        result = process_dataset(
            dataset
        )

        if result["success"]:

            successful.append(
                dataset
            )

        else:

            failed.append({

                "dataset": dataset,

                "reason":
                    result["reason"]

            })

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print()
    print("=" * 80)

    print(
        "        PIPELINE COMPLETE"
    )

    print("=" * 80)

    print()

    print(
        f"Successful: "
        f"{len(successful)}/{len(DATASETS)}"
    )

    print(
        f"Failed:     "
        f"{len(failed)}/{len(DATASETS)}"
    )

    print()

    # --------------------------------------------------------
    # Successful
    # --------------------------------------------------------

    if successful:

        print(
            "SUCCESSFUL DATASETS"
        )

        print("-" * 80)

        for dataset in successful:

            print(
                f"[✓] "
                f"{dataset['category'].upper()} "
                f"- "
                f"{dataset['title']}"
            )

    # --------------------------------------------------------
    # Failed
    # --------------------------------------------------------

    if failed:

        print()
        print(
            "FAILED DATASETS"
        )

        print("-" * 80)

        for item in failed:

            print(
                f"[✗] "
                f"{item['dataset']['category'].upper()} "
                f"- "
                f"{item['dataset']['title']}"
            )

            print(
                f"    Reason: "
                f"{item['reason']}"
            )

    print()
    print("=" * 80)

    print(
        "        CHRONOPATH PIPELINE FINISHED"
    )

    print("=" * 80)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_pipeline()