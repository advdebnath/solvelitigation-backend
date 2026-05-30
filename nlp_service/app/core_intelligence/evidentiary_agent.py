# =========================================================
# 🔥 EVIDENTIARY INTELLIGENCE AGENT
# =========================================================


def run_evidentiary_analysis(
    reconstructed_text,
    semantic_confidence,
    historical_consistency_score,
    contradiction_risk_score,
):

    evidentiary_weight = {
        "evidence_strength": 0.50,
        "contradiction_risk": 0.50,
        "procedural_reliability": 0.50,
        "evidentiary_classification": "MODERATE",
        "strategic_evidentiary_value": "STANDARD",
    }

    try:

        upper_text = reconstructed_text.upper()

        evidence_strength = round(
            (semantic_confidence + historical_consistency_score) / 2, 2
        )

        contradiction_risk = round(contradiction_risk_score, 2)

        procedural_reliability = round(max(0.0, 1 - contradiction_risk), 2)

        evidentiary_classification = "MODERATE"

        if evidence_strength >= 0.80:

            evidentiary_classification = "HIGH"

        elif evidence_strength <= 0.40:

            evidentiary_classification = "LOW"

        strategic_evidentiary_value = "STANDARD"

        if (
            "DYING DECLARATION" in upper_text
            or "FORENSIC" in upper_text
            or "MEDICAL EVIDENCE" in upper_text
        ):

            strategic_evidentiary_value = "CRITICAL"

        evidentiary_weight.update(
            {
                "evidence_strength": evidence_strength,
                "contradiction_risk": contradiction_risk,
                "procedural_reliability": procedural_reliability,
                "evidentiary_classification": evidentiary_classification,
                "strategic_evidentiary_value": strategic_evidentiary_value,
            }
        )

    except Exception as e:

        print("❌ EVIDENTIARY AGENT ERROR:")

        print(str(e))

    return evidentiary_weight
