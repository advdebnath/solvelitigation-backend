# =========================================================
# 🔥 AI LEGAL COPILOT ENGINE
# =========================================================

import re


def generate_legal_copilot_response(

    dominant_issue=None,
    semantic_precedent_data=None,
    litigation_strategy_data=None,
    ai_argument_data=None,
    judgment_outcome_data=None,
    contradiction_risk_data=None,
    legal_draft_data=None
):

    try:

        result = {

            "dominant_issue":
                "General",

            "recommended_precedents":
                [],

            "strategy":
                "",

            "arguments":
                [],

            "predicted_outcome":
                "",

            "identified_risks":
                [],

            "drafting_support":
                {},

            "copilot_summary":
                "",

            "confidence":
                0
        }

        # -------------------------------------------------
        # DOMINANT ISSUE
        if isinstance(dominant_issue, dict):

            issue = dominant_issue.get(
                "dominant_issue"
            )

        elif isinstance(dominant_issue, str):

            issue = re.sub(
                r"\\s+",
                " ",
                dominant_issue
            ).strip()

        result[
            "dominant_issue"
        ] = issue if issue else "General"

        # -------------------------------------------------
        # PRECEDENTS
        # -------------------------------------------------

        if isinstance(
            semantic_precedent_data,
            dict
        ):

            result[
                "recommended_precedents"
            ] = (

                semantic_precedent_data.get(
                    "recommended_precedents",
                    []
                )
            )

        # -------------------------------------------------
        # STRATEGY
        # -------------------------------------------------

        if isinstance(
            litigation_strategy_data,
            dict
        ):

            result[
                "strategy"
            ] = (

                litigation_strategy_data.get(
                    "recommended_strategy",
                    ""
                )
            )

        # -------------------------------------------------
        # ARGUMENTS
        # -------------------------------------------------

        if isinstance(
            ai_argument_data,
            dict
        ):

            result[
                "arguments"
            ] = (

                ai_argument_data.get(
                    "arguments",
                    []
                )
            )

        # -------------------------------------------------
        # OUTCOME
        # -------------------------------------------------

        if isinstance(
            judgment_outcome_data,
            dict
        ):

            result[
                "predicted_outcome"
            ] = (

                judgment_outcome_data.get(
                    "predicted_outcome",
                    ""
                )
            )

        # -------------------------------------------------
        # RISKS
        # -------------------------------------------------

        if isinstance(
            contradiction_risk_data,
            dict
        ):

            result[
                "identified_risks"
            ] = (

                contradiction_risk_data.get(
                    "identified_risks",
                    []
                )
            )

        # -------------------------------------------------
        # DRAFTING
        # -------------------------------------------------

        if isinstance(
            legal_draft_data,
            dict
        ):

            result[
                "drafting_support"
            ] = legal_draft_data

        # -------------------------------------------------
        # COPILOT SUMMARY
        # -------------------------------------------------

        summary = []

        summary.append(
            f"Dominant Issue: {result['dominant_issue']}"
        )

        if result["strategy"]:

            summary.append(
                f"Strategy: {result['strategy']}"
            )

        if result["predicted_outcome"]:

            summary.append(
                f"Likely Outcome: {result['predicted_outcome']}"
            )

        if result["identified_risks"]:

            summary.append(
                f"Risks: {', '.join(result['identified_risks'])}"
            )

        result[
            "copilot_summary"
        ] = " | ".join(summary)

        # -------------------------------------------------
        # CONFIDENCE
        # -------------------------------------------------

        confidence = 70

        confidence += len(
            result["arguments"]
        ) * 2

        confidence += len(
            result["recommended_precedents"]
        ) * 2

        result[
            "confidence"
        ] = min(
            95,
            confidence
        )

        print(
            "✅ AI Legal Copilot Response:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Legal Copilot Error:",
            str(e)
        )

        return {

            "dominant_issue":
                "General",

            "recommended_precedents":
                [],

            "strategy":
                "",

            "arguments":
                [],

            "predicted_outcome":
                "",

            "identified_risks":
                [],

            "drafting_support":
                {},

            "copilot_summary":
                "",

            "confidence":
                0
        }
