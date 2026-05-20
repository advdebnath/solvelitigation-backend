import re


# =========================================================
# 🔥 SECTION ROLE MAP
# =========================================================

SECTION_ROLE_MAP = {

    # -----------------------------------------------------
    # IPC
    # -----------------------------------------------------

    "302": "Murder",
    "304B": "Dowry Death",
    "307": "Attempt to Murder",
    "376": "Sexual Offence",
    "420": "Cheating/Fraud",
    "406": "Criminal Breach of Trust",
    "498A": "Cruelty Against Married Woman",
    "120B": "Criminal Conspiracy",
    "34": "Common Intention",
    "149": "Unlawful Assembly Liability",

    # -----------------------------------------------------
    # CrPC
    # -----------------------------------------------------

    "438": "Anticipatory Bail",
    "439": "Regular Bail",
    "482": "Inherent Powers",
    "125": "Maintenance",

    # -----------------------------------------------------
    # Constitution
    # -----------------------------------------------------

    "226": "Writ Jurisdiction",
    "32": "Constitutional Remedies",

    # -----------------------------------------------------
    # NI Act
    # -----------------------------------------------------

    "138": "Cheque Dishonour",
}


# =========================================================
# 🔥 ROLE CLASSIFIER
# =========================================================

def classify_section_role(section):

    if not section:

        return "General"

    cleaned = str(section).strip().upper()

    cleaned = re.sub(
        r"[^0-9A-Z]",
        "",
        cleaned
    )

    return SECTION_ROLE_MAP.get(
        cleaned,
        "General"
    )


# =========================================================
# 🔥 HIERARCHY BUILDER
# =========================================================

def build_section_hierarchy(sections):

    if not isinstance(sections, list):

        return []

    hierarchy = []

    seen = set()

    for item in sections:

        if not isinstance(item, dict):

            continue

        section = item.get("section")

        if not section:

            continue

        normalized = str(section).strip()

        if normalized in seen:

            continue

        seen.add(normalized)

        role = classify_section_role(
            normalized
        )

        hierarchy.append({

            "section":
                normalized,

            "act":
                item.get("act"),

            "role":
                role,

            "context_score":
                item.get(
                    "context_score",
                    0
                )
        })

    hierarchy = sorted(

        hierarchy,

        key=lambda x: x.get(
            "context_score",
            0
        ),

        reverse=True
    )

    return hierarchy
