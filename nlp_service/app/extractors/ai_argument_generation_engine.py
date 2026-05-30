# =========================================================
# 🔥 AI ARGUMENT GENERATION ENGINE
# =========================================================


ARGUMENT_TEMPLATES = {
    "FIR Quashing": [
        "Continuation of criminal proceedings would amount to abuse of process of law.",
        "Parties have voluntarily settled the dispute.",
        "Quashing would secure the ends of justice.",
    ],
    "Liberty Oriented Bail Jurisprudence": [
        "Personal liberty under Article 21 deserves constitutional protection.",
        "Custodial interrogation is unnecessary.",
        "Bail is the rule and jail is the exception.",
    ],
    "Premature Release Of Life Convicts": [
        "Remission consideration is a constitutional obligation",
        "Article 161 powers must be exercised fairly",
        "Reformative justice supports reintegration",
        "Long incarceration justifies premature release review",
    ],
    "Minimal Arbitration Interference": [
        "Judicial interference under Section 34 is limited.",
        "The arbitral award does not suffer from patent illegality.",
        "Courts must exercise restraint in arbitral review.",
    ],
    "Natural Justice Expansion": [
        "The impugned action violates principles of natural justice.",
        "Adequate opportunity of hearing was denied.",
        "Reasoned decision-making is mandatory.",
    ],
    "Cheque Dishonour": [
        "Statutory presumption under Section 139 operates in favour of the complainant.",
        "Existence of legally enforceable debt stands established.",
        "Burden shifts upon the accused to rebut the presumption.",
    ],
}


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def generate_ai_arguments(
    dominant_issue=None,
    litigation_strategy_data=None,
    semantic_precedent_data=None,
    judge_behaviour_data=None,
    temporal_jurisprudence_data=None,
):

    try:

        result = {
            "dominant_issue": "General",
            "arguments": [],
            "precedents": [],
            "strategy": "",
            "judge_behaviour": "Neutral",
            "confidence": 0,
        }

        issue = None

        # -------------------------------------------------
        # DOMINANT ISSUE
        # -------------------------------------------------

        if isinstance(dominant_issue, dict):

            issue = dominant_issue.get("dominant_issue")
        elif isinstance(dominant_issue, str):

            issue = dominant_issue.strip()

        if not issue:

            return result

        result["dominant_issue"] = issue

        # -------------------------------------------------
        # ARGUMENTS
        # -------------------------------------------------

        result["arguments"] = ARGUMENT_TEMPLATES.get(issue, [])

        # -------------------------------------------------
        # STRATEGY
        # -------------------------------------------------

        if isinstance(litigation_strategy_data, dict):

            result["strategy"] = litigation_strategy_data.get(
                "recommended_strategy", ""
            )

        # -------------------------------------------------
        # PRECEDENTS
        # -------------------------------------------------

        if isinstance(semantic_precedent_data, dict):

            result["precedents"] = semantic_precedent_data.get(
                "recommended_precedents", []
            )

        # -------------------------------------------------
        # JUDGE BEHAVIOUR
        # -------------------------------------------------

        if isinstance(judge_behaviour_data, dict):

            result["judge_behaviour"] = judge_behaviour_data.get(
                "dominant_behaviour", "Neutral"
            )

        # -------------------------------------------------
        # TEMPORAL DOCTRINE
        # -------------------------------------------------

        if isinstance(temporal_jurisprudence_data, dict):

            result["dominant_doctrine"] = temporal_jurisprudence_data.get(
                "dominant_doctrine", "General"
            )

        result["confidence"] = min(95, 60 + len(result["arguments"]) * 5)

        print("✅ AI Arguments Generated:")

        print(result)

        return result

    except Exception as e:

        print("❌ AI Argument Generation Error:", str(e))

        return {
            "dominant_issue": issue if issue else "General",
            "arguments": [],
            "precedents": [],
            "strategy": "",
            "judge_behaviour": "Neutral",
            "confidence": 0,
        }
