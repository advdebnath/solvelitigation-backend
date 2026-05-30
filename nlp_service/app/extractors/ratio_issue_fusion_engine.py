import re

# =========================================================
# 🔥 RATIO + DOMINANT ISSUE FUSION ENGINE
# =========================================================


def build_ratio_issue_fusion(
    dominant_issue=None,
    ratio_data=None,
    operative_data=None,
    section_relationships=None,
    semantic_issues=None,
):

    fusion = {
        "dominant_issue": "General",
        "ratio": None,
        "operative_holding": None,
        "section_relationships": [],
        "semantic_issues": [],
        "fusion_summary": None,
        "confidence": 0,
    }

    # -----------------------------------------------------
    # DOMINANT ISSUE
    # -----------------------------------------------------

    if isinstance(dominant_issue, dict):

        fusion["dominant_issue"] = dominant_issue.get("dominant_issue") or "General"

        fusion["confidence"] += dominant_issue.get("confidence", 0) * 0.20

    # -----------------------------------------------------
    # RATIO
    # -----------------------------------------------------

    if isinstance(ratio_data, dict):

        ratio_text = ratio_data.get("ratio") or ratio_data.get("summary")

        if ratio_text:

            fusion["ratio"] = ratio_text

            fusion["confidence"] += ratio_data.get("confidence", 0) * 0.30

    # -----------------------------------------------------
    # OPERATIVE HOLDING
    # -----------------------------------------------------

    if isinstance(operative_data, dict):

        holding = operative_data.get("final_holding") or operative_data.get(
            "final_disposition"
        )

        if holding:

            fusion["operative_holding"] = holding

            fusion["confidence"] += 20

    # -----------------------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------------------

    if isinstance(section_relationships, list):

        fusion["section_relationships"] = section_relationships

        fusion["confidence"] += min(20, len(section_relationships) * 5)

    # -----------------------------------------------------
    # SEMANTIC ISSUES
    # -----------------------------------------------------

    if isinstance(semantic_issues, list):

        fusion["semantic_issues"] = semantic_issues[:10]

        fusion["confidence"] += min(10, len(semantic_issues))

    # -----------------------------------------------------
    # FUSION SUMMARY
    # -----------------------------------------------------

    summary_parts = []

    if fusion["dominant_issue"]:

        summary_parts.append(fusion["dominant_issue"])

    if fusion["operative_holding"]:

        summary_parts.append(fusion["operative_holding"])

    if fusion["ratio"]:

        summary_parts.append(fusion["ratio"])

    fusion["fusion_summary"] = ". ".join(summary_parts)

    fusion["confidence"] = int(min(95, fusion["confidence"]))

    return fusion
