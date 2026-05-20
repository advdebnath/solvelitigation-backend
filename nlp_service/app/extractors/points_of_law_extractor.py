import re
from collections import defaultdict

# =========================================================
# 🔥 LEGAL ISSUE ONTOLOGY
# =========================================================

LEGAL_POINT_PATTERNS = {

    "Wakf Property Dispute": [
        "wakf property",
        "wakf board",
        "wakf tribunal"
    ],

    "Tenancy Surrender": [
        "surrender tenancy",
        "tenancy rights",
        "tenant in the premises"
    ],

    "Joint Hindu Family": [
        "joint hindu family",
        "karta",
        "coparcener"
    ],

    "Constitutional Jurisdiction": [
        "article 226",
        "article 227",
        "writ petition"
    ],

    "Bail": [
        "anticipatory bail",
        "regular bail",
        "grant of bail"
    ],

    "Murder": [
        "section 302",
        "murder",
        "homicide"
    ]
}

# =========================================================
# 🔥 CATEGORY DETECTION
# =========================================================

def detect_category(text):

    text = text.lower()

    if any(x in text for x in [
        "fir",
        "charge sheet",
        "accused",
        "conviction",
        "sentence"
    ]):
        return "Criminal"

    return "Civil"

# =========================================================
# 🔥 MAIN EXTRACTOR
# =========================================================

def extract_points_of_law(
    full_text="",
    acts=None,
    clustered_issues=None
):

    if acts is None:
        acts = []

    if clustered_issues is None:
        clustered_issues = []

    text = full_text.lower()

    detected = defaultdict(int)

    category = detect_category(text)

    # -----------------------------------------------------
    # 🔥 PRIORITY 1 → CLUSTERED ISSUES
    # -----------------------------------------------------

    for issue in clustered_issues:

        issue_name = issue.get("issue", "").strip()

        score = issue.get("score", 0)

        if not issue_name:
            continue

        detected[issue_name] += (
            100 + score
        )

    # -----------------------------------------------------
    # 🔥 PRIORITY 2 → LEGAL PHRASES
    # -----------------------------------------------------

    for point, patterns in LEGAL_POINT_PATTERNS.items():

        for pattern in patterns:

            hits = len(
                re.findall(
                    re.escape(pattern),
                    text,
                    flags=re.I
                )
            )

            if hits:

                detected[point] += hits * 10

    # -----------------------------------------------------
    # 🔥 ACT BASED BOOST
    # -----------------------------------------------------

    acts_lower = [
        a.lower() for a in acts
    ]

    if any("wakf" in a for a in acts_lower):

        detected["Wakf Property Dispute"] += 100

    if any("constitution" in a for a in acts_lower):

        detected["Constitutional Jurisdiction"] += 40

    # -----------------------------------------------------
    # 🔥 FINAL SORTING
    # -----------------------------------------------------

    final_points = sorted(
        detected.items(),
        key=lambda x: x[1],
        reverse=True
    )

    cleaned = []

    seen = set()

    for point, score in final_points:

        if score < 20:
            continue

        normalized = point.strip()

        if normalized in seen:
            continue

        seen.add(normalized)

        cleaned.append({

            "point": normalized,

            "category": category
        })

    # -----------------------------------------------------
    # 🔥 LIMIT
    # -----------------------------------------------------

    cleaned = cleaned[:6]

    return {

        "points_of_law": cleaned,

        "category": category,

        "confidence": min(
            95,
            60 + len(cleaned) * 5
        )
    }

# =========================================================
# 🔥 LEGACY COMPATIBILITY
# =========================================================

def extract_canonical_points_of_law(
    full_text="",
    acts=None,
    clustered_issues=None
):

    return extract_points_of_law(
        full_text=full_text,
        acts=acts,
        clustered_issues=clustered_issues
    )

