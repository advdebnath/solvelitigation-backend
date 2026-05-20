import re


# =========================================================
# 🔥 CLEAN
# =========================================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        str(text)
    )

    return text.strip()


# =========================================================
# 🔥 BUILD STRATEGY
# =========================================================

def build_strategy(

    issue_data=None,

    precedent_data=None,

    argument_data=None,

    ratio_data=None,

    outcome_data=None
):

    recommendations = []

    # =====================================================
    # 🔥 ISSUE STRATEGY
    # =====================================================

    if issue_data:

        dominant = issue_data.get(
            "dominant_issue"
        )

        if dominant:

            recommendations.append(

                f"Focus litigation strategy on {dominant.lower()}."
            )

    # =====================================================
    # 🔥 PRECEDENT STRATEGY
    # =====================================================

    if precedent_data:

        precedents = precedent_data.get(
            "ranked_precedents",
            []
        )

        if precedents:

            strongest = precedents[0]

            citation = strongest.get(
                "citation"
            )

            recommendations.append(

                f"Strong reliance may be placed on precedent: {citation}."
            )

    # =====================================================
    # 🔥 ACCEPTED ARGUMENTS
    # =====================================================

    if argument_data:

        arguments = argument_data.get(
            "arguments",
            []
        )

        for arg in arguments:

            if arg.get("status") == "Accepted":

                recommendations.append(

                    f"Emphasize accepted {arg.get('party').lower()} arguments."
                )

    # =====================================================
    # 🔥 RATIO PRINCIPLES
    # =====================================================

    if ratio_data:

        ratios = ratio_data.get(
            "ratio_decidendi",
            []
        )

        if ratios:

            principles = ratios[0].get(
                "legal_principles",
                []
            )

            if principles:

                recommendations.append(

                    "Highlight binding principles such as "
                    +
                    ", ".join(principles[:3])
                    +
                    "."
                )

    # =====================================================
    # 🔥 OUTCOME
    # =====================================================

    if outcome_data:

        outcome = outcome_data.get(
            "predicted_outcome"
        )

        if outcome:

            recommendations.append(

                f"Predicted litigation trend: {outcome}."
            )

    return recommendations


# =========================================================
# 🔥 GENERATE RECOMMENDATIONS
# =========================================================

def generate_legal_recommendations(

    issue_data=None,

    precedent_data=None,

    argument_data=None,

    ratio_data=None,

    outcome_data=None
):

    try:

        recommendations = build_strategy(

            issue_data=issue_data,

            precedent_data=precedent_data,

            argument_data=argument_data,

            ratio_data=ratio_data,

            outcome_data=outcome_data
        )

        # =================================================
        # 🔥 PRIMARY STRATEGY
        # =================================================

        primary = None

        if recommendations:

            primary = recommendations[0]

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {

            "primary_strategy":
                primary,

            "recommendations":
                recommendations,

            "confidence":
                95
        }

        print(
            "✅ Legal Recommendations Generated:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Recommendation Engine Error:",
            str(e)
        )

        return {

            "primary_strategy":
                "",

            "recommendations": [],

            "confidence":
                0
        }


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    issue_data = {

        "dominant_issue":
            "Wakf Property Dispute"
    }

    precedent_data = {

        "ranked_precedents": [

            {

                "citation":
                    "AIR 1967 SC 574"
            }
        ]
    }

    argument_data = {

        "arguments": [

            {

                "party":
                    "Petitioner",

                "status":
                    "Accepted"
            }
        ]
    }

    ratio_data = {

        "ratio_decidendi": [

            {

                "legal_principles":

                    [

                        "natural justice",

                        "wakf property"
                    ]
            }
        ]
    }

    outcome_data = {

        "predicted_outcome":
            "Appeal Likely Allowed"
    }

    print(

        generate_legal_recommendations(

            issue_data=issue_data,

            precedent_data=precedent_data,

            argument_data=argument_data,

            ratio_data=ratio_data,

            outcome_data=outcome_data
        )
    )
