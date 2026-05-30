# =========================================================
# 🔥 SECTION-ACT RESOLUTION ENGINE
# =========================================================
#
# PURPOSE:
# Canonical section-to-act resolution.
#
# RESPONSIBILITIES:
# - Resolve legal sections correctly
# - Prevent impossible mappings
# - Deduplicate section mappings
# - Confidence scoring
#
# =========================================================

import re

# =========================================================
# 🔥 MASTER SECTION ONTOLOGY
# =========================================================

SECTION_ACT_ONTOLOGY = {
    "Indian Penal Code, 1860": {
        "302",
        "304B",
        "307",
        "376",
        "409",
        "420",
        "34",
        "120B",
        "161",
        "21",
    },
    "Code Of Criminal Procedure, 1973": {
        "154",
        "156",
        "161",
        "164",
        "173",
        "190",
        "438",
        "439",
        "482",
    },
    "Constitution Of India": {"14", "19", "21", "32", "136", "226"},
}

# =========================================================
# 🔥 SECTION CO-REFERENCE INFERENCE ENGINE
# =========================================================

SECTION_INFERENCE_MAP = {
    "302": "Indian Penal Code, 1860",
    "304B": "Indian Penal Code, 1860",
    "307": "Indian Penal Code, 1860",
    "376": "Indian Penal Code, 1860",
    "420": "Indian Penal Code, 1860",
    "34": "Indian Penal Code, 1860",
    "120B": "Indian Penal Code, 1860",
    "154": "Code Of Criminal Procedure, 1973",
    "161": "Code Of Criminal Procedure, 1973",
    "164": "Code Of Criminal Procedure, 1973",
    "173": "Code Of Criminal Procedure, 1973",
    "438": "Code Of Criminal Procedure, 1973",
    "439": "Code Of Criminal Procedure, 1973",
    "482": "Code Of Criminal Procedure, 1973",
    "14": "Constitution Of India",
    "19": "Constitution Of India",
    "21": "Constitution Of India",
    "32": "Constitution Of India",
    "136": "Constitution Of India",
    "226": "Constitution Of India",
}


# =========================================================
# 🔥 NORMALIZE ACT NAME
# =========================================================


def normalize_act_name(act_name=""):

    if not act_name:
        return ""

    return re.sub(r"\\s+", " ", str(act_name)).strip()


# =========================================================
# 🔥 RESOLVE SECTION ACT
# =========================================================


def resolve_section_act_relationship(sections=None):

    if sections is None:
        sections = []

    resolved = []
    seen = set()

    for item in sections:

        if not isinstance(item, dict):
            continue

        section = str(item.get("section", "")).strip()

        act = normalize_act_name(item.get("act", ""))

        # -------------------------------------------------
        # 🔥 ACT CO-REFERENCE INFERENCE ENGINE
        # -------------------------------------------------

        if section and not act:

            inferred_act = SECTION_INFERENCE_MAP.get(section)

            if inferred_act:

                act = inferred_act

                print("✅ INFERRED ACT FROM SECTION:")
                print({"section": section, "act": act})

        if not section or not act:
            continue

        valid_sections = SECTION_ACT_ONTOLOGY.get(act, set())

        # -------------------------------------------------
        # 🔥 VALIDATE SECTION BELONGS TO ACT
        # -------------------------------------------------

        if section not in valid_sections:

            print("❌ INVALID SECTION-ACT MAPPING:")
            print({"section": section, "act": act})

            continue

        key = (section, act)

        # -------------------------------------------------
        # 🔥 DEDUPLICATION
        # -------------------------------------------------

        if key in seen:
            continue

        seen.add(key)

        resolved.append(
            {
                "section": section,
                "act": act,
                "confidence": 95,
                "source": "section_act_resolution_engine",
            }
        )

    print("✅ RESOLVED SECTION-ACT RELATIONSHIPS:")
    print(resolved)

    return resolved
