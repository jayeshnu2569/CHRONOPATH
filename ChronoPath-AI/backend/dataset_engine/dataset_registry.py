from pathlib import Path
import csv
from datetime import datetime


# ============================================================
# CHRONOPATH AI
# DATASET REGISTRY V1.1
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

REGISTRY_DIR = BASE_DIR / "data" / "registry"

REGISTRY_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REGISTRY_FILE = REGISTRY_DIR / "dataset_registry.csv"


# ============================================================
# REGISTRY FIELDS
# ============================================================

FIELDNAMES = [
    "dataset",
    "kaggle_reference",
    "category",
    "file",

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
# INITIALIZE
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
# READ
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
# WRITE
# ============================================================

def write_registry(records):

    normalized_records = []

    for record in records:

        # ----------------------------------------------------
        # Convert old field names to the new schema
        # ----------------------------------------------------

        normalized = {}

        for field in FIELDNAMES:

            normalized[field] = record.get(
                field,
                ""
            )

        # ----------------------------------------------------
        # Backward compatibility
        # ----------------------------------------------------

        if not normalized["dataset"]:

            normalized["dataset"] = record.get(
                "dataset_name",
                ""
            )

        if not normalized["file"]:

            normalized["file"] = record.get(
                "file_path",
                ""
            )

        # ----------------------------------------------------
        # Normalize list fields
        # ----------------------------------------------------

        for field in [
            "decision_variables",
            "possible_decisions",
            "numeric_variables",
            "categorical_variables",
            "low_value_domains"
        ]:

            value = normalized.get(
                field,
                ""
            )

            if isinstance(value, list):

                normalized[field] = ", ".join(
                    str(item)
                    for item in value
                )

        normalized_records.append(
            normalized
        )

    # --------------------------------------------------------
    # Write clean schema
    # --------------------------------------------------------

    with open(
        REGISTRY_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
            extrasaction="ignore"
        )

        writer.writeheader()

        writer.writerows(
            normalized_records
        )

# ============================================================
# LIST → TEXT
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
# SAVE / UPDATE
# ============================================================

def save_dataset(result):

    initialize_registry()

    records = read_registry()

    dataset_name = str(
        result.get(
            "dataset",
            result.get(
                "dataset_name",
                ""
            )
        )
    ).strip()

    kaggle_reference = str(
        result.get(
            "kaggle_reference",
            ""
        )
    ).strip()


    # ========================================================
    # CREATE RECORD
    # ========================================================

    record = {

        "dataset":
            dataset_name,

        "kaggle_reference":
            kaggle_reference,

        "category":
            result.get(
                "category",
                "other"
            ),

        "file":
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


    # Primary identity = Kaggle reference
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


    # ========================================================
    # UPDATE
    # ========================================================

    if existing_index is not None:

        records[existing_index] = record

        write_registry(
            records
        )

        print(
            f"Registry UPDATED: "
            f"{dataset_name}"
        )

        return existing_index + 1


    # ========================================================
    # ADD
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

    return registry_id


# ============================================================
# GET ALL
# ============================================================

def get_all_datasets():

    return read_registry()


# ============================================================
# CATEGORY
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
# SHORTLIST
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
# TOP DATASETS
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
# STATISTICS
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


# ============================================================
# DISPLAY REGISTRY
# ============================================================

def display_registry():

    records = read_registry()

    print()
    print("=" * 100)
    print(
        "        CHRONOPATH AI - DATASET REGISTRY"
    )
    print("=" * 100)
    print()

    if not records:

        print(
            "Registry is currently empty."
        )

        return


    for index, record in enumerate(
        records,
        start=1
    ):

        print(
            f"{index}. "
            f"{record.get('dataset', 'Unknown')}"
        )

        print(
            f"   Category: "
            f"{record.get('category', 'other')}"
        )

        print(
            f"   Final Score: "
            f"{record.get('final_score', 'N/A')}/100"
        )

        print(
            f"   Status: "
            f"{record.get('status', 'N/A')}"
        )

        print(
            f"   Kaggle: "
            f"{record.get('kaggle_reference', 'N/A')}"
        )

        print(
            "-" * 100
        )
# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================
# ============================================================
# BACKWARD COMPATIBLE ADD DATASET
# ============================================================

def add_dataset(
    dataset=None,
    kaggle_reference="",
    category="other",
    master_result=None,
    **kwargs
):

    # --------------------------------------------------------
    # Normalize master_result
    # --------------------------------------------------------

    if master_result is None:
        master_result = {}

    if not isinstance(master_result, dict):
        master_result = {}


    # --------------------------------------------------------
    # Get dataset name
    # --------------------------------------------------------

    dataset_name = (
        dataset
        or master_result.get("dataset")
        or master_result.get("dataset_name")
        or kwargs.get("dataset_name")
        or "Unknown Dataset"
    )


    # --------------------------------------------------------
    # Helper
    # --------------------------------------------------------

    def value(
        key,
        default=""
    ):

        if key in master_result:
            return master_result[key]

        if key in kwargs:
            return kwargs[key]

        return default


    # --------------------------------------------------------
    # Build normalized registry record
    # --------------------------------------------------------

    result = {

        "dataset":
            dataset_name,

        "kaggle_reference":
            kaggle_reference
            or value(
                "kaggle_reference",
                value(
                    "kaggle_ref",
                    ""
                )
            ),

        "category":
            category
            if category != "other"
            else value(
                "category",
                "other"
            ),

        "file":
            value(
                "file",
                value(
                    "file_path",
                    ""
                )
            ),

        "rows":
            value(
                "rows",
                ""
            ),

        "columns":
            value(
                "columns",
                ""
            ),

        "missing_percentage":
            value(
                "missing_percentage",
                ""
            ),

        "duplicate_percentage":
            value(
                "duplicate_percentage",
                ""
            ),

        "metadata_score":
            value(
                "metadata_score",
                ""
            ),

        "quality_score":
            value(
                "quality_score",
                ""
            ),

        "decision_score":
            value(
                "decision_score",
                ""
            ),

        "semantic_score":
            value(
                "semantic_score",
                ""
            ),

        "final_score":
            value(
                "final_score",
                ""
            ),

        "status":
            value(
                "status",
                ""
            ),

        "quality_status":
            value(
                "quality_status",
                ""
            ),

        "decision_relevance":
            value(
                "decision_relevance",
                ""
            ),

        "decision_variables":
            value(
                "decision_variables",
                []
            ),

        "possible_decisions":
            value(
                "possible_decisions",
                []
            ),

        "numeric_variables":
            value(
                "numeric_variables",
                []
            ),

        "categorical_variables":
            value(
                "categorical_variables",
                []
            ),

        "low_value_domains":
            value(
                "low_value_domains",
                []
            )
    }


    # --------------------------------------------------------
    # Save through the main registry engine
    # --------------------------------------------------------

    return save_dataset(result)# ============================================================
# REGISTRY PATH
# ============================================================

def get_registry_path():
    return REGISTRY_FILE
def display_registry():
    records = read_registry()

    print()
    print("=" * 100)
    print("        CHRONOPATH AI - DATASET REGISTRY")
    print("=" * 100)
    print()

    if not records:
        print("Registry is currently empty.")
        return

    for index, record in enumerate(records, start=1):

        print(
            f"{index}. "
            f"{record.get('dataset', 'Unknown')}"
        )

        print(
            f"   Category: "
            f"{record.get('category', 'other')}"
        )

        print(
            f"   Final Score: "
            f"{record.get('final_score', 'N/A')}/100"
        )

        print(
            f"   Status: "
            f"{record.get('status', 'N/A')}"
        )

        print(
            f"   Kaggle: "
            f"{record.get('kaggle_reference', 'N/A')}"
        )

        print("-" * 100)