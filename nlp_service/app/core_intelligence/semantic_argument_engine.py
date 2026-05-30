from collections import defaultdict

# =========================================================
# 🔥 ARGUMENT STRATEGY RULES
# =========================================================

ARGUMENT_STRATEGIES = {
    "REINSTATEMENT": {
        "dominant_strategy": "PROCEDURAL_FAIRNESS",
        "supporting_doctrines": ["NATURAL JUSTICE", "SUBSTANTIAL JUSTICE"],
    },
    "BAIL": {
        "dominant_strategy": "CIVIL_LIBERTY",
        "supporting_doctrines": ["PERSONAL LIBERTY", "ARTICLE 21"],
    },
    "TAXATION": {
        "dominant_strategy": "STRICT_STATUTORY_INTERPRETATION",
        "supporting_doctrines": ["LITERAL INTERPRETATION", "FISCAL DISCIPLINE"],
    },
}


# =========================================================
# 🔥 SAFE NORMALIZER
# =========================================================


def normalize_text(value):

    if not value:
        return ""

    return str(value).strip().upper()


# =========================================================
# 🔥 ARGUMENT GENERATOR
# =========================================================


def generate_semantic_argument(issue, precedent_graph=None, judicial_profile=None):

    issue = normalize_text(issue)

    precedent_graph = precedent_graph or {}

    judicial_profile = judicial_profile or {}

    strategy = ARGUMENT_STRATEGIES.get(
        issue,
        {
            "dominant_strategy": "GENERAL_LEGAL_REASONING",
            "supporting_doctrines": ["FAIRNESS", "RULE OF LAW"],
        },
    )

    precedents = []

    connected = precedent_graph.get("connected_cases", [])

    for case in connected[:5]:

        precedents.append(case.get("target_case", "UNKNOWN"))

    judicial_alignment = judicial_profile.get("dominant_philosophy", "NEUTRAL")

    return {
        "issue": issue,
        "recommended_argument": {
            "dominant_strategy": strategy["dominant_strategy"],
            "supporting_doctrines": strategy["supporting_doctrines"],
            "supporting_precedents": precedents,
            "judicial_alignment": judicial_alignment,
        },
    }


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    precedent_graph = {
        "connected_cases": [
            {"target_case": "2024 SLSC 101"},
            {"target_case": "2018 SLSC 55"},
        ]
    }

    judicial_profile = {"dominant_philosophy": "CONSTITUTIONAL_LIBERALISM"}

    result = generate_semantic_argument(
        issue="REINSTATEMENT",
        precedent_graph=precedent_graph,
        judicial_profile=judicial_profile,
    )

    print(result)
