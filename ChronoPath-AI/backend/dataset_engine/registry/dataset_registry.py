from pathlib import Path
import csv
from datetime import datetime


# ============================================================
# CHRONOPATH AI
# DATASET REGISTRY V1.1
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

REGISTRY_DIR = BASE_DIR / "data" / "registry"

REGISTRY_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REGISTRY_FILE = REGISTRY_DIR / "dataset_registry.csv"


# ============================================================
# REGISTRY COLUMNS
# ============================================================

FIELDNAMES = [
    "dataset_name",
    "kaggle_reference",
    "category",
    "file_path",

    "rows",
    "columns",

    "missing_percentage",
    "duplicate_percentage",

    "metadata_score",
    "quality_score",
    "decision_score",
    "semantic_score",

    "final_score",
    "status",

    "quality_status",
    "decision_relevance",

    "decision_variables",
    "possible_decisions",

    "numeric_variables",
    "categorical_variables",
    "low_value_domains",

    "processed_at"
]


# ============================================================
# INITIALIZE REGISTRY
# ============================================================

def initialize_registry():

    if not REGISTRY_FILE.exists():

        with open(
            REGISTRY_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=FIELDNAMES
            )

            writer.writeheader()


# ============================================================
# READ REGISTRY
# ============================================================

def read_registry():

    initialize_registry()

    with open(
        REGISTRY_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


# ============================================================
# WRITE REGISTRY
# ============================================================

def write_registry(records):

    with open(
        REGISTRY_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        writer.writeheader()

        writer.writerows(records)


# ============================================================
# CONVERT LIST TO TEXT
# ============================================================

def list_to_text(value):

    if value is None:
        return ""

    if isinstance(value, list):
        return ", ".join(
            str(item)
            for item in value
        )

    return str(value)


# ============================================================
# SAVE / UPDATE DATASET
# ============================================================

def save_dataset(result):

    initialize_registry()

    records = read_registry()

    kaggle_reference = str(
        result.get(
            "kaggle_reference",
            ""
        )
    ).strip()

    dataset_name = str(
        result.get(
            "dataset",
            result.get(
                "dataset_name",
                ""
            )
        )
    ).strip()

    category = str(
        result.get(
            "category",
            "other"
        )
    ).strip()

    # --------------------------------------------------------
    # Build registry record
    # --------------------------------------------------------

    record = {

        "dataset_name": dataset_name,

        "kaggle_reference":
            kaggle_reference,

        "category":
            category,

        "file_path":
            result.get(
                "file",
                result.get(
                    "file_path",
                    ""
                )
            ),

        "rows":
            result.get(
                "rows",
                ""
            ),

        "columns":
            result.get(
                "columns",
                ""
            ),

        "missing_percentage":
            result.get(
                "missing_percentage",
                ""
            ),

        "duplicate_percentage":
            result.get(
                "duplicate_percentage",
                ""
            ),

        "metadata_score":
            result.get(
                "metadata_score",
                ""
            ),

        "quality_score":
            result.get(
                "quality_score",
                ""
            ),

        "decision_score":
            result.get(
                "decision_score",
                ""
            ),

        "semantic_score":
            result.get(
                "semantic_score",
                ""
            ),

        "final_score":
            result.get(
                "final_score",
                ""
            ),

        "status":
            result.get(
                "status",
                ""
            ),

        "quality_status":
            result.get(
                "quality_status",
                ""
            ),

        "decision_relevance":
            result.get(
                "decision_relevance",
                ""
            ),

        "decision_variables":
            list_to_text(
                result.get(
                    "decision_variables",
                    []
                )
            ),

        "possible_decisions":
            list_to_text(
                result.get(
                    "possible_decisions",
                    []
                )
            ),

        "numeric_variables":
            list_to_text(
                result.get(
                    "numeric_variables",
                    []
                )
            ),

        "categorical_variables":
            list_to_text(
                result.get(
                    "categorical_variables",
                    []
                )
            ),

        "low_value_domains":
            list_to_text(
                result.get(
                    "low_value_domains",
                    []
                )
            ),

        "processed_at":
            datetime.now().isoformat()
    }


    # ========================================================
    # FIND EXISTING DATASET
    # ========================================================

    existing_index = None

    # Kaggle reference is the primary identity.
    if kaggle_reference:

        for index, existing in enumerate(records):

            if (
                existing.get(
                    "kaggle_reference",
                    ""
                ).strip()
                == kaggle_reference
            ):

                existing_index = index

                break


    # --------------------------------------------------------
    # UPDATE EXISTING DATASET
    # --------------------------------------------------------

    if existing_index is not None:

        records[existing_index] = record

        write_registry(
            records
        )

        print(
            f"Registry UPDATED: "
            f"{dataset_name}"
        )

        print(
            f"Kaggle: "
            f"{kaggle_reference}"
        )

        return existing_index + 1


    # ========================================================
    # ADD NEW DATASET
    # ========================================================

    records.append(
        record
    )

    write_registry(
        records
    )

    registry_id = len(records)

    print(
        f"Registry ADDED: "
        f"{dataset_name}"
    )

    print(
        f"Kaggle: "
        f"{kaggle_reference}"
    )

    return registry_id


# ============================================================
# GET ALL DATASETS
# ============================================================

def get_all_datasets():

    return read_registry()


# ============================================================
# GET DATASETS BY CATEGORY
# ============================================================

def get_by_category(category):

    records = read_registry()

    return [
        record
        for record in records
        if record.get(
            "category",
            ""
        ).lower()
        == category.lower()
    ]


# ============================================================
# GET SHORTLISTED DATASETS
# ============================================================

def get_shortlisted():

    records = read_registry()

    return [
        record
        for record in records
        if record.get(
            "status",
            ""
        ).upper()
        == "SHORTLIST"
    ]


# ============================================================
# GET TOP DATASETS
# ============================================================

def get_top_datasets(
    limit=10
):

    records = read_registry()

    def score(record):

        try:

            return float(
                record.get(
                    "final_score",
                    0
                )
            )

        except (
            ValueError,
            TypeError
        ):

            return 0


    records.sort(
        key=score,
        reverse=True
    )

    return records[:limit]


# ============================================================
# REGISTRY STATISTICS
# ============================================================

def get_statistics():

    records = read_registry()

    total = len(records)

    shortlisted = sum(
        1
        for record in records
        if record.get(
            "status",
            ""
        ).upper()
        == "SHORTLIST"
    )

    review = sum(
        1
        for record in records
        if record.get(
            "status",
            ""
        ).upper()
        == "REVIEW"
    )

    rejected = sum(
        1
        for record in records
        if record.get(
            "status",
            ""
        ).upper()
        == "REJECT"
    )

    return {
        "total": total,
        "shortlisted": shortlisted,
        "review": review,
        "rejected": rejected
    }