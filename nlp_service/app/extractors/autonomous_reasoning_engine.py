# =========================================================
# 🔥 AUTONOMOUS LEGAL REASONING ENGINE
# =========================================================

import re


def generate_autonomous_legal_reasoning(
    dominant_issue=None,
    semantic_precedent_data=None,
    litigation_strategy_data=None,
    judgment_outcome_data=None,
    contradiction_risk_data=None,
    legal_copilot_data=None,
):

    try:

        result = {
            "dominant_issue": "General",
            "recommended_path": "",
            "strongest_precedents": [],
            "risk_assessment": [],
            "strategic_advice": "",
            "predicted_outcome": "",
            "autonomous_reasoning": "",
            "confidence": 0,
        }

        # -------------------------------------------------
        # ISSUE
        if isinstance(dominant_issue, dict):

            issue = dominant_issue.get("dominant_issue")

        elif isinstance(dominant_issue, str):

            issue = re.sub(r"\\s+", " ", dominant_issue).strip()

        result["dominant_issue"] = issue if issue else "General"

        # -------------------------------------------------
        # PRECEDENTS
        # -------------------------------------------------

        if isinstance(semantic_precedent_data, dict):

            precedents = semantic_precedent_data.get("recommended_precedents", [])

            result["strongest_precedents"] = precedents[:5]

        # -------------------------------------------------
        # STRATEGY
        # -------------------------------------------------

        if isinstance(litigation_strategy_data, dict):

            result["strategic_advice"] = litigation_strategy_data.get(
                "recommended_strategy", ""
            )

        # -------------------------------------------------
        # OUTCOME
        # -------------------------------------------------

        if isinstance(judgment_outcome_data, dict):

            result["predicted_outcome"] = judgment_outcome_data.get(
                "predicted_outcome", ""
            )

        # -------------------------------------------------
        # RISKS
        # -------------------------------------------------

        if isinstance(contradiction_risk_data, dict):

            result["risk_assessment"] = contradiction_risk_data.get(
                "identified_risks", []
            )

        # -------------------------------------------------
        # RECOMMENDED PATH
        # -------------------------------------------------

        path = []

        if result["strategic_advice"]:

            path.append(result["strategic_advice"])

        if result["risk_assessment"]:

            path.append("Mitigate identified litigation risks.")

        if result["strongest_precedents"]:

            path.append("Rely strongly on recommended precedents.")

        result["recommended_path"] = " ".join(path)

        # -------------------------------------------------
        # AUTONOMOUS REASONING
        # -------------------------------------------------

        reasoning = []

        reasoning.append(f"Dominant issue identified as {result['dominant_issue']}.")

        if result["strongest_precedents"]:

            reasoning.append("Relevant precedents support the litigation pathway.")

        if result["risk_assessment"]:

            reasoning.append("Potential litigation risks require strategic handling.")

        if result["predicted_outcome"]:

            reasoning.append(
                f"Predicted judicial outcome indicates: {result['predicted_outcome']}."
            )

        if isinstance(legal_copilot_data, dict):

            summary = legal_copilot_data.get("copilot_summary", "")

            if summary:

                reasoning.append(summary)

        result["autonomous_reasoning"] = " ".join(reasoning)

        # -------------------------------------------------
        # CONFIDENCE
        # -------------------------------------------------

        confidence = 75

        confidence += len(result["strongest_precedents"]) * 2

        confidence += len(result["risk_assessment"])

        result["confidence"] = min(98, confidence)

        print("✅ Autonomous Legal Reasoning Generated:")

        print(result)

        return result

    except Exception as e:

        print("❌ Autonomous Reasoning Error:", str(e))

        return {
            "dominant_issue": "General",
            "recommended_path": "",
            "strongest_precedents": [],
            "risk_assessment": [],
            "strategic_advice": "",
            "predicted_outcome": "",
            "autonomous_reasoning": "",
            "confidence": 0,
        }
