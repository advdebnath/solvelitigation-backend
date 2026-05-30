# =========================================================
# 🔥 SEMANTIC PRECEDENT RECOMMENDATION ENGINE
# =========================================================


PRECEDENT_MAP = {
    "FIR Quashing": [
        "Gian Singh v. State of Punjab",
        "Narinder Singh v. State of Punjab",
    ],
    "Privacy Doctrine": ["K.S. Puttaswamy v. Union of India"],
    "Liberty Oriented Bail Jurisprudence": ["Satender Kumar Antil v. CBI"],
    "Natural Justice Expansion": ["Maneka Gandhi v. Union of India"],
    "Minimal Arbitration Interference": ["Associate Builders v. DDA"],
    "Cheque Dishonour": ["Rangappa v. Sri Mohan"],
    "Dowry Death": ["Kans Raj v. State of Punjab"],
    "Premature Release Of Life Convicts": [
        "Laxman Naskar v. Union of India",
        "State of Haryana v. Jagdish",
        "Maru Ram v. Union of India",
    ],
    "Homicide": ["Sharad Birdhichand Sarda v. State of Maharashtra"],
}


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def recommend_semantic_precedents(
    dominant_issue=None,
    temporal_data=None,
    ratio_issue_fusion=None,
    judge_behaviour_data=None,
):

    try:

        recommendations = {
            "recommended_precedents": [],
            "dominant_issue": "General",
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

        # -------------------------------------------------
        # FUSION FALLBACK
        # -------------------------------------------------

        if not issue:

            if isinstance(ratio_issue_fusion, dict):

                issue = ratio_issue_fusion.get("dominant_issue")

        if not issue:

            return recommendations

        recommendations["dominant_issue"] = issue

        precedent_list = PRECEDENT_MAP.get(issue, [])

        for precedent in precedent_list:

            recommendations["recommended_precedents"].append(
                {"precedent": precedent, "reason": f"Semantically connected to {issue}"}
            )

        recommendations["confidence"] = min(95, 50 + len(precedent_list) * 10)

        # -------------------------------------------------
        # TEMPORAL BOOST
        # -------------------------------------------------

        if isinstance(temporal_data, dict):

            dominant_doctrine = temporal_data.get("dominant_doctrine", "")

            recommendations["dominant_doctrine"] = dominant_doctrine

        # -------------------------------------------------
        # BEHAVIOURAL BOOST
        # -------------------------------------------------

        if isinstance(judge_behaviour_data, dict):

            recommendations["judge_behaviour"] = judge_behaviour_data.get(
                "dominant_behaviour", "Neutral"
            )

        print("✅ Semantic Precedent Recommendations:")

        print(recommendations)

        return recommendations

    except Exception as e:

        print("❌ Semantic Recommendation Error:", str(e))

        return {
            "recommended_precedents": [],
            "dominant_issue": "General",
            "confidence": 0,
        }
