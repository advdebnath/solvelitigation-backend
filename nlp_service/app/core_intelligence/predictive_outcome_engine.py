# =========================================================
# 🔥 OUTCOME PREDICTION ENGINE
# =========================================================


def predict_case_outcome(
    issue, doctrine_data=None, judicial_profile=None, precedent_graph=None
):

    doctrine_data = doctrine_data or {}

    judicial_profile = judicial_profile or {}

    precedent_graph = precedent_graph or {}

    supporting_factors = []

    confidence = 50

    likely_result = "UNCERTAIN"

    # -----------------------------------------------------
    # 🔥 DOCTRINE SIGNALS
    # -----------------------------------------------------

    evolution_pattern = doctrine_data.get("evolution_pattern", "")

    if evolution_pattern == "STRICT_TO_LIBERAL":

        confidence += 15

        supporting_factors.append("LIBERAL_DOCTRINE_SHIFT")

    # -----------------------------------------------------
    # 🔥 JUDICIAL PHILOSOPHY
    # -----------------------------------------------------

    dominant_philosophy = judicial_profile.get("dominant_philosophy", "")

    if dominant_philosophy == ("CONSTITUTIONAL_LIBERALISM"):

        confidence += 15

        supporting_factors.append("CONSTITUTIONAL_LIBERALISM")

    if dominant_philosophy == ("PROCEDURAL_FAIRNESS"):

        confidence += 10

        supporting_factors.append("PROCEDURAL_FAIRNESS")

    # -----------------------------------------------------
    # 🔥 PRECEDENT STRENGTH
    # -----------------------------------------------------

    connected_cases = precedent_graph.get("connected_cases", [])

    strong_precedents = 0

    for case in connected_cases:

        if case.get("confidence", 0) >= 75:

            strong_precedents += 1

    if strong_precedents >= 1:

        confidence += 10

        supporting_factors.append("STRONG_PRECEDENT_SUPPORT")

    if confidence >= 80:

        likely_result = "RELIEF_GRANTED"

    elif confidence >= 60:

        likely_result = "PARTIAL_RELIEF"

    else:

        likely_result = "RELIEF_UNCERTAIN"

    confidence = min(confidence, 100)

    return {
        "issue": issue,
        "predicted_outcome": {
            "likely_result": likely_result,
            "confidence": confidence,
            "supporting_factors": supporting_factors,
        },
    }


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    doctrine_data = {"evolution_pattern": "STRICT_TO_LIBERAL"}

    judicial_profile = {"dominant_philosophy": "CONSTITUTIONAL_LIBERALISM"}

    precedent_graph = {"connected_cases": [{"confidence": 82}]}

    result = predict_case_outcome(
        issue="REINSTATEMENT",
        doctrine_data=doctrine_data,
        judicial_profile=judicial_profile,
        precedent_graph=precedent_graph,
    )

    print(result)
