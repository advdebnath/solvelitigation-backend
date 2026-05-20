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
# 🔥 BUILD REASONING CHAIN
# =========================================================

def build_reasoning_chain(

    issue_data=None,

    precedent_data=None,

    argument_data=None,

    ratio_data=None,

    outcome_data=None,

    judge_data=None
):

    chain = []

    # =====================================================
    # 🔥 ISSUE CLUSTERS
    # =====================================================

    if issue_data:

        dominant = issue_data.get(
            "dominant_issue"
        )

        if dominant:

            chain.append(

                f"Primary legal issue identified: {dominant}"
            )

    # =====================================================
    # 🔥 PRECEDENTS
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

            value = strongest.get(
                "precedent_value"
            )

            chain.append(

                f"Strong precedent support detected from {citation} ({value})"
            )

    # =====================================================
    # 🔥 ARGUMENTS
    # =====================================================

    if argument_data:

        arguments = argument_data.get(
            "arguments",
            []
        )

        for arg in arguments:

            if arg.get("status") == "Accepted":

                chain.append(

                    f"{arg.get('party')} argument accepted by court"
                )

    # =====================================================
    # 🔥 RATIO
    # =====================================================

    if ratio_data:

        ratios = ratio_data.get(
            "ratio_decidendi",
            []
        )

        if ratios:

            ratio = ratios[0]

            principles = ratio.get(
                "legal_principles",
                []
            )

            if principles:

                chain.append(

                    "Binding principles involved: "
                    +
                    ", ".join(principles[:3])
                )

    # =====================================================
    # 🔥 OUTCOME
    # =====================================================

    if outcome_data:

        predicted = outcome_data.get(
            "predicted_outcome"
        )

        if predicted:

            chain.append(

                f"Predicted litigation outcome: {predicted}"
            )

    # =====================================================
    # 🔥 JUDGE ANALYTICS
    # =====================================================

    if judge_data:

        tendency = judge_data.get(
            "primary_tendency"
        )

        if tendency:

            chain.append(

                f"Judicial tendency observed: {tendency}"
            )

    return chain


# =========================================================
# 🔥 GENERATE LEGAL ANALYSIS
# =========================================================

def generate_legal_analysis(

    issue_data=None,

    precedent_data=None,

    argument_data=None,

    ratio_data=None,

    outcome_data=None,

    judge_data=None
):

    try:

        chain = build_reasoning_chain(

            issue_data=issue_data,

            precedent_data=precedent_data,

            argument_data=argument_data,

            ratio_data=ratio_data,

            outcome_data=outcome_data,

            judge_data=judge_data
        )

        # =================================================
        # 🔥 SUMMARY
        # =================================================

        summary_parts = []

        dominant_issue = None

        if issue_data:

            dominant_issue = issue_data.get(
                "dominant_issue"
            )

        predicted = None

        if outcome_data:

            predicted = outcome_data.get(
                "predicted_outcome"
            )

        tendency = None

        if judge_data:

            tendency = judge_data.get(
                "primary_tendency"
            )

        # =================================================
        # 🔥 BUILD ANALYSIS
        # =================================================

        if dominant_issue:

            summary_parts.append(

                f"The dispute primarily concerns {dominant_issue.lower()}."
            )

        if predicted:

            summary_parts.append(

                f"The analytical model predicts that the likely outcome is: {predicted.lower()}."
            )

        if tendency:

            summary_parts.append(

                f"The judicial reasoning reflects a {tendency.lower()} approach."
            )

        # =================================================
        # 🔥 PRECEDENT SUPPORT
        # =================================================

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

                summary_parts.append(

                    f"Strong precedent reliance is visible from {citation}."
                )

        # =================================================
        # 🔥 FINAL ANALYSIS
        # =================================================

        analysis = " ".join(
            summary_parts
        )

        analysis = clean_text(
            analysis
        )

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {

            "legal_analysis":
                analysis,

            "reasoning_chain":
                chain,

            "confidence":
                95
        }

        print(
            "✅ Legal GPT Reasoning Generated:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Legal GPT Engine Error:",
            str(e)
        )

        return {

            "legal_analysis":
                "",

            "reasoning_chain": [],

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
                    "AIR 1967 SC 574",

                "precedent_value":
                    "Relied On"
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

    judge_data = {

        "primary_tendency":
            "Natural Justice Oriented"
    }

    print(

        generate_legal_analysis(

            issue_data=issue_data,

            precedent_data=precedent_data,

            argument_data=argument_data,

            ratio_data=ratio_data,

            outcome_data=outcome_data,

            judge_data=judge_data
        )
    )
