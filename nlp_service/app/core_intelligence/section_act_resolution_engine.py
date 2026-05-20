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
        "21"
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
        "482"
    },

    "Constitution Of India": {
        "14",
        "19",
        "21",
        "32",
        "136",
        "226"
    }
}

# =========================================================
# 🔥 NORMALIZE ACT NAME
# =========================================================

def normalize_act_name(act_name=""):

    if not act_name:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(act_name)
    ).strip()

# =========================================================
# 🔥 RESOLVE SECTION ACT
# =========================================================

def resolve_section_act_relationship(
    sections=None
):

    if sections is None:
        sections = []

    resolved = []
    seen = set()

    for item in sections:

        if not isinstance(item, dict):
            continue

        section = str(
            item.get("section", "")
        ).strip()

        act = normalize_act_name(
            item.get("act", "")
        )

        if not section or not act:
            continue

        valid_sections = SECTION_ACT_ONTOLOGY.get(
            act,
            set()
        )

        # -------------------------------------------------
        # 🔥 VALIDATE SECTION BELONGS TO ACT
        # -------------------------------------------------

        if section not in valid_sections:

            print("❌ INVALID SECTION-ACT MAPPING:")
            print({
                "section": section,
                "act": act
            })

            continue

        key = (
            section,
            act
        )

        # -------------------------------------------------
        # 🔥 DEDUPLICATION
        # -------------------------------------------------

        if key in seen:
            continue

        seen.add(key)

        resolved.append({
            "section": section,
            "act": act,
            "confidence": 95,
            "source": "section_act_resolution_engine"
        })

    print("✅ RESOLVED SECTION-ACT RELATIONSHIPS:")
    print(resolved)

    return resolved

