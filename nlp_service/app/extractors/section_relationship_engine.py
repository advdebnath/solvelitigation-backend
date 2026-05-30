# =========================================================
# 🔥 SECTION RELATIONSHIP ENGINE
# =========================================================


SECTION_RELATIONSHIPS = {
    # -----------------------------------------------------
    # IPC RELATIONSHIPS
    # -----------------------------------------------------
    frozenset(["302", "34"]): "Murder with Common Intention",
    frozenset(["302", "120B"]): "Murder Conspiracy",
    frozenset(["420", "120B"]): "Fraud Conspiracy",
    frozenset(["406", "420"]): "Fraud and Criminal Breach of Trust",
    frozenset(["498A", "304B"]): "Cruelty and Dowry Death",
    frozenset(["376", "506"]): "Sexual Offence with Criminal Intimidation",
    frozenset(["307", "34"]): "Attempt to Murder with Common Intention",
    # -----------------------------------------------------
    # CrPC
    # -----------------------------------------------------
    frozenset(["438", "482"]): "Anticipatory Bail with Inherent Powers",
    # -----------------------------------------------------
    # NI ACT
    # -----------------------------------------------------
    frozenset(["138", "141"]): "Corporate Cheque Dishonour Liability",
}


# =========================================================
# 🔥 NORMALIZER
# =========================================================


def normalize_section(value):

    if not value:

        return None

    cleaned = str(value).strip().upper()

    cleaned = cleaned.replace(" ", "")

    return cleaned


# =========================================================
# 🔥 RELATIONSHIP BUILDER
# =========================================================


def build_section_relationships(section_hierarchy):

    if not isinstance(section_hierarchy, list):

        return []

    sections = []

    for item in section_hierarchy:

        if not isinstance(item, dict):

            continue

        section = normalize_section(item.get("section"))

        if section:

            sections.append(section)

    relationships = []

    seen = set()

    for relation_key, meaning in SECTION_RELATIONSHIPS.items():

        if relation_key.issubset(set(sections)):

            key_tuple = tuple(sorted(relation_key))

            if key_tuple in seen:

                continue

            seen.add(key_tuple)

            relationships.append(
                {
                    "sections": list(sorted(relation_key)),
                    "relationship": meaning,
                    "confidence": 90,
                }
            )

    return relationships
