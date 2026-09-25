from __future__ import annotations

from typing import Any, Dict, List, Optional


# ============================================================
# CHRONOPATH AI
# DECISION-AWARE PRIMARY TABLE SELECTOR
# ============================================================

VERSION = "1.0.0"


# ============================================================
# DECISION PROFILES
# ============================================================

DECISION_PROFILES = {
    "customer strategy": {
        "keywords": [
            "customer",
            "user",
            "client",
            "buyer",
            "customer_id",
            "customer_unique_id",
            "city",
            "state",
            "income",
            "age",
            "satisfaction",
            "retention",
            "loyalty",
        ],
        "preferred_roles": [
            "FACT",
            "DIMENSION",
        ],
    },

    "sales planning": {
        "keywords": [
            "sales",
            "sale",
            "revenue",
            "order",
            "orders",
            "quantity",
            "price",
            "amount",
            "payment",
            "customer",
        ],
        "preferred_roles": [
            "FACT",
            "BRIDGE",
        ],
    },

    "business strategy": {
        "keywords": [
            "business",
            "revenue",
            "sales",
            "profit",
            "order",
            "customer",
            "product",
            "seller",
            "payment",
        ],
        "preferred_roles": [
            "FACT",
            "BRIDGE",
        ],
    },

    "product strategy": {
        "keywords": [
            "product",
            "product_id",
            "category",
            "price",
            "quantity",
            "sales",
            "review",
            "rating",
        ],
        "preferred_roles": [
            "FACT",
            "BRIDGE",
        ],
    },

    "revenue strategy": {
        "keywords": [
            "revenue",
            "payment",
            "price",
            "sales",
            "amount",
            "freight",
            "order",
            "quantity",
        ],
        "preferred_roles": [
            "FACT",
            "BRIDGE",
        ],
    },

    "career planning": {
        "keywords": [
            "career",
            "salary",
            "job",
            "employment",
            "placement",
            "skill",
            "education",
            "degree",
            "promotion",
        ],
        "preferred_roles": [
            "FACT",
            "BRIDGE",
        ],
    },

    "career selection": {
        "keywords": [
            "career",
            "job",
            "salary",
            "skill",
            "degree",
            "education",
            "placement",
            "employment",
        ],
        "preferred_roles": [
            "FACT",
        ],
    },

    "skill development": {
        "keywords": [
            "skill",
            "skills",
            "communication",
            "technical",
            "education",
            "training",
            "learning",
            "experience",
        ],
        "preferred_roles": [
            "FACT",
        ],
    },

    "education planning": {
        "keywords": [
            "education",
            "degree",
            "school",
            "college",
            "university",
            "gpa",
            "grade",
            "learning",
            "study",
        ],
        "preferred_roles": [
            "FACT",
        ],
    },

    "academic planning": {
        "keywords": [
            "academic",
            "gpa",
            "grade",
            "course",
            "study",
            "education",
            "student",
            "exam",
        ],
        "preferred_roles": [
            "FACT",
        ],
    },
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(value: Any) -> str:
    """
    Normalize text for keyword comparison.
    """

    if value is None:
        return ""

    return str(value).strip().lower()


def normalize_columns(columns: Any) -> List[str]:
    """
    Convert a column collection into normalized strings.
    """

    if columns is None:
        return []

    if isinstance(columns, dict):
        columns = list(columns.keys())

    try:
        return [
            normalize_text(column)
            for column in columns
            if normalize_text(column)
        ]
    except TypeError:
        return []


# ============================================================
# DECISION PROFILE
# ============================================================

def get_decision_profile(
    decision: str
) -> Dict[str, Any]:

    decision_key = normalize_text(decision)

    if decision_key in DECISION_PROFILES:
        return DECISION_PROFILES[decision_key]

    return {
        "keywords": decision_key.replace("-", " ").split(),
        "preferred_roles": [
            "FACT",
            "BRIDGE",
            "DIMENSION",
        ],
    }


# ============================================================
# COLUMN MATCHING
# ============================================================

def score_column_matches(
    columns: List[str],
    keywords: List[str]
) -> Dict[str, Any]:

    matched_columns = []
    match_score = 0

    for column in columns:

        for keyword in keywords:

            keyword = normalize_text(keyword)

            if not keyword:
                continue

            if keyword == column:
                matched_columns.append(column)
                match_score += 12
                break

            if keyword in column:
                matched_columns.append(column)
                match_score += 8
                break

            if column in keyword:
                matched_columns.append(column)
                match_score += 6
                break

    matched_columns = list(dict.fromkeys(matched_columns))

    # Prevent excessive keyword matches from dominating.
    match_score = min(match_score, 40)

    return {
        "matched_columns": matched_columns,
        "match_score": match_score,
    }


# ============================================================
# ROLE SCORE
# ============================================================

def score_role(
    role: str,
    preferred_roles: List[str]
) -> int:

    role = normalize_text(role).upper()

    preferred_roles = [
        normalize_text(value).upper()
        for value in preferred_roles
    ]

    if role in preferred_roles:

        if role == "FACT":
            return 15

        if role == "BRIDGE":
            return 12

        if role == "DIMENSION":
            return 8

        return 5

    if role == "FACT":
        return 5

    if role == "BRIDGE":
        return 4

    if role == "DIMENSION":
        return 3

    if role == "SUPPORTING":
        return 1

    if role == "REFERENCE":
        return 0

    return 0


# ============================================================
# RELATIONSHIP SCORE
# ============================================================

def score_relationships(
    relationship_count: Any,
    connected_files: Any
) -> int:

    try:
        relationships = int(relationship_count or 0)
    except (TypeError, ValueError):
        relationships = 0

    try:
        connected = int(connected_files or 0)
    except (TypeError, ValueError):
        connected = 0

    score = 0

    if relationships >= 1:
        score += 5

    if relationships >= 3:
        score += 5

    if relationships >= 5:
        score += 5

    if connected >= 1:
        score += 3

    if connected >= 3:
        score += 2

    return min(score, 20)


# ============================================================
# INTELLIGENCE SCORE
# ============================================================

def get_intelligence_score(
    file_info: Dict[str, Any]
) -> float:

    value = (
        file_info.get("intelligence_score")
        if "intelligence_score" in file_info
        else file_info.get("score", 0)
    )

    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


# ============================================================
# TABLE SCORING
# ============================================================

def score_table(
    file_info: Dict[str, Any],
    decision: str
) -> Dict[str, Any]:

    profile = get_decision_profile(decision)

    columns = normalize_columns(
        file_info.get("columns", [])
    )

    keywords = profile["keywords"]

    column_result = score_column_matches(
        columns,
        keywords
    )

    role = file_info.get(
        "role",
        file_info.get("dataset_role", "UNKNOWN")
    )

    role_score = score_role(
        role,
        profile["preferred_roles"]
    )

    relationship_score = score_relationships(
        file_info.get("relationships", 0),
        file_info.get("connected_files", 0)
    )

    intelligence_score = get_intelligence_score(
        file_info
    )

    # Normalize intelligence score to 0-20.
    intelligence_component = min(
        intelligence_score * 0.20,
        20
    )

    # Final score:
    #
    # Decision-column relevance = 40
    # Role relevance            = 15
    # Relationship strength     = 20
    # Existing intelligence     = 20
    # Small structural bonus    = 5
    #

    structural_bonus = 0

    row_count = file_info.get(
        "rows",
        file_info.get("row_count", 0)
    )

    try:
        row_count = int(row_count or 0)
    except (TypeError, ValueError):
        row_count = 0

    if row_count >= 1000:
        structural_bonus += 2

    if len(columns) >= 3:
        structural_bonus += 2

    if file_info.get("unique_ids"):
        structural_bonus += 1

    final_score = (
        column_result["match_score"]
        + role_score
        + relationship_score
        + intelligence_component
        + structural_bonus
    )

    final_score = min(
        round(final_score, 2),
        100
    )

    return {
        "file": file_info.get(
            "file",
            file_info.get(
                "filename",
                file_info.get("name", "Unknown")
            )
        ),

        "role": role,

        "score": final_score,

        "matched_columns": column_result[
            "matched_columns"
        ],

        "column_score": column_result[
            "match_score"
        ],

        "role_score": role_score,

        "relationship_score": relationship_score,

        "intelligence_component": round(
            intelligence_component,
            2
        ),

        "structural_bonus": structural_bonus,

        "intelligence_score": intelligence_score,

        "relationships": file_info.get(
            "relationships",
            0
        ),

        "connected_files": file_info.get(
            "connected_files",
            0
        ),
    }


# ============================================================
# RANK TABLES
# ============================================================

def rank_tables(
    files: List[Dict[str, Any]],
    decision: str
) -> List[Dict[str, Any]]:

    results = []

    for file_info in files:

        result = score_table(
            file_info,
            decision
        )

        results.append(result)

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results


# ============================================================
# PRIMARY TABLE SELECTION
# ============================================================

def select_primary_table(
    files: List[Dict[str, Any]],
    decision: str
) -> Dict[str, Any]:

    if not files:

        return {
            "decision": decision,
            "primary_table": None,
            "supporting_tables": [],
            "rankings": [],
            "confidence": 0,
            "reason": "No files available.",
        }

    rankings = rank_tables(
        files,
        decision
    )

    primary = rankings[0]

    supporting = rankings[1:]

    if len(rankings) == 1:

        confidence = 100

    else:

        difference = (
            primary["score"]
            - rankings[1]["score"]
        )

        confidence = min(
            100,
            round(
                60 + difference * 4,
                2
            )
        )

    reason_parts = []

    if primary["matched_columns"]:

        reason_parts.append(
            "contains decision-relevant "
            "columns: "
            + ", ".join(
                primary["matched_columns"]
            )
        )

    if primary["role"]:

        reason_parts.append(
            f"has role {primary['role']}"
        )

    if primary["relationships"]:

        reason_parts.append(
            f"has {primary['relationships']} "
            "detected relationships"
        )

    if not reason_parts:

        reason_parts.append(
            "highest decision-aware score"
        )

    reason = "; ".join(
        reason_parts
    ) + "."

    return {
        "decision": decision,

        "primary_table": primary["file"],

        "primary_role": primary["role"],

        "primary_score": primary["score"],

        "supporting_tables": [
            {
                "file": item["file"],
                "role": item["role"],
                "score": item["score"],
            }
            for item in supporting
        ],

        "rankings": rankings,

        "confidence": confidence,

        "reason": reason,
    }


# ============================================================
# DISPLAY
# ============================================================

def display_selection(
    result: Dict[str, Any]
) -> None:

    print()
    print("=" * 80)
    print(
        "        CHRONOPATH AI - "
        "DECISION-AWARE TABLE SELECTION"
    )
    print("=" * 80)

    print()

    print(
        f"Decision: {result['decision']}"
    )

    print()
    print("-" * 80)

    print("PRIMARY TABLE")
    print("-" * 80)

    print(
        f"File:       {result['primary_table']}"
    )

    print(
        f"Role:       {result['primary_role']}"
    )

    print(
        f"Score:      "
        f"{result['primary_score']}/100"
    )

    print(
        f"Confidence: "
        f"{result['confidence']}%"
    )

    print(
        f"Reason:     "
        f"{result['reason']}"
    )

    print()
    print("-" * 80)

    print("TABLE RANKING")
    print("-" * 80)

    for index, item in enumerate(
        result["rankings"],
        start=1
    ):

        print(
            f"{index}. "
            f"{item['file']}"
        )

        print(
            f"   Role: {item['role']}"
        )

        print(
            f"   Score: "
            f"{item['score']}/100"
        )

        if item["matched_columns"]:

            print(
                "   Decision columns: "
                + ", ".join(
                    item["matched_columns"]
                )
            )

        print(
            f"   Relationships: "
            f"{item['relationships']}"
        )

        print()

    print("-" * 80)

    print("SUPPORTING TABLES")

    for item in result[
        "supporting_tables"
    ]:

        print(
            f"  - {item['file']} "
            f"({item['role']}, "
            f"{item['score']}/100)"
        )

    print()

    print("=" * 80)
    print(
        "        TABLE SELECTION COMPLETE"
    )
    print("=" * 80)