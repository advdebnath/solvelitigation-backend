import re

# =========================================================
# 🔥 CRIMINAL ACTS
# =========================================================

CRIMINAL_ACTS = [
    "Indian Penal Code",
    "Bharatiya Nyaya Sanhita",
    "Code Of Criminal Procedure",
    "Bharatiya Nagarik Suraksha Sanhita",
    "NDPS",
    "POCSO",
    "Prevention Of Corruption",
    "Prevention Of Money Laundering",
    "National Investigation Agency",
    "Food Adulteration",
    "Evidence Act",
    "Juvenile Justice",
    "UAPA",
    "TADA",
    "MCOCA",
]

# =========================================================
# 🔥 SERVICE LAW
# =========================================================

SERVICE_KEYWORDS = [
    "departmental proceeding",
    "dismissal",
    "reinstatement",
    "suspension",
    "promotion",
    "service matter",
    "pension",
    "disciplinary authority",
    "termination",
    "compulsory retirement",
]

# =========================================================
# 🔥 TAXATION / CORPORATE
# =========================================================

TAX_ACTS = [
    "Income Tax",
    "GST",
    "Goods And Services Tax",
    "Customs",
    "Central Excise",
    "Companies Act",
    "SEBI",
    "Insolvency",
    "SARFAESI",
    "Negotiable Instruments",
]

# =========================================================
# 🔥 CIVIL
# =========================================================

CIVIL_ACTS = [
    "Contract Act",
    "Transfer Of Property",
    "Specific Relief",
    "Arbitration",
    "Civil Procedure Code",
    "Constitution Of India",
    "Consumer Protection",
    "Motor Vehicles",
    "Wakf Act",
]

# =========================================================
# 🔥 ACT BASED CATEGORY
# =========================================================


def infer_category_from_act(acts):

    if not acts:
        return "Unknown"

    joined = " ".join([str(a).lower() for a in acts])

    for act in CRIMINAL_ACTS:

        if act.lower() in joined:
            return "Criminal"

    for act in TAX_ACTS:

        if act.lower() in joined:
            return "Taxation & Corporate"

    for act in CIVIL_ACTS:

        if act.lower() in joined:
            return "Civil"

    return "Unknown"


# =========================================================
# 🔥 SECTION BASED CATEGORY
# =========================================================


def infer_category_from_sections(sections):

    if not sections:
        return "Unknown"

    joined = str(sections).lower()

    criminal_sections = [
        "302",
        "307",
        "376",
        "420",
        "498a",
        "138",
        "125",
        "409",
        "467",
        "468",
        "471",
    ]

    for sec in criminal_sections:

        if sec in joined:
            return "Criminal"

    return "Unknown"


# =========================================================
# 🔥 CASE NUMBER CATEGORY
# =========================================================


def infer_category_from_case_number(case_number):

    if not case_number:
        return "Unknown"

    text = str(case_number).lower()

    if "criminal" in text:
        return "Criminal"

    if "civil" in text:
        return "Civil"

    if "service" in text:
        return "Service"

    if "tax" in text:
        return "Taxation & Corporate"

    if "writ petition" in text:
        return "Civil"

    if "special leave petition" in text:
        return "Civil"

    return "Unknown"


# =========================================================
# 🔥 ONTOLOGY ELIGIBILITY
# =========================================================


def is_ontology_eligible(data):

    case_number = str(data.get("caseNumber", "")).strip()

    citations = data.get("citations", [])

    doctrines = data.get("doctrines", [])

    acts = data.get("acts", [])

    points_of_law = data.get("points_of_law", [])

    final_holding = str(data.get("final_holding", "")).strip()

    dominant_issue = str(data.get("dominant_issue", "General")).strip()

    invalid_patterns = [
        r"^ITEM",
        r"^NO\.",
        r"SUPREME COURT OF INDIA NOTICE",
        r"UNKNOWN CASE",
    ]

    semantic_signals = any(
        [
            citations,
            doctrines,
            acts,
            points_of_law,
            final_holding not in ["", "Disposition Unknown"],
            dominant_issue not in ["", "General", "Unknown"],
        ]
    )

    if semantic_signals:
        return True

    for pattern in invalid_patterns:

        if re.search(pattern, case_number, re.I):
            return False

    if case_number:
        return True

    return False


# =========================================================
# 🔥 SEMANTIC CATEGORY CONFIDENCE ENGINE
# =========================================================


def build_category_confidence(acts=None, sections=None, case_number=""):

    acts = acts or []
    sections = sections or []

    category_scores = {
        "Criminal": 0,
        "Civil": 0,
        "Service": 0,
        "Taxation & Corporate": 0,
    }

    category_signals = []

    # =====================================================
    # 🔥 ACT SIGNALS
    # =====================================================

    acts_joined = " ".join([str(a).lower() for a in acts])

    for act in CRIMINAL_ACTS:

        if act.lower() in acts_joined:

            category_scores["Criminal"] += 35

            category_signals.append(f"Criminal Act: {act}")

    for act in TAX_ACTS:

        if act.lower() in acts_joined:

            category_scores["Taxation & Corporate"] += 35

            category_signals.append(f"Tax Act: {act}")

    for act in CIVIL_ACTS:

        if act.lower() in acts_joined:

            category_scores["Civil"] += 30

            category_signals.append(f"Civil Act: {act}")

    # =====================================================
    # 🔥 SECTION SIGNALS
    # =====================================================

    section_text = str(sections).lower()

    criminal_sections = ["302", "307", "376", "420", "498a", "467", "468", "471"]

    for sec in criminal_sections:

        if sec in section_text:

            category_scores["Criminal"] += 20

            category_signals.append(f"Criminal Section: {sec}")

    # =====================================================
    # 🔥 CASE NUMBER SIGNALS
    # =====================================================

    case_text = str(case_number).lower()

    if "criminal" in case_text:

        category_scores["Criminal"] += 40

        category_signals.append("Case Number: Criminal")

    if "civil" in case_text:

        category_scores["Civil"] += 40

        category_signals.append("Case Number: Civil")

    if "service" in case_text:

        category_scores["Service"] += 40

        category_signals.append("Case Number: Service")

    if "tax" in case_text:

        category_scores["Taxation & Corporate"] += 40

        category_signals.append("Case Number: Tax")

    # =====================================================
    # 🔥 FINAL CATEGORY
    # =====================================================

    top_category = max(category_scores, key=category_scores.get)

    top_confidence = category_scores[top_category]

    if top_confidence < 40:

        top_category = "Unknown"

    return {
        "category": top_category,
        "confidence": top_confidence,
        "scores": category_scores,
        "signals": category_signals,
    }
