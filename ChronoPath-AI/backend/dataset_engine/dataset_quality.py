from pathlib import Path
import pandas as pd


# ============================================================
# CHRONOPATH AI
# DATASET QUALITY SCANNER
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json"
}


# ============================================================
# FILE DISCOVERY
# ============================================================

def find_dataset_files(folder):

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {folder}"
        )

    files = []

    for file in folder.rglob("*"):

        if (
            file.is_file()
            and file.suffix.lower()
            in SUPPORTED_EXTENSIONS
        ):
            files.append(file)

    return files


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".csv":

        return pd.read_csv(
            file_path,
            low_memory=False
        )

    if extension in {".xlsx", ".xls"}:

        return pd.read_excel(
            file_path
        )

    if extension == ".json":

        return pd.read_json(
            file_path
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


# ============================================================
# BASIC STRUCTURE ANALYSIS
# ============================================================

def analyze_structure(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns)
    }


# ============================================================
# MISSING VALUE ANALYSIS
# ============================================================

def analyze_missing_values(df):

    total_cells = (
        df.shape[0] *
        df.shape[1]
    )

    if total_cells == 0:

        return {
            "missing_cells": 0,
            "missing_percentage": 100.0
        }

    missing_cells = int(
        df.isna().sum().sum()
    )

    missing_percentage = (
        missing_cells /
        total_cells
    ) * 100

    return {
        "missing_cells": missing_cells,
        "missing_percentage": round(
            missing_percentage,
            2
        )
    }


# ============================================================
# DUPLICATE ANALYSIS
# ============================================================

def analyze_duplicates(df):

    rows = len(df)

    duplicate_rows = int(
        df.duplicated().sum()
    )

    if rows == 0:

        duplicate_percentage = 100.0

    else:

        duplicate_percentage = (
            duplicate_rows /
            rows
        ) * 100

    return {
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": round(
            duplicate_percentage,
            2
        )
    }


# ============================================================
# EMPTY COLUMN ANALYSIS
# ============================================================

def analyze_empty_columns(df):

    empty_columns = []

    for column in df.columns:

        if df[column].isna().all():

            empty_columns.append(
                str(column)
            )

    return {
        "empty_columns": empty_columns,
        "empty_column_count": len(
            empty_columns
        )
    }


# ============================================================
# CONSTANT COLUMN ANALYSIS
# ============================================================

def analyze_constant_columns(df):

    constant_columns = []

    for column in df.columns:

        if df[column].nunique(
            dropna=False
        ) <= 1:

            constant_columns.append(
                str(column)
            )

    return {
        "constant_columns": constant_columns,
        "constant_column_count": len(
            constant_columns
        )
    }


# ============================================================
# DATA TYPE ANALYSIS
# ============================================================

def analyze_data_types(df):

    data_types = {}

    for column in df.columns:

        data_types[str(column)] = str(
            df[column].dtype
        )

    return {
        "data_types": data_types
    }


# ============================================================
# COLUMN USABILITY
# ============================================================

def analyze_column_usability(df):

    usable_columns = 0
    unusable_columns = 0

    for column in df.columns:

        series = df[column]

        if series.isna().all():

            unusable_columns += 1

        elif series.nunique(
            dropna=True
        ) <= 1:

            unusable_columns += 1

        else:

            usable_columns += 1

    total_columns = len(
        df.columns
    )

    if total_columns == 0:

        usability_percentage = 0

    else:

        usability_percentage = (
            usable_columns /
            total_columns
        ) * 100

    return {
        "usable_columns": usable_columns,
        "unusable_columns": unusable_columns,
        "column_usability_percentage": round(
            usability_percentage,
            2
        )
    }


# ============================================================
# QUALITY SCORE
# ============================================================

def calculate_quality_score(
    structure,
    missing,
    duplicates,
    empty_columns,
    constant_columns,
    column_usability
):

    if structure["rows"] == 0:
        return 0.0

    if structure["columns"] == 0:
        return 0.0

    # --------------------------------------------------------
    # Missing-value score
    # --------------------------------------------------------

    missing_percentage = (
        missing["missing_percentage"]
    )

    if missing_percentage <= 1:
        missing_score = 100

    elif missing_percentage <= 5:
        missing_score = 90

    elif missing_percentage <= 10:
        missing_score = 75

    elif missing_percentage <= 25:
        missing_score = 55

    elif missing_percentage <= 50:
        missing_score = 30

    else:
        missing_score = 10

    # --------------------------------------------------------
    # Duplicate score
    # --------------------------------------------------------

    duplicate_percentage = (
        duplicates["duplicate_percentage"]
    )

    if duplicate_percentage <= 1:
        duplicate_score = 100

    elif duplicate_percentage <= 5:
        duplicate_score = 90

    elif duplicate_percentage <= 10:
        duplicate_score = 75

    elif duplicate_percentage <= 25:
        duplicate_score = 50

    else:
        duplicate_score = 20

    # --------------------------------------------------------
    # Empty-column score
    # --------------------------------------------------------

    total_columns = structure["columns"]

    empty_count = (
        empty_columns["empty_column_count"]
    )

    if total_columns == 0:

        empty_score = 0

    else:

        empty_score = (
            1 -
            (
                empty_count /
                total_columns
            )
        ) * 100

    # --------------------------------------------------------
    # Constant-column score
    # --------------------------------------------------------

    constant_count = (
        constant_columns[
            "constant_column_count"
        ]
    )

    if total_columns == 0:

        constant_score = 0

    else:

        constant_score = (
            1 -
            (
                constant_count /
                total_columns
            )
        ) * 100

    # --------------------------------------------------------
    # Column usability
    # --------------------------------------------------------

    usability_score = (
        column_usability[
            "column_usability_percentage"
        ]
    )

    # --------------------------------------------------------
    # Weighted quality score
    # --------------------------------------------------------

    score = (

        missing_score * 0.30 +

        duplicate_score * 0.20 +

        empty_score * 0.15 +

        constant_score * 0.10 +

        usability_score * 0.25

    )

    return round(
        score,
        2
    )


# ============================================================
# STATUS DETERMINATION
# ============================================================

def determine_status(
    quality_score,
    duplicate_percentage=0,
    missing_percentage=0,
    empty_column_count=0,
    constant_column_count=0
):

    # --------------------------------------------------------
    # Critical rejection rules
    # --------------------------------------------------------

    if duplicate_percentage > 25:
        return "REJECT"

    if missing_percentage > 50:
        return "REJECT"

    # --------------------------------------------------------
    # Serious issues requiring review
    # --------------------------------------------------------

    if empty_column_count > 0:
        return "REVIEW"

    if constant_column_count > 20:
        return "REVIEW"

    if duplicate_percentage > 10:
        return "REVIEW"

    if missing_percentage > 25:
        return "REVIEW"

    # --------------------------------------------------------
    # Overall quality score
    # --------------------------------------------------------

    if quality_score >= 85:
        return "PASS"

    if quality_score >= 70:
        return "REVIEW"

    return "REJECT"


# ============================================================
# COMPLETE DATASET ANALYSIS
# ============================================================

def analyze_dataset(file_path):

    file_path = Path(file_path)

    result = {
        "file": file_path.name,
        "path": str(file_path),
        "extension": file_path.suffix.lower(),
        "readable": False,
        "error": None
    }

    try:

        # ----------------------------------------------------
        # Load file
        # ----------------------------------------------------

        df = load_dataset(
            file_path
        )

        result["readable"] = True

        # ----------------------------------------------------
        # Analyze dataset
        # ----------------------------------------------------

        structure = analyze_structure(
            df
        )

        missing = analyze_missing_values(
            df
        )

        duplicates = analyze_duplicates(
            df
        )

        empty_columns = analyze_empty_columns(
            df
        )

        constant_columns = analyze_constant_columns(
            df
        )

        data_types = analyze_data_types(
            df
        )

        column_usability = analyze_column_usability(
            df
        )

        # ----------------------------------------------------
        # Calculate quality score
        # ----------------------------------------------------

        quality_score = calculate_quality_score(

            structure,

            missing,

            duplicates,

            empty_columns,

            constant_columns,

            column_usability

        )

        # ----------------------------------------------------
        # Determine status
        # ----------------------------------------------------

        status = determine_status(

            quality_score,

            duplicate_percentage=duplicates[
                "duplicate_percentage"
            ],

            missing_percentage=missing[
                "missing_percentage"
            ],

            empty_column_count=empty_columns[
                "empty_column_count"
            ],

            constant_column_count=constant_columns[
                "constant_column_count"
            ]

        )

        # ----------------------------------------------------
        # Build result
        # ----------------------------------------------------

        result.update({

            "rows":
                structure["rows"],

            "columns":
                structure["columns"],

            "column_names":
                structure["column_names"],

            "missing_cells":
                missing["missing_cells"],

            "missing_percentage":
                missing["missing_percentage"],

            "duplicate_rows":
                duplicates["duplicate_rows"],

            "duplicate_percentage":
                duplicates["duplicate_percentage"],

            "empty_columns":
                empty_columns[
                    "empty_columns"
                ],

            "empty_column_count":
                empty_columns[
                    "empty_column_count"
                ],

            "constant_columns":
                constant_columns[
                    "constant_columns"
                ],

            "constant_column_count":
                constant_columns[
                    "constant_column_count"
                ],

            "data_types":
                data_types["data_types"],

            "usable_columns":
                column_usability[
                    "usable_columns"
                ],

            "unusable_columns":
                column_usability[
                    "unusable_columns"
                ],

            "column_usability_percentage":
                column_usability[
                    "column_usability_percentage"
                ],

            "quality_score":
                quality_score,

            "status":
                status

        })

    except Exception as error:

        result["error"] = str(
            error
        )

        result["status"] = "ERROR"

    return result


# ============================================================
# SCAN COMPLETE FOLDER
# ============================================================

def scan_folder(folder):

    files = find_dataset_files(
        folder
    )

    results = []

    for file in files:

        results.append(
            analyze_dataset(
                file
            )
        )

    return results