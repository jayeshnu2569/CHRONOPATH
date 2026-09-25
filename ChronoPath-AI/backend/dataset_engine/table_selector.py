from pathlib import Path
import re


# ============================================================
# CHRONOPATH AI
# DECISION-AWARE TABLE SELECTOR
# ============================================================


ROLE_WEIGHTS = {
    "FACT": 16,
    "BRIDGE": 11,
    "DIMENSION": 5,
    "REFERENCE": 1,
    "SUPPORTING": 3,
    "UNKNOWN": -10,
}


# Decision-specific signals.
# These are intentionally stronger than relationship count.
DECISION_KEYWORDS = {

    "revenue strategy": {
        "payment": 35,
        "revenue": 35,
        "amount": 32,
        "price": 30,
        "sales": 30,
        "value": 28,
        "freight": 18,
        "quantity": 18,
        "order": 12,
    },

    "sales planning": {
        "sales": 35,
        "revenue": 35,
        "payment": 30,
        "amount": 30,
        "price": 28,
        "value": 25,
        "order": 20,
        "quantity": 20,
        "product": 15,
    },

    "customer strategy": {
        "customer": 35,
        "review": 25,
        "satisfaction": 25,
        "city": 12,
        "state": 12,
        "order": 15,
    },

    "product strategy": {
        "product": 35,
        "price": 30,
        "category": 28,
        "quantity": 22,
        "sales": 20,
        "review": 15,
    },

    "business strategy": {
        "revenue": 30,
        "sales": 30,
        "customer": 25,
        "product": 25,
        "order": 22,
        "payment": 22,
    },

    "career planning": {
        "career": 35,
        "salary": 32,
        "job": 30,
        "employment": 28,
        "skill": 25,
        "promotion": 25,
    },

    "education planning": {
        "education": 35,
        "gpa": 30,
        "grade": 28,
        "student": 25,
        "course": 25,
        "degree": 22,
        "skill": 20,
    },

    "academic planning": {
        "academic": 35,
        "gpa": 30,
        "grade": 28,
        "student": 25,
        "course": 25,
        "degree": 22,
    },

    "study strategy": {
        "study": 35,
        "student": 28,
        "course": 25,
        "grade": 25,
        "gpa": 25,
        "skill": 20,
    },
}


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def _normalise(value):
    return re.sub(
        r"[^a-z0-9]+",
        " ",
        str(value).lower()
    ).strip()


def _name(item):
    return str(
        item.get("name")
        or Path(
            str(item.get("file", ""))
        ).name
    )


def _columns(item):
    """
    Inspector-compatible column extraction.

    dataset_inspector.py may expose columns under
    different keys depending on the inspection stage.
    """

    possible_keys = (
        "column_names",
        "columns_names",
        "columns_list",
        "column_names_detected",
        "columns",
    )

    for key in possible_keys:

        value = item.get(key)

        if isinstance(value, (list, tuple)):
            return [
                str(column)
                for column in value
            ]

    return []


# ============================================================
# ROLE PROPAGATION
# ============================================================

def _get_role(item):
    """
    Read the role produced by dataset_inspector.py.

    The inspector's canonical field is `table_role`; older selector/test
    versions may still provide `role`, `dataset_role`, or `file_role`.
    """
    role = (
        item.get("table_role")
        or item.get("role")
        or item.get("dataset_role")
        or item.get("file_role")
    )

    if role is None:
        return "UNKNOWN"

    role = str(role).strip().upper()

    valid_roles = {
        "FACT",
        "BRIDGE",
        "DIMENSION",
        "REFERENCE",
        "SUPPORTING",
        "UNKNOWN",
    }

    return role if role in valid_roles else "UNKNOWN"


# ============================================================
# RELATIONSHIP HANDLING
# ============================================================

def _relationship_counts(files, relationships):
    """
    Count direct relationships for every inspected file.

    Supports the relationship schemas used by the inspector and keeps
    relationship count as supporting evidence rather than the main selector.
    """
    counts = {_name(item): 0 for item in files}

    for rel in relationships or []:
        if not isinstance(rel, dict):
            continue

        candidates = [
            (rel.get("file_a"), rel.get("file_b")),
            (rel.get("source"), rel.get("target")),
            (rel.get("left"), rel.get("right")),
            (rel.get("file1"), rel.get("file2")),
        ]

        pair = next(
            (
                (left, right)
                for left, right in candidates
                if left is not None or right is not None
            ),
            None,
        )

        if pair is None:
            continue

        left, right = pair

        left_name = Path(str(left)).name if left is not None else None
        right_name = Path(str(right)).name if right is not None else None

        if left_name in counts:
            counts[left_name] += 1

        if right_name in counts:
            counts[right_name] += 1

    return counts


# ============================================================
# DECISION PROFILES
# ============================================================

# The selector now distinguishes between:
#   1. exact decision signals,
#   2. related/secondary signals,
#   3. analytical grain,
#   4. preferred table roles.
#
# This prevents "many relationships" from overpowering a table that
# contains the actual variables needed for the requested decision.

DECISION_PROFILES = {
    "revenue strategy": {
        "exact": {
            "payment_value": 1.00,
            "revenue": 1.00,
            "sales": 0.95,
            "price": 0.95,
            "freight_value": 0.75,
            "amount": 0.85,
            "value": 0.80,
            "quantity": 0.65,
        },
        "related": {
            "payment": 0.55,
            "order": 0.35,
            "product": 0.25,
        },
        "preferred_roles": {
            "FACT": 1.00,
            "BRIDGE": 0.88,
            "DIMENSION": 0.45,
            "SUPPORTING": 0.30,
            "REFERENCE": 0.10,
        },
        "grain": {
            "payment": 15,
            "order_item": 14,
            "order": 11,
            "product": 7,
            "customer": 4,
        },
    },

    "sales planning": {
        "exact": {
            "sales": 1.00,
            "revenue": 1.00,
            "price": 0.95,
            "quantity": 0.95,
            "payment_value": 0.85,
            "amount": 0.85,
            "value": 0.75,
        },
        "related": {
            "order": 0.65,
            "product": 0.55,
            "freight_value": 0.45,
        },
        "preferred_roles": {
            "FACT": 1.00,
            "BRIDGE": 0.95,
            "DIMENSION": 0.45,
            "SUPPORTING": 0.30,
            "REFERENCE": 0.10,
        },
        "grain": {
            "order_item": 15,
            "order": 13,
            "payment": 11,
            "product": 9,
            "customer": 4,
        },
    },

    "customer strategy": {
        "exact": {
            "customer": 1.00,
            "customer_unique_id": 1.00,
            "review_score": 0.95,
            "satisfaction": 0.95,
            "city": 0.65,
            "state": 0.65,
        },
        "related": {
            "review": 0.75,
            "order": 0.50,
            "zip": 0.35,
        },
        "preferred_roles": {
            "FACT": 0.90,
            "DIMENSION": 1.00,
            "BRIDGE": 0.70,
            "SUPPORTING": 0.45,
            "REFERENCE": 0.15,
        },
        "grain": {
            "customer": 15,
            "order": 11,
            "review": 11,
            "order_item": 7,
            "seller": 4,
        },
    },

    "product strategy": {
        "exact": {
            "product": 1.00,
            "product_id": 1.00,
            "price": 0.95,
            "category": 0.90,
            "quantity": 0.85,
            "sales": 0.75,
        },
        "related": {
            "review": 0.55,
            "order": 0.45,
            "freight_value": 0.35,
        },
        "preferred_roles": {
            "FACT": 0.95,
            "BRIDGE": 1.00,
            "DIMENSION": 0.90,
            "SUPPORTING": 0.40,
            "REFERENCE": 0.25,
        },
        "grain": {
            "product": 15,
            "order_item": 15,
            "order": 8,
            "review": 8,
            "customer": 3,
        },
    },

    "business strategy": {
        "exact": {
            "revenue": 1.00,
            "sales": 0.95,
            "customer": 0.90,
            "product": 0.90,
            "order": 0.80,
            "payment": 0.75,
            "price": 0.70,
        },
        "related": {
            "quantity": 0.55,
            "review": 0.45,
            "value": 0.45,
        },
        "preferred_roles": {
            "FACT": 1.00,
            "BRIDGE": 0.90,
            "DIMENSION": 0.70,
            "SUPPORTING": 0.40,
            "REFERENCE": 0.15,
        },
        "grain": {
            "order": 15,
            "order_item": 14,
            "payment": 12,
            "customer": 10,
            "product": 10,
        },
    },

    "career planning": {
        "exact": {
            "salary": 1.00,
            "career": 1.00,
            "job": 0.95,
            "employment": 0.90,
            "skill": 0.85,
            "promotion": 0.85,
        },
        "related": {
            "student": 0.55,
            "education": 0.50,
            "degree": 0.45,
            "gpa": 0.35,
        },
        "preferred_roles": {
            "FACT": 1.00,
            "BRIDGE": 0.60,
            "DIMENSION": 0.70,
            "SUPPORTING": 0.30,
            "REFERENCE": 0.10,
        },
        "grain": {
            "student": 15,
            "career": 15,
            "job": 14,
            "education": 10,
        },
    },

    "education planning": {
        "exact": {
            "education": 1.00,
            "gpa": 0.95,
            "grade": 0.95,
            "student": 0.85,
            "course": 0.85,
            "degree": 0.80,
            "skill": 0.65,
        },
        "related": {
            "career": 0.45,
            "salary": 0.25,
            "job": 0.25,
        },
        "preferred_roles": {
            "FACT": 1.00,
            "DIMENSION": 0.80,
            "BRIDGE": 0.60,
            "SUPPORTING": 0.30,
            "REFERENCE": 0.10,
        },
        "grain": {
            "student": 15,
            "education": 15,
            "course": 14,
            "career": 8,
        },
    },

    "academic planning": {
        "exact": {
            "academic": 1.00,
            "gpa": 0.95,
            "grade": 0.95,
            "student": 0.85,
            "course": 0.85,
            "degree": 0.75,
        },
        "related": {
            "skill": 0.55,
            "education": 0.55,
        },
        "preferred_roles": {
            "FACT": 1.00,
            "DIMENSION": 0.80,
            "BRIDGE": 0.55,
            "SUPPORTING": 0.30,
            "REFERENCE": 0.10,
        },
        "grain": {
            "student": 15,
            "academic": 15,
            "course": 14,
            "education": 12,
        },
    },

    "study strategy": {
        "exact": {
            "study": 1.00,
            "student": 0.90,
            "course": 0.90,
            "grade": 0.85,
            "gpa": 0.80,
            "skill": 0.70,
        },
        "related": {
            "education": 0.60,
            "degree": 0.45,
        },
        "preferred_roles": {
            "FACT": 1.00,
            "DIMENSION": 0.75,
            "BRIDGE": 0.55,
            "SUPPORTING": 0.30,
            "REFERENCE": 0.10,
        },
        "grain": {
            "student": 15,
            "course": 15,
            "study": 15,
            "education": 10,
        },
    },
}


# ============================================================
# DECISION ALIGNMENT
# ============================================================

def _column_tokens(column):
    return set(_normalise(column).split())


def _column_matches_signal(column, signal):
    """
    Match a signal against an actual column name.

    Exact normalized column matches receive the strongest evidence.
    Token overlap is allowed for practical schemas such as:
        payment_value -> payment + value
        customer_unique_id -> customer + unique + id
    """
    column_norm = _normalise(column)
    signal_norm = _normalise(signal)

    if not column_norm or not signal_norm:
        return False, 0.0

    if column_norm == signal_norm:
        return True, 1.0

    column_tokens = _column_tokens(column)
    signal_tokens = _column_tokens(signal)

    if signal_tokens.issubset(column_tokens):
        return True, 0.90

    if column_tokens & signal_tokens:
        return True, 0.45

    return False, 0.0


def _decision_profile(decision):
    decision_key = _normalise(decision)

    if decision_key in DECISION_PROFILES:
        return DECISION_PROFILES[decision_key]

    # Generic fallback for unsupported decisions.
    words = [w for w in decision_key.split() if len(w) > 2]

    return {
        "exact": {word: 1.0 for word in words},
        "related": {},
        "preferred_roles": {
            "FACT": 1.0,
            "BRIDGE": 0.85,
            "DIMENSION": 0.65,
            "SUPPORTING": 0.35,
            "REFERENCE": 0.10,
        },
        "grain": {},
    }


def _keyword_score(item, decision):
    """
    Return decision alignment on a strict 0-45 scale.

    Unlike the old implementation, this is primarily column-based.
    Filename matches provide only a small fallback signal.
    """
    profile = _decision_profile(decision)
    columns = _columns(item)

    # If the inspector did not expose columns, fall back to filename.
    searchable = columns or [_name(item)]

    exact_total = 0.0
    related_total = 0.0
    matched = []

    for signal, strength in profile["exact"].items():
        best = 0.0

        for column in searchable:
            matched_signal, quality = _column_matches_signal(
                column,
                signal,
            )
            if matched_signal:
                best = max(best, quality)

        if best > 0:
            exact_total += strength * best
            matched.append(signal)

    for signal, strength in profile["related"].items():
        best = 0.0

        for column in searchable:
            matched_signal, quality = _column_matches_signal(
                column,
                signal,
            )
            if matched_signal:
                best = max(best, quality)

        if best > 0:
            related_total += strength * best
            if signal not in matched:
                matched.append(signal)

    # Exact decision variables are deliberately dominant.
    # Related variables can contribute, but cannot overwhelm exact signals.
    raw = exact_total * 38.0 + related_total * 7.0

    return min(45.0, raw), matched
def _signal_analysis(item, decision):
    """
    Separate decision signals into direct and indirect signals.
    """

    columns = _columns(item)

    normalized_columns = {
        str(c).lower().strip().replace(" ", "_")
        for c in columns
    }

    decision_key = _normalise(decision)

    DIRECT_SIGNALS = {
        "revenue strategy": {
            "revenue", "payment_value", "price",
            "freight_value", "amount", "sales", "value"
        },
        "sales planning": {
            "sales", "revenue", "payment_value",
            "price", "amount", "quantity"
        },
        "customer strategy": {
            "customer", "customer_id",
            "customer_unique_id", "review_score",
            "satisfaction"
        },
        "product strategy": {
            "product", "product_id",
            "price", "quantity", "sales"
        },
        "business strategy": {
            "revenue", "sales", "payment_value",
            "customer", "product", "order"
        },
    }

    INDIRECT_SIGNALS = {
        "revenue strategy": {
            "order_id", "product_id",
            "seller_id", "quantity"
        },
        "sales planning": {
            "order_id", "product_id",
            "seller_id"
        },
        "customer strategy": {
            "order_id", "customer_id",
            "customer_unique_id", "city", "state"
        },
        "product strategy": {
            "order_id", "seller_id",
            "category"
        },
        "business strategy": {
            "order_id", "product_id",
            "seller_id", "customer_id"
        },
    }

    direct = []
    indirect = []

    for column in normalized_columns:

        if column in DIRECT_SIGNALS.get(decision_key, set()):
            direct.append(column)

        elif column in INDIRECT_SIGNALS.get(decision_key, set()):
            indirect.append(column)

    return {
        "direct": direct,
        "indirect": indirect,
    }

# ============================================================
# ANALYTICAL GRAIN
# ============================================================

def _grain_score(item, decision):
    """
    Score how appropriate the table's analytical grain is for the decision.

    This is intentionally separate from relationships. A table can be highly
    connected yet still be the wrong grain for the requested decision.
    """
    profile = _decision_profile(decision)
    grain_rules = profile.get("grain", {})

    if not grain_rules:
        return 0.0, "no grain rule"

    text = _normalise(
        _name(item) + " " + " ".join(map(str, _columns(item)))
    )

    tokens = set(text.split())

    best_score = 0.0
    best_grain = None

    for grain, score in grain_rules.items():
        grain_tokens = set(_normalise(grain).split())

        if grain_tokens.issubset(tokens):
            if score > best_score:
                best_score = float(score)
                best_grain = grain

    if best_grain is None:
        return 0.0, "unmatched"

    return best_score, best_grain


# ============================================================
# ROLE + DECISION COMPATIBILITY
# ============================================================

def _role_score(role, decision):
    """
    Convert role compatibility to a 0-20 score.
    """
    profile = _decision_profile(decision)
    compatibility = profile.get("preferred_roles", {})
    strength = compatibility.get(role, 0.0)

    return round(strength * 20.0, 2)


# ============================================================
# RELATIONSHIP SCORE
# ============================================================

def _relationship_score(nrel):
    """
    Relationship connectivity is useful, but deliberately capped at 10.
    """
    if nrel >= 5:
        return 10.0
    if nrel == 4:
        return 8.5
    if nrel == 3:
        return 7.0
    if nrel == 2:
        return 5.0
    if nrel == 1:
        return 2.5
    return 0.0


# ============================================================
# INTELLIGENCE SCORE
# ============================================================

def _intelligence_score(item):
    try:
        value = float(
            item.get(
                "intelligence_score",
                item.get("score", 0),
            )
        )
    except (TypeError, ValueError):
        value = 0.0

    return max(0.0, min(100.0, value))


# ============================================================
# DECISION-AWARE TABLE SELECTION
# ============================================================

def select_decision_tables(inspection, decision):
    """
    Decision-aware table selection.

    Priority:
        1. Decision alignment
        2. Direct signals
        3. Decision-specific grain
        4. Table role
        5. Relationships
        6. General intelligence

    Direct signals are stronger than indirect/contextual signals.
    """

    files = [
        x for x in inspection.get("files", [])
        if x.get("success")
    ]

    if not files:
        return {
            "decision": decision,
            "primary_table": None,
            "ranking": [],
            "supporting_tables": [],
            "confidence": 0.0
        }

    # ------------------------------------------------------------
    # RELATIONSHIP COUNTS
    # ------------------------------------------------------------

    counts = _relationship_counts(
        files,
        inspection.get("relationships", [])
    )

    # ------------------------------------------------------------
    # DECISION-SPECIFIC SIGNALS
    # ------------------------------------------------------------

    SIGNALS = {

        "revenue strategy": {
            "direct": {
                "revenue",
                "sales",
                "amount",
                "payment_value",
                "price",
                "freight_value",
                "total_value",
                "order_value",
                "sales_amount",
                "transaction_value",
            },

            "indirect": {
                "order_id",
                "order_item_id",
                "product_id",
                "seller_id",
                "customer_id",
                "quantity",
            },

            "preferred_grains": {
                "payment": 20,
                "order_item": 18,
                "order": 14,
            },
        },

        "sales planning": {
            "direct": {
                "sales",
                "revenue",
                "amount",
                "payment_value",
                "price",
                "quantity",
                "total_value",
            },

            "indirect": {
                "order_id",
                "order_item_id",
                "product_id",
                "seller_id",
                "customer_id",
            },

            "preferred_grains": {
                "order_item": 20,
                "order": 18,
                "payment": 16,
                "product": 12,
            },
        },

        "customer strategy": {
            "direct": {
                "customer_id",
                "customer_unique_id",
                "customer",
                "review_score",
                "satisfaction",
                "customer_satisfaction",
            },

            "indirect": {
                "order_id",
                "order_item_id",
                "city",
                "state",
                "zip_code",
            },

            "preferred_grains": {
                "customer": 20,
                "order": 16,
            },
        },

        "product strategy": {
            "direct": {
                "product_id",
                "product",
                "price",
                "quantity",
                "sales",
                "revenue",
                "product_category_name",
            },

            "indirect": {
                "order_id",
                "order_item_id",
                "seller_id",
                "review_score",
            },

            "preferred_grains": {
                "product": 20,
                "order_item": 18,
            },
        },

        "business strategy": {
            "direct": {
                "revenue",
                "sales",
                "payment_value",
                "amount",
                "price",
                "customer",
                "product",
            },

            "indirect": {
                "order_id",
                "order_item_id",
                "customer_id",
                "product_id",
                "seller_id",
            },

            "preferred_grains": {
                "order": 18,
                "order_item": 18,
                "payment": 18,
                "customer": 14,
                "product": 14,
            },
        },

        "career planning": {
            "direct": {
                "salary",
                "starting_salary",
                "current_salary",
                "career_satisfaction",
                "job_offers",
                "employment",
                "promotion",
                "years_to_promotion",
                "skill",
                "skills",
            },

            "indirect": {
                "student_id",
                "university",
                "degree",
                "gpa",
            },

            "preferred_grains": {
                "student": 20,
                "employee": 20,
                "career": 20,
            },
        },
    }

    decision_key = _normalise(decision)

    config = SIGNALS.get(
        decision_key,
        {
            "direct": set(),
            "indirect": set(),
            "preferred_grains": {}
        }
    )

    direct_signals = config["direct"]
    indirect_signals = config["indirect"]
    preferred_grains = config["preferred_grains"]

    # ------------------------------------------------------------
    # ROLE WEIGHTS
    # ------------------------------------------------------------

    ROLE_SCORES = {
        "FACT": 15,
        "BRIDGE": 11,
        "DIMENSION": 7,
        "SUPPORTING": 4,
        "REFERENCE": 2,
        "UNKNOWN": 0,
    }

    # ------------------------------------------------------------
    # GRAIN DETECTION
    # ------------------------------------------------------------

    def detect_grain(item):

        text = _normalise(
            _name(item)
            + " "
            + " ".join(
                map(str, _columns(item))
            )
        )

        grain_patterns = [
            ("payment", ["payment", "payment_value"]),
            ("order_item", ["order_item", "order_item_id"]),
            ("order", ["order", "order_id"]),
            ("customer", ["customer", "customer_id"]),
            ("product", ["product", "product_id"]),
            ("seller", ["seller", "seller_id"]),
            ("student", ["student", "student_id"]),
            ("employee", ["employee", "employee_id"]),
            ("career", ["career"]),
        ]

        for grain, patterns in grain_patterns:
            for pattern in patterns:
                if pattern in text:
                    return grain

        return "unmatched"

    # ------------------------------------------------------------
    # NORMALIZE COLUMN NAMES
    # ------------------------------------------------------------

    def normalized_columns(item):

        columns = _columns(item)

        result = set()

        for column in columns:

            value = str(column).lower().strip()

            value = re.sub(
                r"[^a-z0-9_]+",
                "_",
                value
            )

            result.add(value)

        return result

    # ------------------------------------------------------------
    # SCORE TABLES
    # ------------------------------------------------------------

    ranked = []

    for item in files:

        name = _name(item)

        columns = normalized_columns(item)

        role = str(
            item.get("table_role")
            or item.get("role")
            or "UNKNOWN"
        ).upper()

        # --------------------------------------------------------
        # DIRECT SIGNALS
        # --------------------------------------------------------

        direct_matches = sorted(
            columns.intersection(
                direct_signals
            )
        )

        indirect_matches = sorted(
            columns.intersection(
                indirect_signals
            )
        )

        # Direct signals are intentionally dominant.
        direct_score = min(
            30.0,
            len(direct_matches) * 8.0
        )

        # Small contextual contribution.
        indirect_score = min(
            5.0,
            len(indirect_matches) * 1.5
        )

        signal_score = min(
            30.0,
            direct_score + indirect_score
        )

        # --------------------------------------------------------
        # DECISION ALIGNMENT
        # --------------------------------------------------------

        decision_score = min(
            30.0,
            direct_score + indirect_score
        )

        # --------------------------------------------------------
        # GRAIN
        # --------------------------------------------------------

        grain = detect_grain(item)

        grain_score = preferred_grains.get(
            grain,
            0
        )

        # --------------------------------------------------------
        # ROLE
        # --------------------------------------------------------

        role_score = ROLE_SCORES.get(
            role,
            0
        )

        # --------------------------------------------------------
        # RELATIONSHIPS
        # --------------------------------------------------------

        relationship_count = counts.get(
            name,
            0
        )

        relationship_score = min(
            5.0,
            relationship_count * 1.25
        )

        # --------------------------------------------------------
        # INTELLIGENCE
        # --------------------------------------------------------

        try:
            intelligence = float(
                item.get(
                    "intelligence_score",
                    item.get("score", 0)
                )
            )
        except (
            TypeError,
            ValueError
        ):
            intelligence = 0.0

        intelligence_score = min(
            5.0,
            intelligence / 20.0
        )

        # --------------------------------------------------------
        # FINAL SCORE
        # --------------------------------------------------------

        total = (
            decision_score
            + grain_score
            + role_score
            + relationship_score
            + intelligence_score
        )

        total = min(
            100.0,
            max(0.0, total)
        )

        ranked.append({

            "file": item.get("file"),

            "name": name,

            "role": role,

            "grain": grain,

            "score": round(
                total,
                2
            ),

            "decision_score": round(
                decision_score,
                2
            ),

            "direct_score": round(
                direct_score,
                2
            ),

            "indirect_score": round(
                indirect_score,
                2
            ),

            "grain_score": round(
                grain_score,
                2
            ),

            "role_score": round(
                role_score,
                2
            ),

            "relationship_score": round(
                relationship_score,
                2
            ),

            "intelligence_score": round(
                intelligence_score,
                2
            ),

            "relationships": relationship_count,

            "direct_signals": direct_matches,

            "indirect_signals": indirect_matches,
        })

    # ------------------------------------------------------------
    # RANK
    # ------------------------------------------------------------

    ranked.sort(
        key=lambda x: (
            x["score"],
            x["decision_score"],
            x["direct_score"],
            x["grain_score"],
            x["role_score"],
            x["relationships"]
        ),
        reverse=True
    )

    primary = ranked[0]

    # ------------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------------

    if len(ranked) > 1:

        gap = (
            primary["score"]
            - ranked[1]["score"]
        )

    else:

        gap = 30.0

    confidence = min(
        95.0,
        max(
            60.0,
            60.0 + gap * 2
        )
    )

    # ------------------------------------------------------------
    # RETURN
    # ------------------------------------------------------------

    return {

        "decision": decision,

        "primary_table": primary,

        "ranking": ranked,

        "supporting_tables": ranked[1:],

        "confidence": round(
            confidence,
            2
        ),
    }

    return {
        "decision": decision,
        "primary_table": primary,
        "ranking": ranked,
        "supporting_tables": ranked[1:],
        "confidence": confidence,
    }


# ============================================================
# DISPLAY
# ============================================================

def display_selection(result):
    print()
    print("=" * 80)
    print("        CHRONOPATH AI - DECISION-AWARE TABLE SELECTION")
    print("=" * 80)
    print()

    print(f"Decision: {result['decision']}")
    print()

    print("-" * 80)
    print("PRIMARY TABLE")
    print("-" * 80)

    primary = result.get("primary_table")

    if not primary:
        print("No usable table found.")
        return

    print(f"File:       {primary['file']}")
    print(f"Role:       {primary['role']}")
    print(f"Grain:      {primary['grain']}")
    print(f"Score:      {primary['score']}/100")
    print(f"Confidence: {result['confidence']}%")

    print()
    print(
        "Reason:     "
        f"role={primary['role']}, "
        f"grain={primary['grain']}, "
        f"{primary['relationships']} relationship(s)."
    )

    print(
        "Components: "
        f"decision={primary['decision_score']}/30, "
        f"direct={primary['direct_score']}/30, "
        f"indirect={primary['indirect_score']}/5, "
        f"grain={primary['grain_score']}/20, "
        f"role={primary['role_score']}/15, "
        f"relationships={primary['relationship_score']}/5, "
        f"intelligence={primary['intelligence_score']}/5"
    )

    print(
        "Direct signals:   "
        + (
            ", ".join(primary["direct_signals"])
            if primary["direct_signals"]
            else "None"
        )
    )

    print(
        "Indirect signals: "
        + (
            ", ".join(primary["indirect_signals"])
            if primary["indirect_signals"]
            else "None"
        )
    )

    print()
    print("-" * 80)
    print("TABLE RANKING")
    print("-" * 80)

    for i, row in enumerate(result["ranking"], 1):

        print()
        print(f"{i}. {row['file']}")
        print(f"   Role: {row['role']}")
        print(f"   Grain: {row['grain']}")
        print(f"   Score: {row['score']}/100")
        print(f"   Relationships: {row['relationships']}")

        print(
            f"   Decision alignment: "
            f"{row['decision_score']}/30"
        )

        print(
            f"   Direct signals: "
            f"{row['direct_score']}/30"
        )

        print(
            f"   Indirect signals: "
            f"{row['indirect_score']}/5"
        )

        print(
            f"   Role score: "
            f"{row['role_score']}/15"
        )

        print(
            f"   Grain score: "
            f"{row['grain_score']}/20"
        )

        print(
            f"   Relationship score: "
            f"{row['relationship_score']}/5"
        )

        print(
            f"   Intelligence score: "
            f"{row['intelligence_score']}/5"
        )

        print(
            "   Direct: "
            + (
                ", ".join(row["direct_signals"])
                if row["direct_signals"]
                else "None"
            )
        )

        print(
            "   Indirect: "
            + (
                ", ".join(row["indirect_signals"])
                if row["indirect_signals"]
                else "None"
            )
        )

    print()
    print("-" * 80)
    print("SUPPORTING TABLES")
    print("-" * 80)

    for row in result["supporting_tables"]:

        print(
            f"  - {row['file']} "
            f"({row['role']}, "
            f"{row['score']}/100)"
        )

    print()
    print("=" * 80)
    print("        TABLE SELECTION COMPLETE")
    print("=" * 80)


# Pipeline-friendly alias
select_primary_table = select_decision_tables