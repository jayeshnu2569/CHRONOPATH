from pathlib import Path
import hashlib
import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
    ".parquet"
}


def calculate_hash(file_path, chunk_size=1024 * 1024):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_file(file_path):

    path = Path(file_path)

    result = {
        "filename": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "sha256": calculate_hash(path),
        "supported": path.suffix.lower()
        in SUPPORTED_EXTENSIONS
    }

    if not result["supported"]:
        result["status"] = "REJECTED"
        result["reason"] = "Unsupported file format"

        return result

    try:

        if path.suffix.lower() == ".csv":
            df = pd.read_csv(path)

        elif path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(path)

        elif path.suffix.lower() == ".json":
            df = pd.read_json(path)

        elif path.suffix.lower() == ".parquet":
            df = pd.read_parquet(path)

        result["rows"] = len(df)

        result["columns_count"] = len(df.columns)

        result["columns"] = [
            str(column)
            for column in df.columns
        ]

        result["duplicate_rows"] = int(
            df.duplicated().sum()
        )

        if len(df) > 0:
            result["duplicate_percentage"] = round(
                df.duplicated().mean() * 100,
                2
            )
        else:
            result["duplicate_percentage"] = 100

        result["missing_percentage"] = round(
            df.isnull().mean().mean() * 100,
            2
        )

        result["dtypes"] = {
            str(column): str(dtype)
            for column, dtype
            in df.dtypes.items()
        }

        result["status"] = "SCANNED"

        return result

    except Exception as error:

        return {
            **result,
            "status": "REJECTED",
            "reason": f"Unable to read dataset: {error}"
        }


def scan_directory(directory):

    directory = Path(directory)

    results = []

    for file_path in directory.rglob("*"):

        if file_path.is_file():

            results.append(
                scan_file(file_path)
            )

    return results