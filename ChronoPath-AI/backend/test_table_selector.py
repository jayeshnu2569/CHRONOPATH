from pathlib import Path

from dataset_engine.kaggle_downloader import find_data_files
from dataset_engine.table_selector import (
    select_decision_tables,
    display_selection,
)

try:
    from dataset_engine.dataset_intelligence import inspect_dataset
except ImportError:
    from dataset_engine.dataset_inspector import inspect_dataset

DATASET_DIRECTORY = Path(
    "./data/kaggle_downloads/olistbr_brazilian-ecommerce"
)
DECISION = "revenue strategy"

def main():
    print()
    print("=" * 80)
    print("        CHRONOPATH AI - DECISION TABLE SELECTOR TEST")
    print("=" * 80)

    files = find_data_files(DATASET_DIRECTORY)
    print()
    print(f"Files found: {len(files)}")

    if not files:
        print("No dataset files found.")
        return

    # Critical integration:
    # inspector -> enriched structure -> selector
    inspection = inspect_dataset(files)

    result = select_decision_tables(
        inspection,
        DECISION,
    )
    display_selection(result)

if __name__ == "__main__":
    main()