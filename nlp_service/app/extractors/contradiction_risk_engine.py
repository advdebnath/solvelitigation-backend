# =========================================================
# 🔥 CONTRADICTION & RISK DETECTION ENGINE
# =========================================================

import re

RISK_MAP = {
    "FIR Quashing": [
        "Serious offence may limit quashing jurisdiction.",
        "Public policy considerations may override settlement.",
    ],
    "Liberty Oriented Bail Jurisprudence": [
        "Criminal antecedents may weaken bail claim.",
        "Possibility of tampering with evidence may be considered.",
    ],
    "Premature Release Of Life Convicts": [
        "Executive remission discretion may vary",
        "Victim rights objections may arise",
        "Public policy concerns may affect relief",
    ],
    "Minimal Arbitration Interference": [
        "Scope of interference under Section 34 is narrow.",
        "Patent illegality threshold is difficult to establish.",
    ],
    "Natural Justice Expansion": [
        "Substantial compliance argument may arise.",
        "Prejudice requirement may not be satisfied.",
    ],
    "Cheque Dishonour": [
        "Statutory presumption may remain unrebutted.",
        "Existence of enforceable debt may be inferred.",
    ],
}


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def detect_contradictions_and_risks(
    dominant_issue=None,
    ai_argument_data=None,
    litigation_strategy_data=None,
    judgment_outcome_data=None,
):

    try:

        result = {
            "dominant_issue": "General",
            "identified_risks": [],
            "contradictions": [],
            "risk_level": "Moderate",
            "confidence": 0,
        }

        issue = None

        # -------------------------------------------------
        # DOMINANT ISSUE
        if isinstance(dominant_issue, dict):

            issue = dominant_issue.get("dominant_issue")

        elif isinstance(dominant_issue, str):

            issue = re.sub(r"\\s+", " ", dominant_issue).strip()

        if not issue:

            return result

        result["dominant_issue"] = issue

        # -------------------------------------------------
        # RISKS
        # -------------------------------------------------

        risks = RISK_MAP.get(issue, [])

        result["identified_risks"] = risks

        # -------------------------------------------------
        # CONTRADICTION CHECK
        # -------------------------------------------------

        if isinstance(judgment_outcome_data, dict):

            outcome = judgment_outcome_data.get("predicted_outcome", "").lower()

            if "dismissed" in outcome and issue == "FIR Quashing":

                result["contradictions"].append(
                    "Predicted dismissal conflicts with settlement-oriented strategy."
                )

        # -------------------------------------------------
        # RISK LEVEL
        # -------------------------------------------------

        if len(risks) >= 2:

            result["risk_level"] = "High"

        elif len(risks) == 1:

            result["risk_level"] = "Moderate"

        else:

            result["risk_level"] = "Low"

        result["confidence"] = min(95, 60 + len(risks) * 5)

        print("✅ Contradictions & Risks:")

        print(result)

        return result

    except Exception as e:

        print("❌ Contradiction Risk Error:", str(e))

        return {
            "dominant_issue": "General",
            "identified_risks": [],
            "contradictions": [],
            "risk_level": "Moderate",
            "confidence": 0,
        }
