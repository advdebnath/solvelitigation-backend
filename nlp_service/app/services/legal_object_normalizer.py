# =========================================================
# 🔥 LEGAL OBJECT NORMALIZER (PRODUCTION SAFE)
# =========================================================

from copy import deepcopy

# =========================================================
# 🔥 SAFE HELPERS
# =========================================================

def ensure_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def ensure_dict(value):

    if isinstance(value, dict):
        return value

    return {}


def clean_string(value):

    if value is None:
        return ""

    return str(value).strip()


# =========================================================
# 🔥 DEDUPLICATION
# =========================================================

def unique_list(items):

    seen = set()

    output = []

    for item in items:

        key = str(item)

        if key in seen:
            continue

        seen.add(key)

        output.append(item)

    return output


# =========================================================
# 🔥 ACT NORMALIZATION
# =========================================================

def normalize_acts(acts):

    normalized = []

    for act in ensure_list(acts):

        # =================================================
        # 🔥 STRING
        # =================================================

        if isinstance(act, str):

            value = clean_string(act)

            if value:
                normalized.append(value)

        # =================================================
        # 🔥 DICT
        # =================================================

        elif isinstance(act, dict):

            value = (

                act.get("act_name")

                or act.get("act")

                or act.get("name")

                or act.get("title")
            )

            value = clean_string(value)

            if value:
                normalized.append(value)

    return sorted(unique_list(normalized))


# =========================================================
# 🔥 SECTION NORMALIZATION
# =========================================================

def normalize_sections(sections):

    normalized = []

    for s in ensure_list(sections):

        if not isinstance(s, dict):
            continue

        section_obj = {

            "type":
                clean_string(
                    s.get("type")
                ),

            "section":
                clean_string(
                    s.get("section")
                ),

            "act":
                clean_string(
                    s.get("act")
                )
        }

        if (
            section_obj["section"]
            or
            section_obj["act"]
        ):
            normalized.append(section_obj)

    return unique_list(normalized)


# =========================================================
# 🔥 POINTS OF LAW NORMALIZATION
# =========================================================

def normalize_points(points):

    normalized = []

    for p in ensure_list(points):

        # =================================================
        # 🔥 STRING
        # =================================================

        if isinstance(p, str):

            value = clean_string(p)

            if value:

                normalized.append({

                    "point": value,

                    "category": "Unknown"
                })

        # =================================================
        # 🔥 DICT
        # =================================================

        elif isinstance(p, dict):

            point_obj = {

                "point":
                    clean_string(
                        p.get("point")
                    ),

                "category":
                    clean_string(
                        p.get(
                            "category",
                            "Unknown"
                        )
                    ),

                "confidence":
                    p.get(
                        "confidence",
                        60
                    ),

                "sources":
                    ensure_list(
                        p.get(
                            "sources",
                            []
                        )
                    ),

                "supporting_section":
                    clean_string(
                        p.get(
                            "supporting_section"
                        )
                    ),

                "supporting_act":
                    clean_string(
                        p.get(
                            "supporting_act"
                        )
                    ),

                "lineage":
                    clean_string(
                        p.get(
                            "lineage"
                        )
                    )
            }

            if point_obj["point"]:

                normalized.append(point_obj)

    return unique_list(normalized)


# =========================================================
# 🔥 CITATION NORMALIZATION
# =========================================================

def normalize_citations(citations):

    normalized = []

    for c in ensure_list(citations):

        # =================================================
        # 🔥 STRING
        # =================================================

        if isinstance(c, str):

            value = clean_string(c)

            if value:

                normalized.append({

                    "citation": value
                })

        # =================================================
        # 🔥 DICT
        # =================================================

        elif isinstance(c, dict):

            citation_obj = {

                "citation":
                    clean_string(
                        c.get("citation")
                    ),

                "case":
                    clean_string(
                        c.get("case")
                    ),

                "court":
                    clean_string(
                        c.get("court")
                    )
            }

            if citation_obj["citation"]:

                normalized.append(citation_obj)

    return unique_list(normalized)


# =========================================================
# 🔥 JUDGE NORMALIZATION
# =========================================================

def normalize_judges(judges):

    normalized = []

    for j in ensure_list(judges):

        # =================================================
        # 🔥 STRING
        # =================================================

        if isinstance(j, str):

            value = clean_string(j)

            if value:

                normalized.append({

                    "name": value
                })

        # =================================================
        # 🔥 DICT
        # =================================================

        elif isinstance(j, dict):

            judge_obj = {

                "name":
                    clean_string(
                        j.get("name")
                    )
            }

            if judge_obj["name"]:

                normalized.append(judge_obj)

    return unique_list(normalized)


# =========================================================
# 🔥 SIMILAR CASES NORMALIZATION
# =========================================================

def normalize_similar_cases(similar_cases):

    normalized = []

    for s in ensure_list(similar_cases):

        if not isinstance(s, dict):
            continue

        case_obj = {

            "caseNumber":
                clean_string(
                    s.get("caseNumber")
                ),

            "score":
                s.get("score", 0),

            "category":
                clean_string(
                    s.get("category")
                )
        }

        if case_obj["caseNumber"]:

            normalized.append(case_obj)

    return unique_list(normalized)


# =========================================================
# 🔥 MAIN NORMALIZER
# =========================================================

def normalize_legal_objects(judgment_doc):

    doc = deepcopy(judgment_doc)

    # =====================================================
    # 🔥 ACTS
    # =====================================================

    doc["actNames"] = normalize_acts(
        doc.get("actNames", [])
    )

    # =====================================================
    # 🔥 SECTIONS
    # =====================================================

    doc["sections"] = normalize_sections(
        doc.get("sections", [])
    )

    # =====================================================
    # 🔥 POINTS OF LAW
    # =====================================================

    doc["pointsOfLaw"] = normalize_points(
        doc.get("pointsOfLaw", [])
    )

    # =====================================================
    # 🔥 CITATIONS
    # =====================================================

    doc["citations"] = normalize_citations(
        doc.get("citations", [])
    )

    # =====================================================
    # 🔥 JUDGES
    # =====================================================

    if isinstance(doc.get("judges"), dict):

        doc["judges"]["judges"] = normalize_judges(

            doc["judges"].get(
                "judges",
                []
            )
        )

    else:

        doc["judges"] = {

            "judges":
                normalize_judges(
                    doc.get("judges", [])
                )
        }

    # =====================================================
    # 🔥 SIMILAR CASES
    # =====================================================

    doc["similarCases"] = normalize_similar_cases(
        doc.get("similarCases", [])
    )

    # =====================================================
    # 🔥 DEBUG
    # =====================================================

    print("✅ Legal objects normalized")

    print({

        "actNames":
            doc.get("actNames"),

        "sections":
            len(
                doc.get("sections", [])
            ),

        "pointsOfLaw":
            len(
                doc.get("pointsOfLaw", [])
            ),

        "citations":
            len(
                doc.get("citations", [])
            )
    })

    return doc
