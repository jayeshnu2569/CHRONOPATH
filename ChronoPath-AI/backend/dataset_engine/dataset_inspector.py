from pathlib import Path
import pandas as pd


# ============================================================
# CHRONOPATH AI
# RELATIONSHIP-AWARE MULTI-FILE DATASET INSPECTOR
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".parquet",
    ".json",
    ".xlsx",
    ".xls",
}


# ============================================================
# BASIC FILE DISCOVERY
# ============================================================

def inspectable_files(files):
    """
    Return only files that ChronoPath can inspect.
    """

    return [
        Path(file)
        for file in files
        if Path(file).suffix.lower()
        in SUPPORTED_EXTENSIONS
    ]


# ============================================================
# LOAD DATA
# ============================================================

def load_dataframe(file_path):
    """
    Load a supported dataset file into pandas.
    Returns None if the file cannot be read.
    """

    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    try:

        if extension == ".csv":
            return pd.read_csv(
                file_path,
                low_memory=False
            )

        if extension == ".parquet":
            return pd.read_parquet(
                file_path
            )

        if extension == ".json":
            return pd.read_json(
                file_path
            )

        if extension in {".xlsx", ".xls"}:
            return pd.read_excel(
                file_path
            )

    except Exception:
        return None

    return None


# ============================================================
# COLUMN TYPE DETECTION
# ============================================================

def detect_column_types(df):

    numeric = []
    categorical = []
    datetime_columns = []

    for column in df.columns:

        series = df[column]

        if pd.api.types.is_numeric_dtype(series):
            numeric.append(column)

        elif pd.api.types.is_datetime64_any_dtype(series):
            datetime_columns.append(column)

        else:
            categorical.append(column)

    return {
        "numeric": numeric,
        "categorical": categorical,
        "datetime": datetime_columns,
    }


# ============================================================
# ID DETECTION
# ============================================================

def detect_id_columns(df):

    id_columns = []

    for column in df.columns:

        name = str(column).strip().lower()

        if (
            name == "id"
            or name.endswith("_id")
            or name.endswith("id")
            or "identifier" in name
        ):
            id_columns.append(column)

    return id_columns


# ============================================================
# UNIQUE ID DETECTION
# ============================================================

def detect_unique_id_columns(df):

    unique_ids = []

    if len(df) == 0:
        return unique_ids

    for column in detect_id_columns(df):

        try:

            unique_ratio = (
                df[column]
                .nunique(dropna=True)
                / len(df)
            )

            if unique_ratio >= 0.95:
                unique_ids.append(column)

        except Exception:
            continue

    return unique_ids


# ============================================================
# FILE SCORE
# ============================================================

def calculate_file_score(
    file_path,
    df
):

    score = 0.0

    rows = len(df)
    columns = len(df.columns)

    # --------------------------------------------------------
    # Dataset size
    # --------------------------------------------------------

    if rows >= 100000:
        score += 30

    elif rows >= 50000:
        score += 25

    elif rows >= 10000:
        score += 20

    elif rows >= 1000:
        score += 15

    elif rows >= 100:
        score += 10

    else:
        score += 5

    # --------------------------------------------------------
    # Column richness
    # --------------------------------------------------------

    if columns >= 20:
        score += 30

    elif columns >= 10:
        score += 25

    elif columns >= 5:
        score += 15

    elif columns >= 2:
        score += 10

    # --------------------------------------------------------
    # ID availability
    # --------------------------------------------------------

    id_columns = detect_id_columns(df)

    if len(id_columns) >= 3:
        score += 20

    elif len(id_columns) == 2:
        score += 15

    elif len(id_columns) == 1:
        score += 10

    # --------------------------------------------------------
    # Analytical columns
    # --------------------------------------------------------

    useful_keywords = [
        "price",
        "salary",
        "income",
        "score",
        "rating",
        "status",
        "category",
        "date",
        "amount",
        "quantity",
        "revenue",
        "target",
        "outcome",
        "payment",
        "review",
        "order",
    ]

    useful_count = 0

    for column in df.columns:

        column_name = str(column).lower()

        if any(
            keyword in column_name
            for keyword in useful_keywords
        ):
            useful_count += 1

    score += min(
        useful_count * 3,
        20
    )

    return min(
        round(score, 2),
        100.0
    )


# ============================================================
# RELATIONSHIP DETECTION
# ============================================================

def detect_relationships(
    inspections
):

    relationships = []

    successful = [
        item
        for item in inspections
        if item.get("success")
    ]

    for i in range(
        len(successful)
    ):

        first = successful[i]

        first_ids = set(
            first.get(
                "id_columns",
                []
            )
        )

        if not first_ids:
            continue

        for j in range(
            i + 1,
            len(successful)
        ):

            second = successful[j]

            second_ids = set(
                second.get(
                    "id_columns",
                    []
                )
            )

            shared = sorted(
                first_ids.intersection(
                    second_ids
                )
            )

            if not shared:
                continue

            for column in shared:

                relationships.append(
                    {
                        "file_a": first["name"],
                        "file_b": second["name"],
                        "shared_column": column,
                    }
                )

    return relationships


# ============================================================
# RELATIONSHIP STATISTICS
# ============================================================

def calculate_relationship_stats(
    inspections,
    relationships
):

    stats = {}

    for item in inspections:

        name = item.get(
            "name"
        )

        stats[name] = {
            "relationship_count": 0,
            "connected_files": 0,
            "relationship_columns": [],
        }

    for relationship in relationships:

        file_a = relationship[
            "file_a"
        ]

        file_b = relationship[
            "file_b"
        ]

        column = relationship[
            "shared_column"
        ]

        if file_a in stats:

            stats[file_a][
                "relationship_count"
            ] += 1

            stats[file_a][
                "connected_files"
            ] += 1

            stats[file_a][
                "relationship_columns"
            ].append(column)

        if file_b in stats:

            stats[file_b][
                "relationship_count"
            ] += 1

            stats[file_b][
                "connected_files"
            ] += 1

            stats[file_b][
                "relationship_columns"
            ].append(column)

    return stats


# ============================================================
# TABLE ROLE CLASSIFICATION
# ============================================================

def classify_table_role(
    inspection,
    relationship_stats
):

    if not inspection.get("success"):
        return "UNKNOWN"

    rows = inspection.get(
        "rows",
        0
    )

    columns = inspection.get(
        "columns",
        0
    )

    id_columns = inspection.get(
        "id_columns",
        []
    )

    unique_ids = inspection.get(
        "unique_id_columns",
        []
    )

    relationship_count = (
        relationship_stats
        .get(
            inspection["name"],
            {}
        )
        .get(
            "relationship_count",
            0
        )
    )

    connected_files = (
        relationship_stats
        .get(
            inspection["name"],
            {}
        )
        .get(
            "connected_files",
            0
        )
    )

    name = inspection[
        "name"
    ].lower()

    # --------------------------------------------------------
    # Reference table
    # --------------------------------------------------------

    reference_keywords = [
        "translation",
        "lookup",
        "mapping",
        "reference",
        "dictionary",
    ]

    if any(
        keyword in name
        for keyword in reference_keywords
    ):
        return "REFERENCE"

    # Small lookup-like tables
    if (
        rows <= 500
        and columns <= 5
        and relationship_count <= 1
    ):
        return "REFERENCE"

    # --------------------------------------------------------
    # Bridge table
    # --------------------------------------------------------

    if (
        columns <= 10
        and len(id_columns) >= 2
        and relationship_count >= 2
    ):
        return "BRIDGE"

    # --------------------------------------------------------
    # Fact table
    # --------------------------------------------------------

    fact_keywords = [
        "order",
        "payment",
        "transaction",
        "sales",
        "sale",
        "invoice",
        "event",
        "booking",
        "review",
        "item",
    ]

    fact_name = any(
        keyword in name
        for keyword in fact_keywords
    )

    if (
        relationship_count >= 1
        and (
            fact_name
            or columns >= 5
            or rows >= 10000
        )
    ):
        return "FACT"

    # --------------------------------------------------------
    # Dimension table
    # --------------------------------------------------------

    if (
        len(unique_ids) >= 1
        and columns >= 3
        and connected_files >= 1
    ):
        return "DIMENSION"

    # --------------------------------------------------------
    # Supporting
    # --------------------------------------------------------

    return "SUPPORTING"


# ============================================================
# RELATIONSHIP-AWARE SCORE
# ============================================================

def calculate_intelligence_score(
    inspection,
    relationship_stats
):

    base_score = inspection.get(
        "score",
        0
    )

    stats = relationship_stats.get(
        inspection["name"],
        {}
    )

    relationship_count = stats.get(
        "relationship_count",
        0
    )

    connected_files = stats.get(
        "connected_files",
        0
    )

    # Relationship bonus
    relationship_bonus = min(
        relationship_count * 5,
        20
    )

    # Connected-file bonus
    connectivity_bonus = min(
        connected_files * 3,
        15
    )

    final_score = (
        base_score
        + relationship_bonus
        + connectivity_bonus
    )

    return round(
        min(
            final_score,
            100.0
        ),
        2
    )


# ============================================================
# DATASET STRUCTURE
# ============================================================

def determine_dataset_structure(
    inspections,
    relationships
):

    successful_count = sum(
        1
        for item in inspections
        if item.get("success")
    )

    if successful_count <= 1:
        return "SINGLE_TABLE"

    if relationships:
        return "MULTI_TABLE"

    return "MULTI_FILE"


# ============================================================
# PRIMARY FILE SELECTION
# ============================================================

def select_primary_file(
    inspections
):

    successful = [
        item
        for item in inspections
        if item.get("success")
    ]

    if not successful:
        return None

    # Prefer FACT tables.
    facts = [
        item
        for item in successful
        if item.get(
            "table_role"
        ) == "FACT"
    ]

    candidates = (
        facts
        if facts
        else successful
    )

    candidates.sort(
        key=lambda item: (
            item.get(
                "intelligence_score",
                0
            ),
            item.get(
                "relationship_count",
                0
            ),
            item.get(
                "rows",
                0
            ),
        ),
        reverse=True
    )

    return candidates[0]


# ============================================================
# COMPLETE DATASET INSPECTION
# ============================================================

def inspect_dataset(
    files
):

    files = inspectable_files(
        files
    )

    inspections = []

    for file in files:

        result = inspect_file(
            file
        )

        inspections.append(
            result
        )

    relationships = detect_relationships(
        inspections
    )

    relationship_stats = (
        calculate_relationship_stats(
            inspections,
            relationships
        )
    )

    # --------------------------------------------------------
    # Apply relationship intelligence
    # --------------------------------------------------------

    for item in inspections:

        stats = relationship_stats.get(
            item.get("name"),
            {}
        )

        item[
            "relationship_count"
        ] = stats.get(
            "relationship_count",
            0
        )

        item[
            "connected_files"
        ] = stats.get(
            "connected_files",
            0
        )

        item[
            "relationship_columns"
        ] = sorted(
            set(
                stats.get(
                    "relationship_columns",
                    []
                )
            )
        )

        # Unique IDs
        if item.get("success"):

            df = load_dataframe(
                item["file"]
            )

            if df is not None:

                item[
                    "unique_id_columns"
                ] = [
                    str(column)
                    for column
                    in detect_unique_id_columns(
                        df
                    )
                ]

            else:

                item[
                    "unique_id_columns"
                ] = []

        else:

            item[
                "unique_id_columns"
            ] = []

        # Table role
        item[
            "table_role"
        ] = classify_table_role(
            item,
            relationship_stats
        )

        # Intelligence score
        item[
            "intelligence_score"
        ] = calculate_intelligence_score(
            item,
            relationship_stats
        )

    structure = (
        determine_dataset_structure(
            inspections,
            relationships
        )
    )

    primary = select_primary_file(
        inspections
    )

    supporting = [
        item
        for item in inspections
        if (
            item.get("success")
            and (
                primary is None
                or item["file"]
                != primary["file"]
            )
        )
    ]

    return {
        "file_count": len(files),
        "successful_files": sum(
            1
            for item in inspections
            if item.get("success")
        ),
        "structure": structure,
        "files": inspections,
        "relationships": relationships,
        "relationship_stats": relationship_stats,
        "primary_file": primary,
        "supporting_files": supporting,
    }


# ============================================================
# INSPECT ONE FILE
# ============================================================

def inspect_file(
    file_path
):

    file_path = Path(
        file_path
    )

    df = load_dataframe(
        file_path
    )

    if df is None:

        return {
            "file": str(file_path),
            "name": file_path.name,
            "success": False,
            "reason": "read_failed",
        }

    column_types = (
        detect_column_types(
            df
        )
    )

    id_columns = (
        detect_id_columns(
            df
        )
    )

    missing_percentage = 0.0

    if df.size > 0:

        missing_percentage = (
            df.isna()
            .sum()
            .sum()
            / df.size
        ) * 100

    score = calculate_file_score(
        file_path,
        df
    )

    return {
        "file": str(file_path),
        "name": file_path.name,
        "success": True,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": [
            str(column)
            for column in df.columns
        ],
        "id_columns": [
            str(column)
            for column in id_columns
        ],
        "numeric_columns": [
            str(column)
            for column
            in column_types["numeric"]
        ],
        "categorical_columns": [
            str(column)
            for column
            in column_types["categorical"]
        ],
        "datetime_columns": [
            str(column)
            for column
            in column_types["datetime"]
        ],
        "missing_percentage": round(
            missing_percentage,
            2
        ),
        "score": score,
    }


# ============================================================
# DISPLAY INSPECTION
# ============================================================

def display_inspection(
    inspection
):

    print()
    print("=" * 80)
    print(
        "        CHRONOPATH AI - DATASET INTELLIGENCE"
    )
    print("=" * 80)
    print()

    print(
        f"Files discovered: "
        f"{inspection['file_count']}"
    )

    print(
        f"Successfully inspected: "
        f"{inspection['successful_files']}"
    )

    print(
        f"Dataset structure: "
        f"{inspection['structure']}"
    )

    print()
    print("-" * 80)
    print("FILE ANALYSIS")
    print("-" * 80)

    for index, item in enumerate(
        inspection["files"],
        start=1
    ):

        print()
        print(
            f"{index}. "
            f"{item.get('name', 'Unknown')}"
        )

        if not item.get("success"):

            print(
                "   Status: READ FAILED"
            )

            continue

        print(
            f"   Rows: "
            f"{item['rows']}"
        )

        print(
            f"   Columns: "
            f"{item['columns']}"
        )

        print(
            f"   Missing: "
            f"{item['missing_percentage']}%"
        )

        print(
            f"   IDs: "
            f"{', '.join(item['id_columns']) or 'None'}"
        )

        print(
            f"   Unique IDs: "
            f"{', '.join(item.get('unique_id_columns', [])) or 'None'}"
        )

        print(
            f"   Relationships: "
            f"{item.get('relationship_count', 0)}"
        )

        print(
            f"   Connected Files: "
            f"{item.get('connected_files', 0)}"
        )

        print(
            f"   Role: "
            f"{item.get('table_role', 'UNKNOWN')}"
        )

        print(
            f"   Base Score: "
            f"{item['score']}/100"
        )

        print(
            f"   Intelligence Score: "
            f"{item.get('intelligence_score', 0)}/100"
        )

    print()
    print("-" * 80)
    print("RELATIONSHIPS")
    print("-" * 80)

    if not inspection[
        "relationships"
    ]:

        print(
            "No shared ID relationships detected."
        )

    else:

        for relationship in inspection[
            "relationships"
        ]:

            print(
                f"{relationship['file_a']}"
            )

            print(
                f"  ↕ "
                f"{relationship['shared_column']}"
            )

            print(
                f"{relationship['file_b']}"
            )

            print(
                "-" * 40
            )

    print()
    print("-" * 80)
    print("PRIMARY FILE")
    print("-" * 80)

    primary = inspection[
        "primary_file"
    ]

    if primary:

        print(
            f"Recommended: "
            f"{primary['name']}"
        )

        print(
            f"Role: "
            f"{primary.get('table_role', 'UNKNOWN')}"
        )

        print(
            f"Intelligence Score: "
            f"{primary.get('intelligence_score', 0)}/100"
        )

    else:

        print(
            "No usable primary file found."
        )

    print()
    print("=" * 80)