from difflib import SequenceMatcher


# =========================================================
# 🔥 SAFE NORMALIZER
# =========================================================

def normalize_text(value):

    if not value:
        return ""

    return str(value).strip().upper()


# =========================================================
# 🔥 SAFE LIST NORMALIZER
# =========================================================

def normalize_list(values):

    if not values:
        return []

    normalized = []

    for item in values:

        item = normalize_text(item)

        if item and item not in normalized:

            normalized.append(item)

    return normalized


# =========================================================
# 🔥 TEXT SIMILARITY
# =========================================================

def similarity(a, b):

    a = normalize_text(a)
    b = normalize_text(b)

    if not a or not b:
        return 0

    return int(
        SequenceMatcher(
            None,
            a,
            b
        ).ratio() * 100
    )


# =========================================================
# 🔥 OVERLAP SCORE
# =========================================================

def overlap_score(list_a, list_b):

    a = set(
        normalize_list(list_a)
    )

    b = set(
        normalize_list(list_b)
    )

    if not a or not b:
        return 0

    intersection = len(a.intersection(b))

    union = len(a.union(b))

    return int(
        (intersection / union) * 100
    )


# =========================================================
# 🔥 PRECEDENT RELATIONSHIP ENGINE
# =========================================================

def build_precedent_relationship(

    source_case,

    candidate_case
):

    source_case_number = source_case.get(
        "caseNumber",
        "UNKNOWN"
    )

    candidate_case_number = candidate_case.get(
        "caseNumber",
        "UNKNOWN"
    )

    # -----------------------------------------------------
    # 🔥 CATEGORY SCORE
    # -----------------------------------------------------

    category_score = similarity(

        source_case.get(
            "category",
            ""
        ),

        candidate_case.get(
            "category",
            ""
        )
    )

    # -----------------------------------------------------
    # 🔥 ACT SCORE
    # -----------------------------------------------------

    act_score = overlap_score(

        source_case.get(
            "actNames",
            []
        ),

        candidate_case.get(
            "actNames",
            []
        )
    )

    # -----------------------------------------------------
    # 🔥 POINT OF LAW SCORE
    # -----------------------------------------------------

    point_score = overlap_score(

        source_case.get(
            "pointsOfLaw",
            []
        ),

        candidate_case.get(
            "pointsOfLaw",
            []
        )
    )

    # -----------------------------------------------------
    # 🔥 JUDGE SCORE
    # -----------------------------------------------------

    judge_score = overlap_score(

        source_case.get(
            "judges",
            []
        ),

        candidate_case.get(
            "judges",
            []
        )
    )

    # -----------------------------------------------------
    # 🔥 FINAL SCORE
    # -----------------------------------------------------

    final_score = int(

        (
            category_score * 0.20
            +
            act_score * 0.30
            +
            point_score * 0.35
            +
            judge_score * 0.15
        )
    )

    relationship = "WEAK_PRECEDENT"

    if final_score >= 85:

        relationship = (
            "STRONG_PRECEDENT_CONNECTION"
        )

    elif final_score >= 65:

        relationship = (
            "MODERATE_PRECEDENT_CONNECTION"
        )

    elif final_score >= 45:

        relationship = (
            "SEMANTICALLY_RELATED"
        )

    return {

        "source_case": source_case_number,

        "target_case": candidate_case_number,

        "relationship": relationship,

        "confidence": final_score,

        "score_breakdown": {

            "category_score": category_score,

            "act_score": act_score,

            "point_score": point_score,

            "judge_score": judge_score
        }
    }


# =========================================================
# 🔥 GRAPH BUILDER
# =========================================================

def build_precedent_graph(

    source_case,

    candidate_cases
):

    graph = {

        "source_case": source_case.get(
            "caseNumber",
            "UNKNOWN"
        ),

        "connected_cases": []
    }

    if not candidate_cases:
        return graph

    for candidate in candidate_cases:

        relation = build_precedent_relationship(

            source_case,

            candidate
        )

        graph["connected_cases"].append(
            relation
        )

    graph["connected_cases"] = sorted(

        graph["connected_cases"],

        key=lambda x: x["confidence"],

        reverse=True
    )

    return graph


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    source_case = {

        "caseNumber": "2024 SLSC 101",

        "category": "SERVICE LAW",

        "actNames": [
            "CONSTITUTION OF INDIA"
        ],

        "pointsOfLaw": [
            "REINSTATEMENT",
            "DEPARTMENTAL ENQUIRY"
        ],

        "judges": [
            "Justice Chandrachud"
        ]
    }

    candidate_cases = [

        {

            "caseNumber": "2021 SLSC 55",

            "category": "SERVICE LAW",

            "actNames": [
                "CONSTITUTION OF INDIA"
            ],

            "pointsOfLaw": [
                "REINSTATEMENT"
            ],

            "judges": [
                "Justice Chandrachud"
            ]
        },

        {

            "caseNumber": "2020 SLHC_DEL 44",

            "category": "TAXATION",

            "actNames": [
                "GST ACT"
            ],

            "pointsOfLaw": [
                "INPUT TAX CREDIT"
            ],

            "judges": [
                "Justice Rao"
            ]
        }
    ]

    result = build_precedent_graph(

        source_case,

        candidate_cases
    )

    print(result)
