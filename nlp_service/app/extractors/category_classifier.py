import re

# =====================================================
# 🔥 CATEGORY KEYWORDS
# =====================================================

CATEGORY_RULES = {
    "Criminal": [
        "ipc",
        "indian penal code",
        "crpc",
        "code of criminal procedure",
        "murder",
        "bail",
        "anticipatory bail",
        "acquittal",
        "conviction",
        "dowry death",
        "fir",
        "charge sheet",
        "criminal appeal",
        "ndps",
        "pocso",
        "prevention of corruption",
        "custody",
        "sentence",
        "prosecution",
        "accused",
    ],
    "Civil": [
        "specific performance",
        "breach of contract",
        "civil appeal",
        "injunction",
        "property dispute",
        "partition suit",
        "title suit",
        "agreement for sale",
        "civil procedure code",
        "cpc",
        "damages",
        "recovery suit",
        "arbitration",
        "contract act",
        "transfer of property",
        "easement",
    ],
    "Service Law": [
        "departmental proceeding",
        "termination",
        "reinstatement",
        "disciplinary authority",
        "suspension",
        "government servant",
        "promotion",
        "service matter",
        "compulsory retirement",
        "misconduct",
        "departmental enquiry",
        "service tribunal",
    ],
    "Taxation & Corporate": [
        "income tax",
        "gst",
        "goods and services tax",
        "assessment order",
        "tax liability",
        "vat",
        "excise duty",
        "service tax",
        "customs duty",
        "input tax credit",
        "companies act",
        "shareholder",
        "company petition",
        "oppression and mismanagement",
        "nclt",
        "insolvency",
        "ibc",
        "corporate debtor",
        "liquidation",
        "board resolution",
    ],
    "Constitutional": [
        "article 14",
        "article 19",
        "article 21",
        "constitution of india",
        "fundamental rights",
        "constitutional validity",
        "writ petition",
        "habeas corpus",
        "mandamus",
        "certiorari",
    ],
}
# =====================================================
# 🔥 ACT → CATEGORY MAP (CATEGORY ENGINE V2)
# =====================================================

ACT_CATEGORY_MAP = {

    # -----------------------------------------
    # CRIMINAL
    # -----------------------------------------

    "INDIAN PENAL CODE": "Criminal",
    "IPC": "Criminal",
    "CODE OF CRIMINAL PROCEDURE": "Criminal",
    "CRIMINAL PROCEDURE CODE": "Criminal",
    "CRPC": "Criminal",
    "NDPS ACT": "Criminal",
    "PREVENTION OF CORRUPTION ACT": "Criminal",

    # -----------------------------------------
    # CIVIL
    # -----------------------------------------

    "CODE OF CIVIL PROCEDURE": "Civil",
    "CPC": "Civil",
    "SPECIFIC RELIEF ACT": "Civil",
    "TRANSFER OF PROPERTY ACT": "Civil",
    "HINDU MARRIAGE ACT": "Civil",
    "ARBITRATION AND CONCILIATION ACT": "Civil",

    # -----------------------------------------
    # CONSTITUTIONAL
    # -----------------------------------------

    "CONSTITUTION OF INDIA": "Constitutional",

    # -----------------------------------------
    # TAXATION
    # -----------------------------------------

    "INCOME TAX ACT": "Taxation & Corporate",
    "GST ACT": "Taxation & Corporate",
    "CGST ACT": "Taxation & Corporate",
    "CUSTOMS ACT": "Taxation & Corporate",

    # -----------------------------------------
    # SERVICE
    # -----------------------------------------

    "ADMINISTRATIVE TRIBUNALS ACT": "Service Law",
}


# =====================================================
# 🔥 NORMALIZE
# =====================================================


def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text


# =====================================================
# 🔥 JURISDICTION ENGINE
# =====================================================


def detect_jurisdiction_category(text: str):

    upper_text = text.upper()

    # ==============================================
    # CRIMINAL
    # ==============================================

    if (
        "CRIMINAL APPEAL" in upper_text
        or "CRIMINAL ORIGINAL JURISDICTION" in upper_text
        or "CRIMINAL REVISION" in upper_text
    ):

        return "Criminal"

    # ==============================================
    # CIVIL
    # ==============================================

    if (
        "CIVIL APPEAL" in upper_text
        or "CIVIL ORIGINAL JURISDICTION" in upper_text
        or "CIVIL REVISION" in upper_text
    ):

        return "Civil"

    # ==============================================
    # SERVICE
    # ==============================================

    if (
        "SERVICE MATTER" in upper_text
        or "CENTRAL ADMINISTRATIVE TRIBUNAL" in upper_text
        or "DISCIPLINARY AUTHORITY" in upper_text
    ):

        return "Service Law"

    # ==============================================
    # TAXATION / CORPORATE
    # ==============================================

    if (
        "GST" in upper_text
        or "INCOME TAX" in upper_text
        or "COMPANIES ACT" in upper_text
        or "NCLT" in upper_text
    ):

        return "Taxation & Corporate"

    return None


# =====================================================
# 🔥 DYNAMIC CONSTITUTIONAL OVERLAY ENGINE
# =====================================================

def detect_constitutional_overlay(text):

    if not text:
        return {
            "secondary_categories": [],
            "constitutional_articles": []
        }

    upper_text = text.upper()

    constitutional_articles = sorted(
        list(
            set(
                re.findall(
                    r"ARTICLE\s+(\d+[A-Z]?)",
                    upper_text
                )
            )
        )
    )

    constitutional_articles = [
        f"Article {article}"
        for article in constitutional_articles
    ]

    constitutional_score = 0

    constitutional_score += len(
        constitutional_articles
    ) * 5

    constitutional_terms = [
        "CONSTITUTION OF INDIA",
        "FUNDAMENTAL RIGHTS",
        "BASIC STRUCTURE",
        "JUDICIAL REVIEW",
        "CONSTITUTIONAL VALIDITY",
        "EQUALITY BEFORE LAW",
        "RULE OF LAW",
        "WRIT JURISDICTION",
        "HABEAS CORPUS",
        "MANDAMUS",
        "CERTIORARI",
        "QUO WARRANTO",
        "PROHIBITION",
    ]

    for term in constitutional_terms:

        if term in upper_text:

            constitutional_score += 10

    overlays = []

    if constitutional_score >= 10:

        overlays.append("Constitutional")

    return {
        "secondary_categories": overlays,
        "constitutional_articles":
            constitutional_articles
    }


# =====================================================
# 🔥 CLASSIFY CATEGORY
# =====================================================


def classify_category(text: str):

    try:

        if not text:

            return "Unknown"

        # ==========================================
        # 🔥 JURISDICTION FIRST
        # ==========================================

        jurisdiction_category = detect_jurisdiction_category(text[:10000])

        if jurisdiction_category:

            print("✅ Jurisdiction category:", jurisdiction_category)

            return jurisdiction_category

        # ==========================================
        # 🔥 NORMALIZE
        # ==========================================

        text = normalize_text(text[:50000])

        scores = {}

        # ==========================================
        # 🔥 SCORE KEYWORDS
        # ==========================================

        for category, keywords in CATEGORY_RULES.items():

            score = 0

            for keyword in keywords:

                if keyword in text:

                    score += 1

            scores[category] = score

        # ==========================================
        # 🔥 ACT → CATEGORY BOOST
        # ==========================================

        upper_text = text.upper()

        for act_name, category in ACT_CATEGORY_MAP.items():

            if act_name in upper_text:

                scores[category] = (
                    scores.get(category, 0) + 20
                )

        # ==========================================
        # 🔥 BEST CATEGORY
        # ==========================================

        best_category = max(scores, key=scores.get)

        best_score = scores[best_category]

        # ==========================================
        # 🔥 NO MATCH
        # ==========================================

        if best_score == 0:

            # ==========================================
            # 🔥 LEGACY CAPTION RESCUE
            # ==========================================

            if "COMMISSIONER OF INCOME-TAX" in upper_text:
                return "Taxation & Corporate"

            if "COMMISSIONER OF INCOME TAX" in upper_text:
                return "Taxation & Corporate"

            if "CENTRAL BUREAU OF INVESTIGATION" in upper_text:
                return "Criminal"

            if "APPEAL (CRL" in upper_text:
                return "Criminal"

            if "BOARD OF EDUCATION" in upper_text:
                return "Service Law"

            if "RAILWAY MANAGER" in upper_text:
                return "Service Law"

            return "Unknown"


        print("✅ Keyword category:", best_category, scores)

        return best_category

    except Exception as e:

        print("❌ CATEGORY CLASSIFICATION ERROR:", e)

        return "Unknown"
