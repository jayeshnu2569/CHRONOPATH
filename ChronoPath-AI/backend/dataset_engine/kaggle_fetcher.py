from pathlib import Path
from datetime import datetime, timezone

from kaggle.api.kaggle_api_extended import KaggleApi


# ============================================================
# CHRONOPATH AI
# KAGGLE DATASET ACQUISITION ENGINE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_DIR = BASE_DIR / "kaggle_temp"

TEMP_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# KAGGLE CONNECTION
# ============================================================

def get_kaggle_api():

    api = KaggleApi()

    api.authenticate()

    return api


# ============================================================
# SEARCH KAGGLE DATASETS
# ============================================================

def search_kaggle(
    keyword,
    limit=20
):

    api = get_kaggle_api()

    datasets = api.dataset_list(
        search=keyword
    )

    return datasets[:limit]


# ============================================================
# GET DATASET METADATA
# ============================================================

    api = get_kaggle_api()

    dataset = api.dataset_view(
        dataset_ref
    )

    title = getattr(
        dataset,
        "title",
        ""
    )

    description = getattr(
        dataset,
        "description",
        ""
    )

    downloads = getattr(
        dataset,
        "download_count",
        0
    )

    votes = getattr(
        dataset,
        "vote_count",
        0
    )

    usability = getattr(
        dataset,
        "usability_rating",
        0
    )

    # --------------------------------------------------------
    # Normalize usability
    # Kaggle normally returns 0-1.
    # ChronoPath uses 0-100.
    # --------------------------------------------------------

    try:

        usability = float(
            usability
        )

    except (
        TypeError,
        ValueError
    ):

        usability = 0

    if usability <= 1:

        usability *= 100

    usability = max(
        0,
        min(
            usability,
            100
        )
    )

    # --------------------------------------------------------
    # Popularity
    # --------------------------------------------------------

    try:

        downloads = float(
            downloads
        )

    except (
        TypeError,
        ValueError
    ):

        downloads = 0

    try:

        votes = float(
            votes
        )

    except (
        TypeError,
        ValueError
    ):

        votes = 0

    # Log scaling prevents huge Kaggle datasets
    # from completely dominating the score.

    import math

    download_score = (
        min(
            math.log10(
                downloads + 1
            ) / 7 * 100,
            100
        )
    )

    vote_score = (
        min(
            math.log10(
                votes + 1
            ) / 4 * 100,
            100
        )
    )

    popularity_score = (
        download_score * 0.65
        +
        vote_score * 0.35
    )

    # --------------------------------------------------------
    # Freshness
    # --------------------------------------------------------

    freshness_score = 50

    last_updated = getattr(
        dataset,
        "last_updated",
        None
    )

    if last_updated is None:

        last_updated = getattr(
            dataset,
            "lastUpdated",
            None
        )

    if last_updated:

        try:

            if isinstance(
                last_updated,
                str
            ):

                updated = datetime.fromisoformat(
                    last_updated.replace(
                        "Z",
                        "+00:00"
                    )
                )

            else:

                updated = last_updated

            if updated.tzinfo is None:

                updated = updated.replace(
                    tzinfo=timezone.utc
                )

            now = datetime.now(
                timezone.utc
            )

            age_days = (
                now - updated
            ).days

            if age_days <= 90:

                freshness_score = 100

            elif age_days <= 365:

                freshness_score = 80

            elif age_days <= 730:

                freshness_score = 60

            elif age_days <= 1825:

                freshness_score = 40

            else:

                freshness_score = 20

        except Exception:

            freshness_score = 50

    # --------------------------------------------------------
    # Relevance
    # --------------------------------------------------------

    relevance_score = 50

    if category:

        category_text = str(
            category
        ).lower()

        searchable_text = (
            str(title)
            + " "
            + str(description)
        ).lower()

        category_words = [
            word.strip()
            for word in category_text.split()
            if len(word.strip()) >= 3
        ]

        if category_words:

            matches = sum(
                1
                for word in category_words
                if word in searchable_text
            )

            if matches >= 2:

                relevance_score = 100

            elif matches == 1:

                relevance_score = 75

            else:

                relevance_score = 40

    # --------------------------------------------------------
    # Decision value
    # --------------------------------------------------------

    decision_value = (
        relevance_score * 0.50
        +
        usability * 0.30
        +
        popularity_score * 0.20
    )

    decision_value = round(
        decision_value,
        2
    )

    # --------------------------------------------------------
    # Metadata score
    # --------------------------------------------------------

    metadata_score = (

        relevance_score * 0.25

        +

        popularity_score * 0.20

        +

        usability * 0.25

        +

        freshness_score * 0.15

        +

        decision_value * 0.15

    )

    metadata_score = round(
        max(
            0,
            min(
                metadata_score,
                100
            )
        ),
        2
    )

    return {

        "title": title,

        "description": description,

        "reference": dataset_ref,

        "downloads": downloads,

        "votes": votes,

        "usability": round(
            usability,
            2
        ),

        "popularity": round(
            popularity_score,
            2
        ),

        "freshness": round(
            freshness_score,
            2
        ),

        "relevance": round(
            relevance_score,
            2
        ),

        "decision_value": decision_value,

        "metadata_score": metadata_score
    }


# ============================================================
# GET DATASET METADATA
# ============================================================

def get_dataset_metadata(
    dataset_ref,
    category=None
):

    """
    Retrieve Kaggle metadata using dataset_list().

    This version is compatible with the Kaggle API
    available in the current ChronoPath environment.
    """

    import math

    api = get_kaggle_api()

    # --------------------------------------------------------
    # Extract owner and dataset name
    # --------------------------------------------------------

    if "/" in dataset_ref:

        owner, dataset_name = (
            dataset_ref.split(
                "/",
                1
            )
        )

    else:

        owner = ""

        dataset_name = dataset_ref

    # --------------------------------------------------------
    # Search Kaggle for the exact dataset
    # --------------------------------------------------------

    datasets = api.dataset_list(
        search=dataset_name
    )

    dataset = None

    for item in datasets:

        ref = getattr(
            item,
            "ref",
            ""
        )

        if ref.lower() == dataset_ref.lower():

            dataset = item

            break

    # --------------------------------------------------------
    # If exact match isn't found, use first result
    # --------------------------------------------------------

    if dataset is None:

        if not datasets:

            raise RuntimeError(
                f"Kaggle dataset not found: {dataset_ref}"
            )

        dataset = datasets[0]

    # --------------------------------------------------------
    # Basic metadata
    # --------------------------------------------------------

    title = getattr(
        dataset,
        "title",
        dataset_name
    )

    description = getattr(
        dataset,
        "description",
        ""
    )

    downloads = getattr(
        dataset,
        "download_count",
        0
    )

    votes = getattr(
        dataset,
        "vote_count",
        0
    )

    usability = getattr(
        dataset,
        "usability_rating",
        0
    )

    # --------------------------------------------------------
    # Normalize values
    # --------------------------------------------------------

    try:

        downloads = float(
            downloads
        )

    except (
        TypeError,
        ValueError
    ):

        downloads = 0

    try:

        votes = float(
            votes
        )

    except (
        TypeError,
        ValueError
    ):

        votes = 0

    try:

        usability = float(
            usability
        )

    except (
        TypeError,
        ValueError
    ):

        usability = 0

    # Kaggle normally reports usability between 0 and 1.

    if usability <= 1:

        usability *= 100

    usability = max(
        0,
        min(
            usability,
            100
        )
    )

    # --------------------------------------------------------
    # POPULARITY SCORE
    # --------------------------------------------------------

    download_score = min(
        (
            math.log10(
                downloads + 1
            )
            / 7
        )
        * 100,
        100
    )

    vote_score = min(
        (
            math.log10(
                votes + 1
            )
            / 4
        )
        * 100,
        100
    )

    popularity_score = (
        download_score * 0.65
        +
        vote_score * 0.35
    )

    # --------------------------------------------------------
    # FRESHNESS
    #
    # dataset_list() may expose lastUpdated depending
    # on the installed Kaggle API version.
    # --------------------------------------------------------

    freshness_score = 50

    last_updated = getattr(
        dataset,
        "lastUpdated",
        None
    )

    if last_updated is None:

        last_updated = getattr(
            dataset,
            "last_updated",
            None
        )

    if last_updated:

        try:

            from datetime import datetime, timezone

            if isinstance(
                last_updated,
                str
            ):

                updated = datetime.fromisoformat(
                    last_updated.replace(
                        "Z",
                        "+00:00"
                    )
                )

            else:

                updated = last_updated

            if updated.tzinfo is None:

                updated = updated.replace(
                    tzinfo=timezone.utc
                )

            now = datetime.now(
                timezone.utc
            )

            age_days = (
                now - updated
            ).days

            if age_days <= 90:

                freshness_score = 100

            elif age_days <= 365:

                freshness_score = 80

            elif age_days <= 730:

                freshness_score = 60

            elif age_days <= 1825:

                freshness_score = 40

            else:

                freshness_score = 20

        except Exception:

            freshness_score = 50

    # --------------------------------------------------------
    # RELEVANCE
    # --------------------------------------------------------

    relevance_score = 50

    if category:

        category_text = str(
            category
        ).lower()

        searchable_text = (
            str(title)
            + " "
            + str(description)
        ).lower()

        category_words = [

            word.strip()

            for word in category_text.split()

            if len(
                word.strip()
            ) >= 3

        ]

        if category_words:

            matches = sum(

                1

                for word in category_words

                if word in searchable_text

            )

            if matches >= 2:

                relevance_score = 100

            elif matches == 1:

                relevance_score = 75

            else:

                relevance_score = 40

    # --------------------------------------------------------
    # DECISION VALUE
    # --------------------------------------------------------

    decision_value = (

        relevance_score * 0.50

        +

        usability * 0.30

        +

        popularity_score * 0.20

    )

    decision_value = round(
        decision_value,
        2
    )

    # --------------------------------------------------------
    # METADATA SCORE
    # --------------------------------------------------------

    metadata_score = (

        relevance_score * 0.25

        +

        popularity_score * 0.20

        +

        usability * 0.25

        +

        freshness_score * 0.15

        +

        decision_value * 0.15

    )

    metadata_score = round(
        max(
            0,
            min(
                metadata_score,
                100
            )
        ),
        2
    )

    # --------------------------------------------------------
    # RETURN CHRONOPATH METADATA OBJECT
    # --------------------------------------------------------

    return {

        "title": title,

        "description": description,

        "reference": dataset_ref,

        "downloads": downloads,

        "votes": votes,

        "usability": round(
            usability,
            2
        ),

        "popularity": round(
            popularity_score,
            2
        ),

        "freshness": round(
            freshness_score,
            2
        ),

        "relevance": round(
            relevance_score,
            2
        ),

        "decision_value": decision_value,

        "metadata_score": metadata_score

    }