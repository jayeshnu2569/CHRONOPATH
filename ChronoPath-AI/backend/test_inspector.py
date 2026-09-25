from pathlib import Path

from dataset_engine.kaggle_downloader import find_data_files
from dataset_engine.dataset_inspector import (
    inspect_dataset,
    display_inspection,
)


DATASET_DIRECTORY = Path(
    "data/kaggle_downloads/"
    "olistbr_brazilian-ecommerce"
)


print()
print("=" * 80)
print("        CHRONOPATH AI - MULTI-FILE INSPECTOR TEST")
print("=" * 80)


files = find_data_files(
    DATASET_DIRECTORY
)

print()
print(
    f"Files found: {len(files)}"
)

inspection = inspect_dataset(
    files
)

display_inspection(
    inspection
)

print()
print("=" * 80)
print("        INSPECTION COMPLETE")
print("=" * 80)