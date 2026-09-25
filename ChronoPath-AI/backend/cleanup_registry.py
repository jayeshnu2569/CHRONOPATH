from dataset_engine.registry.dataset_registry import (
    read_registry,
    write_registry
)


print()
print("=" * 80)
print("        CHRONOPATH AI - REGISTRY CLEANUP")
print("=" * 80)
print()


records = read_registry()


# ============================================================
# DEDUPLICATE BY KAGGLE REFERENCE
# ============================================================

unique = {}


for record in records:

    reference = record.get(
        "kaggle_reference",
        ""
    ).strip()


    # --------------------------------------------------------
    # If Kaggle reference exists, use it as identity
    # --------------------------------------------------------

    if reference:

        key = (
            "kaggle",
            reference
        )

    else:

        # ----------------------------------------------------
        # Legacy/manual datasets
        # ----------------------------------------------------

        key = (
            "manual",
            record.get(
                "dataset_name",
                ""
            ).strip()
        )


    # Later records replace older records.
    unique[key] = record


cleaned_records = list(
    unique.values()
)


write_registry(
    cleaned_records
)


print(
    f"Original records: "
    f"{len(records)}"
)

print(
    f"Clean records:    "
    f"{len(cleaned_records)}"
)

print(
    f"Removed:          "
    f"{len(records) - len(cleaned_records)}"
)

print()

print(
    "Registry cleanup complete."
)

print("=" * 80)