# =========================================================
# 🔥 HEADNOTE JURISPRUDENTIAL COGNITION ENGINE
# =========================================================

import re

# =========================================================
# 🔥 HEADNOTE SEMANTIC ONTOLOGY
# =========================================================

HEADNOTE_POINT_PATTERNS = {
    "Article 32 Remedy": [
        r"article\s+32",
        r"constitutional remedy",
        r"writ jurisdiction",
    ],
    "Fundamental Rights Enforcement": [
        r"fundamental rights",
        r"article\s+14",
        r"article\s+21",
        r"constitutional protection",
    ],
    "Natural Justice": [r"natural justice", r"fair hearing", r"audi alteram partem"],
    "Judicial Review": [r"judicial review", r"constitutional validity", r"ultra vires"],
    "Reinstatement In Service": [
        r"reinstatement",
        r"continuity of service",
        r"back wages",
    ],
    "Departmental Proceeding": [
        r"departmental proceeding",
        r"disciplinary authority",
        r"misconduct",
    ],
    "FIR Quashing": [
        r"quashing of fir",
        r"section\s+482",
        r"criminal proceedings quashed",
    ],
    "NDPS Recovery": [r"ndps", r"contraband", r"commercial quantity"],
    "GST Input Tax Credit": [r"input tax credit", r"gst", r"itc"],
    "Reassessment": [r"reassessment", r"escaped assessment"],
}

# =========================================================
# 🔥 JURISPRUDENTIAL HIERARCHY ENGINE
# =========================================================


def build_headnote_jurisprudence(
    headnote_data,
    issue_data=None,
    operative_data=None,
    sections_data=None,
    dominant_issue=None,
):

    result = {
        "primary": [],
        "constitutional": [],
        "procedural": [],
        "criminal": [],
        "service": [],
        "taxation": [],
        "general": [],
    }

    if isinstance(headnote_data, dict):

        text = " ".join(str(v) for v in headnote_data.values())

    else:

        text = str(headnote_data)

    text = text.lower()

    for point, patterns in HEADNOTE_POINT_PATTERNS.items():

        matched = False

        for pattern in patterns:

            if re.search(pattern, text, re.I):

                matched = True
                break

        if not matched:
            continue

        lowered = point.lower()

        if any(k in lowered for k in ["article", "constitutional", "judicial review"]):

            result["constitutional"].append(point)

        elif any(k in lowered for k in ["natural justice", "departmental"]):

            result["procedural"].append(point)

        elif any(k in lowered for k in ["fir", "ndps"]):

            result["criminal"].append(point)

        elif any(k in lowered for k in ["service", "reinstatement"]):

            result["service"].append(point)

        elif any(k in lowered for k in ["gst", "reassessment"]):

            result["taxation"].append(point)

        else:

            result["general"].append(point)

    # =====================================================
    # 🔥 SEMANTIC JURISPRUDENTIAL FUSION
    # =====================================================

    semantic_points = []

    try:

        if dominant_issue:

            if isinstance(dominant_issue, dict):

                dominant_issue_name = str(
                    dominant_issue.get("dominant_issue", "")
                ).strip()

            else:

                dominant_issue_name = str(dominant_issue).strip()

            if dominant_issue_name and dominant_issue_name.lower() != "general":

                semantic_points.append(dominant_issue_name)

        if issue_data:

            for issue in issue_data.get("issues", []):

                issue_name = str(issue.get("issue", "")).strip()

                if issue_name:

                    semantic_points.append(issue_name)

        if sections_data:

            for sec in sections_data.get("sections", []):

                section_number = str(sec.get("section", "")).strip()

                act_name = str(sec.get("act", "")).strip()

                if section_number == "32" and "Constitution" in act_name:

                    semantic_points.append("Article 32 Remedy")

                    semantic_points.append("Constitutional Remedy")

        if operative_data:

            holding = str(operative_data.get("final_holding", "")).lower()

            if "allowed" in holding:

                semantic_points.append("Relief Granted")

            elif "dismissed" in holding:

                semantic_points.append("Relief Denied")

    except Exception as e:

        print("❌ SEMANTIC FUSION ERROR:")

        print(str(e))

    all_points = []

    for values in result.values():

        all_points.extend(values)

    merged_points = all_points + semantic_points

    sanitized_points = []

    for item in merged_points:

        if isinstance(item, dict):

            value = str(item.get("dominant_issue", "")).strip()

        else:

            value = str(item).strip()

        if not value:
            continue

        if value.lower() == "general":
            continue

        if value.startswith("{"):
            continue

        sanitized_points.append(value)

    canonical_points = []

    for point in list(dict.fromkeys(sanitized_points))[:10]:

        point_lower = point.lower()

        category = "General"

        lineage = "GENERAL_JURISPRUDENCE"

        confidence = 70

        sources = ["semantic_fusion"]

        supporting_section = ""

        supporting_act = ""

        if "article 32" in point_lower:

            category = "Constitutional"

            lineage = "WRIT_JURISDICTION"

            confidence = 95

            supporting_section = "32"

            supporting_act = "Constitution Of India"

            sources.extend(["constitutional_section", "headnote"])

        elif "constitutional" in point_lower:

            category = "Constitutional"

            lineage = "CONSTITUTIONAL_REMEDY"

            confidence = 88

        elif "writ petition" in point_lower:

            category = "Constitutional"

            lineage = "WRIT_MAINTAINABILITY"

            confidence = 90

            sources.extend(["semantic_issue"])

        canonical_points.append(
            {
                "point": point,
                "category": category,
                "confidence": confidence,
                "sources": list(dict.fromkeys(sources)),
                "supporting_section": supporting_section,
                "supporting_act": supporting_act,
                "lineage": lineage,
            }
        )

    result["primary"] = canonical_points

    return result


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = """
    Article 32 remedy allowed.
    Violation of natural justice.
    Reinstatement in service directed.
    """

    print(build_headnote_jurisprudence(sample))
