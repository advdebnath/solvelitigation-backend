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

        "accused"
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

        "easement"
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

        "service tribunal"
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

        "board resolution"
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

        "certiorari"
    ]
}

# =====================================================
# 🔥 NORMALIZE
# =====================================================

def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(

        r"\s+",

        " ",

        text
    )

    return text

# =====================================================
# 🔥 JURISDICTION ENGINE
# =====================================================

def detect_jurisdiction_category(

    text: str
):

    upper_text = text.upper()

    # ==============================================
    # CRIMINAL
    # ==============================================

    if (

        "CRIMINAL APPEAL"

        in upper_text

        or

        "CRIMINAL ORIGINAL JURISDICTION"

        in upper_text

        or

        "CRIMINAL REVISION"

        in upper_text
    ):

        return "Criminal"

    # ==============================================
    # CIVIL
    # ==============================================

    if (

        "CIVIL APPEAL"

        in upper_text

        or

        "CIVIL ORIGINAL JURISDICTION"

        in upper_text

        or

        "CIVIL REVISION"

        in upper_text
    ):

        return "Civil"

    # ==============================================
    # SERVICE
    # ==============================================

    if (

        "SERVICE MATTER"

        in upper_text

        or

        "CENTRAL ADMINISTRATIVE TRIBUNAL"

        in upper_text

        or

        "DISCIPLINARY AUTHORITY"

        in upper_text
    ):

        return "Service Law"

    # ==============================================
    # TAXATION / CORPORATE
    # ==============================================

    if (

        "GST"

        in upper_text

        or

        "INCOME TAX"

        in upper_text

        or

        "COMPANIES ACT"

        in upper_text

        or

        "NCLT"

        in upper_text
    ):

        return "Taxation & Corporate"

    return None

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

        jurisdiction_category = (

            detect_jurisdiction_category(
                text[:10000]
            )
        )

        if jurisdiction_category:

            print(

                "✅ Jurisdiction category:",

                jurisdiction_category
            )

            return jurisdiction_category

        # ==========================================
        # 🔥 NORMALIZE
        # ==========================================

        text = normalize_text(

            text[:50000]
        )

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
        # 🔥 BEST CATEGORY
        # ==========================================

        best_category = max(

            scores,

            key=scores.get
        )

        best_score = scores[
            best_category
        ]

        # ==========================================
        # 🔥 NO MATCH
        # ==========================================

        if best_score == 0:

            return "Unknown"

        print(

            "✅ Keyword category:",

            best_category,

            scores
        )

        return best_category

    except Exception as e:

        print(

            "❌ CATEGORY CLASSIFICATION ERROR:",

            e
        )

        return "Unknown"
