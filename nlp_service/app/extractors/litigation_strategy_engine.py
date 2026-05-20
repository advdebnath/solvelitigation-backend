# =========================================================
# 🔥 LITIGATION STRATEGY INTELLIGENCE ENGINE
# =========================================================


STRATEGY_MAP = {

    "FIR Quashing": {

        "strategy":
            "Emphasize settlement, abuse of process, and continuation of criminal proceedings being futile.",

        "arguments": [

            "Abuse of process",

            "Settlement between parties",

            "Ends of justice"
        ]
    },

    "Liberty Oriented Bail Jurisprudence": {

        "strategy":
            "Stress personal liberty, absence of custodial interrogation, and constitutional protections.",

        "arguments": [

            "Article 21",

            "Bail is the rule",

            "No custodial interrogation"
        ]
    },

    "Premature Release Of Life Convicts": {

        "strategy":
            "Stress remission jurisprudence, reformative justice, prison conduct, and constitutional clemency powers.",

        "arguments": [

            "Article 161 constitutional powers",

            "Reformative justice principles",

            "Good prison conduct",

            "Remission jurisprudence precedents"
        ]
    },

    "Minimal Arbitration Interference": {

        "strategy":
            "Highlight limited scope of judicial interference under Section 34.",

        "arguments": [

            "Judicial restraint",

            "Patent illegality threshold",

            "Minimal interference"
        ]
    },

    "Natural Justice Expansion": {

        "strategy":
            "Focus on procedural fairness and denial of fair hearing.",

        "arguments": [

            "Audi alteram partem",

            "Procedural fairness",

            "Reasoned order requirement"
        ]
    },

    "Cheque Dishonour": {

        "strategy":
            "Stress statutory presumptions and legally enforceable debt.",

        "arguments": [

            "Section 139 presumption",

            "Legally enforceable debt",

            "Burden shifts to accused"
        ]
    }
}


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================

def generate_litigation_strategy(

    dominant_issue=None,
    semantic_precedent_data=None,
    judge_behaviour_data=None,
    temporal_jurisprudence_data=None
):

    try:

        result = {

            "dominant_issue":
                "General",

            "recommended_strategy":
                "",

            "arguments":
                [],

            "recommended_precedents":
                [],

            "judge_behaviour":
                "Neutral",

            "confidence":
                0
        }

        issue = None

        # -------------------------------------------------
        # DOMINANT ISSUE
        # -------------------------------------------------

        if isinstance(dominant_issue, dict):

            issue = dominant_issue.get(
                "dominant_issue"
            )
        elif isinstance(dominant_issue, str):

            issue = dominant_issue.strip()


        if not issue:

            return result

        result[
            "dominant_issue"
        ] = issue

        # -------------------------------------------------
        # STRATEGY LOOKUP
        # -------------------------------------------------

        strategy_data = STRATEGY_MAP.get(
            issue,
            {}
        )

        result[
            "recommended_strategy"
        ] = strategy_data.get(
            "strategy",
            ""
        )

        result[
            "arguments"
        ] = strategy_data.get(
            "arguments",
            []
        )

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
        # JUDGE BEHAVIOUR
        # -------------------------------------------------

        if isinstance(
            judge_behaviour_data,
            dict
        ):

            result[
                "judge_behaviour"
            ] = (

                judge_behaviour_data.get(
                    "dominant_behaviour",
                    "Neutral"
                )
            )

        # -------------------------------------------------
        # TEMPORAL DOCTRINE
        # -------------------------------------------------

        if isinstance(
            temporal_jurisprudence_data,
            dict
        ):

            result[
                "dominant_doctrine"
            ] = (

                temporal_jurisprudence_data.get(
                    "dominant_doctrine",
                    "General"
                )
            )

        result[
            "confidence"
        ] = min(

            95,

            60 + len(
                result["arguments"]
            ) * 5
        )

        print(
            "✅ Litigation Strategy:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Litigation Strategy Error:",
            str(e)
        )

        return {

            "dominant_issue":
                "General",

            "recommended_strategy":
                "",

            "arguments":
                [],

            "recommended_precedents":
                [],

            "judge_behaviour":
                "Neutral",

            "confidence":
                0
        }
