# =========================================================
# 🔥 DOMINANT ISSUE ENGINE
# =========================================================


DOMINANT_ISSUE_MAP = {

    # -----------------------------------------------------
    # HOMICIDE
    # -----------------------------------------------------

    frozenset(["302"]):
        "Homicide",

    frozenset(["302", "34"]):
        "Homicide",

    frozenset(["302", "120B"]):
        "Homicide Conspiracy",

    frozenset(["307"]):
        "Attempt to Murder",

    # -----------------------------------------------------
    # FRAUD
    # -----------------------------------------------------

    frozenset(["420"]):
        "Fraud",

    frozenset(["420", "120B"]):
        "Fraud Conspiracy",

    frozenset(["406", "420"]):
        "Fraud and Breach of Trust",

    # -----------------------------------------------------
    # MATRIMONIAL
    # -----------------------------------------------------

    frozenset(["498A"]):
        "Cruelty Against Married Woman",

    frozenset(["498A", "304B"]):
        "Dowry Death",

    # -----------------------------------------------------
    # SEXUAL OFFENCES
    # -----------------------------------------------------

    frozenset(["376"]):
        "Sexual Offence",

    frozenset(["376", "506"]):
        "Sexual Offence with Intimidation",

    # -----------------------------------------------------
    # NI ACT
    # -----------------------------------------------------

    frozenset(["138"]):
        "Cheque Dishonour",

    frozenset(["138", "141"]):
        "Corporate Cheque Dishonour",

    # -----------------------------------------------------
    # CrPC
    # -----------------------------------------------------

    frozenset(["482"]):
        "FIR Quashing",

    frozenset(["438"]):
        "Anticipatory Bail",

    # -----------------------------------------------------
    # CONSTITUTION
    # -----------------------------------------------------

    frozenset(["226"]):
        "Writ Jurisdiction",
}


# =========================================================
# 🔥 SEMANTIC ISSUE ONTOLOGY
# =========================================================

SEMANTIC_ISSUE_PATTERNS = {

    "Executive Clemency And Remission": [

        "article 161",

        "premature release",

        "remission",

        "executive clemency",

        "life convict",

        "prison rules",

        "rule 591",

        "sentence remission",

        "release of prisoners",
    ],

    "Constitutional Writ Jurisdiction": [

        "article 32",

        "article 226",

        "writ petition",

        "constitutional remedy",

        "fundamental rights",
    ],

    "Quashing Of FIR": [

        "section 482",

        "quash fir",

        "criminal proceedings quashed",

        "charge sheet quashed",
    ],

    "Preventive Detention": [

        "preventive detention",

        "detention order",

        "habeas corpus",

        "national security act",
    ],

    "Service Reinstatement": [

        "reinstated in service",

        "departmental proceeding",

        "termination quashed",

        "dismissal quashed",
    ],

    "NDPS Bail": [

        "ndps",

        "commercial quantity",

        "section 37",

        "contraband",

        "bail application",
    ],
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
# 🔥 DOMINANT ISSUE DETECTOR
# =========================================================

def detect_dominant_issue(
    section_hierarchy,
    full_text="",
    citations=None,
    doctrines=None,
    acts=None,
):

    if not isinstance(section_hierarchy, list):

        section_hierarchy = []

    detected_sections = set()

    full_text = str(full_text).lower()

    citations = citations or []

    doctrines = doctrines or []

    acts = acts or []

    citation_text = " ".join(
        map(str, citations)
    ).lower()

    doctrine_text = " ".join(
        map(str, doctrines)
    ).lower()

    acts_text = " ".join(
        map(str, acts)
    ).lower()

    semantic_text = " ".join([

        full_text,

        citation_text,

        doctrine_text,

        acts_text,
    ])

    for item in section_hierarchy:

        if not isinstance(item, dict):

            continue

        section = normalize_section(
            item.get("section")
        )

        if section:

            detected_sections.add(section)

    best_issue = "General"

    best_score = 0

    for relation_key, issue_name in DOMINANT_ISSUE_MAP.items():

        if relation_key.issubset(detected_sections):

            score = len(relation_key) * 20

            if score > best_score:

                best_score = score

                best_issue = issue_name

    return {

        "dominant_issue":
            best_issue,

        "confidence":
            min(
                95,
                50 + best_score
            )
    }
