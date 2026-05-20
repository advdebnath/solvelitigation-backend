import math
import re

from app.legal_ontology.canonical_legal_object_engine import (

    canonicalize_point_of_law,
    canonicalize_act_name
)


# =========================================================
# 🔥 SAFE LOWER
# =========================================================

def safe_lower(value):

    if not value:

        return ""

    return str(value).lower().strip()

# =========================================================
# 🔥 NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    text = safe_lower(text)

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# =========================================================
# 🔥 NORMALIZE LIST
# =========================================================

def normalize_list(items):

    if not items:

        return set()

    result = set()

    for item in items:

        if isinstance(item, dict):

            # =============================================
            # 🔥 POINTS OF LAW
            # =============================================

            if "point" in item:

                canonical_point = (
                    canonicalize_point_of_law(
                        item["point"]
                    )
                )

                value = normalize_text(
                    canonical_point
                )

                if value:

                    result.add(value)

            # =============================================
            # 🔥 SECTIONS
            # =============================================

            elif "section" in item:

                value = normalize_text(
                    item["section"]
                )

                if value:

                    result.add(value)

            # =============================================
            # 🔥 ACTS
            # =============================================

            elif "act_name" in item:

                canonical_act = (
                    canonicalize_act_name(
                        item["act_name"]
                    )
                )

                value = normalize_text(
                    canonical_act
                )

                if value:

                    result.add(value)

        elif isinstance(item, str):

            value = normalize_text(item)

            if value:

                result.add(value)

    return result

# =========================================================
# 🔥 JACCARD SIMILARITY
# =========================================================

def jaccard_similarity(a, b):

    if not a or not b:

        return 0

    intersection = len(

        a.intersection(b)
    )

    union = len(

        a.union(b)
    )

    if union == 0:

        return 0

    return intersection / union

# =========================================================
# 🔥 TOKENIZE
# =========================================================

def tokenize(text):

    text = normalize_text(text)

    words = text.split()

    stop_words = {

        "the",
        "and",
        "that",
        "this",
        "with",
        "from",
        "under",
        "where",
        "therefore",
        "held",
        "court",
        "case",
        "petition",
        "appeal",
        "section",
        "article"
    }

    return set(

        w for w in words

        if len(w) > 2
        and w not in stop_words
    )

# =========================================================
# 🔥 TEXT SIMILARITY
# =========================================================

def text_similarity(a, b):

    a_words = tokenize(a)

    b_words = tokenize(b)

    return jaccard_similarity(

        a_words,

        b_words
    )

# =========================================================
# 🔥 CATEGORY BONUS
# =========================================================

def category_bonus(current_case, candidate_case):

    if safe_lower(

        current_case.get("category")

    ) == safe_lower(

        candidate_case.get("category")

    ):

        return 20

    return 0

# =========================================================
# 🔥 POINT SCORE
# =========================================================

def point_score(current_case, candidate_case):

    current_points = normalize_list(

        current_case.get(
            "points_of_law",
            []
        )
    )

    candidate_points = normalize_list(

        candidate_case.get(
            "points_of_law",
            []
        )
    )

    similarity = jaccard_similarity(

        current_points,

        candidate_points
    )

    return similarity * 30

# =========================================================
# 🔥 SECTION SCORE
# =========================================================

def section_score(current_case, candidate_case):

    current_sections = normalize_list(

        current_case.get(
            "sections",
            []
        )
    )

    candidate_sections = normalize_list(

        candidate_case.get(
            "sections",
            []
        )
    )

    similarity = jaccard_similarity(

        current_sections,

        candidate_sections
    )

    return similarity * 25

# =========================================================
# 🔥 ACT SCORE
# =========================================================

def act_score(current_case, candidate_case):

    current_acts = normalize_list(

        current_case.get(
            "acts",
            []
        )
    )

    candidate_acts = normalize_list(

        candidate_case.get(
            "acts",
            []
        )
    )

    similarity = jaccard_similarity(

        current_acts,

        candidate_acts
    )

    return similarity * 15

# =========================================================
# 🔥 RATIO SCORE
# =========================================================

def ratio_score(current_case, candidate_case):

    current_ratio = current_case.get(
        "ratio",
        ""
    )

    candidate_ratio = candidate_case.get(
        "ratio",
        ""
    )

    similarity = text_similarity(

        current_ratio,

        candidate_ratio
    )

    return similarity * 10

# =========================================================
# 🔥 COMPUTE SIMILARITY
# =========================================================

def compute_similarity(current_case, candidate_case):

    score = 0

    score += category_bonus(

        current_case,

        candidate_case
    )

    score += point_score(

        current_case,

        candidate_case
    )

    score += section_score(

        current_case,

        candidate_case
    )

    score += act_score(

        current_case,

        candidate_case
    )

    score += ratio_score(

        current_case,

        candidate_case
    )

    return round(score, 2)

# =========================================================
# 🔥 FIND SIMILAR CASES
# =========================================================

def find_similar_cases(

    current_case,

    database_cases,

    top_k=5
):

    try:

        if not current_case:

            return []

        results = []

        for case in database_cases:

            similarity = compute_similarity(

                current_case,

                case
            )

            if similarity > 15:

                results.append({

                    "case_number": case.get("caseNumber") or case.get("case_number") or "Unknown",

                    "category": case.get(
                        "category",
                        "Unknown"
                    ),

                    "similarity": similarity,

                    "matching_points": [

                        p.get("point")

                        for p in case.get(
                            "points_of_law",
                            []
                        )

                        if isinstance(p, dict)
                    ][:5],

                    "ratio": str(

                        case.get(
                            "ratio",
                            ""
                        ) or ""

                    )[:500]
                })

        # =====================================================
        # 🔥 SORT
        # =====================================================

        results.sort(

            key=lambda x: x["similarity"],

            reverse=True
        )

        final_results = results[:top_k]

        print(

            "✅ Similar Cases Found:",

            final_results
        )

        return final_results

    except Exception as e:

        print(
            "❌ PRECEDENT ENGINE ERROR:",
            e
        )

        return []

# =====================================================
# 🔥 GET STRONGEST CASE
# =====================================================

def get_strongest_case(similar_cases):

    """
    Compatibility support for legal_router.
    Returns highest ranked precedent.
    """

    try:

        if not similar_cases:

            return None

        sorted_cases = sorted(

            similar_cases,

            key=lambda x: x.get(
                "similarity",
                0
            ),

            reverse=True
        )

        return sorted_cases[0]

    except Exception as e:

        print(
            "❌ Strongest Case Error:",
            e
        )

        return None

# =====================================================
# 🔥 RESOLVE CONFLICT
# =====================================================

def resolve_conflict(cases):

    """
    Compatibility support for legal_router.
    Resolves conflicting precedents.
    """

    try:

        if not cases:

            return None

        strongest = get_strongest_case(cases)

        return {

            "selected_case": strongest,

            "reason":

                "Highest similarity precedent selected",

            "confidence":

                strongest.get(
                    "similarity",
                    0
                ) if strongest else 0
        }

    except Exception as e:

        print(
            "❌ Conflict Resolution Error:",
            e
        )

        return None

# =====================================================
# 🔥 COMPARE PRECEDENTS
# =====================================================

def compare_precedents(case_a, case_b):

    """
    Compare two precedents directly.
    """

    try:

        score = compute_similarity(

            case_a,

            case_b
        )

        return {

            "case_a":

                case_a.get("caseNumber") or case_a.get("case_number") or "Unknown",

            "case_b":

                case_b.get("caseNumber") or case_b.get("case_number") or "Unknown",

            "similarity":
                score,

            "stronger":

                case_a.get("caseNumber") or case_a.get("case_number")

                if score >= 50

                else case_b.get("caseNumber") or case_b.get("case_number")
        }

    except Exception as e:

        print(
            "❌ Compare Precedents Error:",
            e
        )

        return {

            "similarity": 0
        }

# =====================================================
# 🔥 GET TOP PRECEDENTS
# =====================================================

def get_top_precedents(

    current_case,

    database_cases,

    limit=3
):

    results = find_similar_cases(

        current_case,

        database_cases,

        top_k=limit
    )

    return results

# =====================================================
# 🔥 DIRECT TEST
# =====================================================

if __name__ == "__main__":

    sample_current = {

        "category": "Criminal",

        "points_of_law": [

            {"point": "Murder"}
        ],

        "sections": [

            {"section": "302"}
        ],

        "acts": [

            {
                "act_name":
                "Indian Penal Code, 1860"
            }
        ],

        "ratio":
            "Conviction sustainable"
    }

    sample_db = [

        {

            "case_number":
                "Criminal Appeal 101",

            "category":
                "Criminal",

            "points_of_law": [

                {"point": "Murder"}
            ],

            "sections": [

                {"section": "302"}
            ],

            "acts": [

                {
                    "act_name":
                    "Indian Penal Code, 1860"
                }
            ],

            "ratio":
                "Conviction sustainable"
        }
    ]

    print(

        find_similar_cases(

            sample_current,

            sample_db
        )
    )


# =========================================================
# 🔥 PRECEDENT WEIGHT CLASSIFIER
# =========================================================

def assign_weight(score: float) -> str:

    """
    Assign precedent importance level
    based on similarity / authority score.
    """

    try:

        score = float(score)

    except Exception:

        return "LOW"

    if score >= 0.90:
        return "VERY_HIGH"

    elif score >= 0.75:
        return "HIGH"

    elif score >= 0.60:
        return "MEDIUM"

    elif score >= 0.40:
        return "LOW"

    return "VERY_LOW"
