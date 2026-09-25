from pathlib import Path
import subprocess
import zipfile
import shutil


# ============================================================
# CHRONOPATH AI
# KAGGLE DATASET DOWNLOADER
# ============================================================

DOWNLOAD_ROOT = Path("./data/kaggle_downloads")


# ============================================================
# CREATE DIRECTORY
# ============================================================

def create_download_directory(
    kaggle_reference
):

    safe_name = (
        kaggle_reference
        .replace("/", "_")
        .replace("\\", "_")
    )

    directory = (
        DOWNLOAD_ROOT / safe_name
    )

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return directory


# ============================================================
# DOWNLOAD DATASET
# ============================================================

def download_dataset(
    kaggle_reference
):

    output_directory = (
        create_download_directory(
            kaggle_reference
        )
    )

    print()
    print("=" * 80)

    print(
        "CHRONOPATH AI - KAGGLE DOWNLOAD"
    )

    print("=" * 80)

    print(
        f"Dataset: {kaggle_reference}"
    )

    print(
        f"Location: {output_directory}"
    )

    print()

    command = [

        "kaggle",

        "datasets",

        "download",

        "-d",

        kaggle_reference,

        "-p",

        str(output_directory)

    ]

    try:

        result = subprocess.run(

            command,

            capture_output=True,

            text=True,

            encoding="utf-8",

            errors="replace"

        )

    except FileNotFoundError:

        raise RuntimeError(
            "Kaggle CLI was not found. "
            "Run 'kaggle --version' first."
        )

    if result.returncode != 0:

        raise RuntimeError(
            "Kaggle download failed:\n"
            + result.stderr
        )

    print(
        result.stdout
    )

    return output_directory


# ============================================================
# EXTRACT ZIP FILES
# ============================================================

def extract_archives(
    directory
):

    extracted_files = []

    for zip_file in directory.glob(
        "*.zip"
    ):

        print(
            f"Extracting: {zip_file.name}"
        )

        try:

            with zipfile.ZipFile(
                zip_file,
                "r"
            ) as archive:

                archive.extractall(
                    directory
                )

                extracted_files.extend(
                    archive.namelist()
                )

        except zipfile.BadZipFile:

            print(
                f"WARNING: Invalid ZIP: "
                f"{zip_file.name}"
            )

    return extracted_files


# ============================================================
# FIND DATA FILES
# ============================================================

def find_data_files(
    directory
):

    extensions = {

        ".csv",
        ".json",
        ".parquet",
        ".xlsx",
        ".xls"

    }

    files = []

    for path in directory.rglob("*"):

        if (

            path.is_file()

            and

            path.suffix.lower()
            in extensions

        ):

            files.append(path)

    return files


# ============================================================
# DOWNLOAD + EXTRACT + FIND
# ============================================================

def fetch_dataset(
    kaggle_reference
):

    directory = download_dataset(
        kaggle_reference
    )

    extract_archives(
        directory
    )

    data_files = find_data_files(
        directory
    )

    print()

    print(
        f"Found {len(data_files)} "
        f"data file(s)."
    )

    for file in data_files:

        print(
            f"  - {file}"
        )

    return {

        "kaggle_reference":
            kaggle_reference,

        "directory":
            str(directory),

        "files":
            [
                str(file)
                for file in data_files
            ]

    }