# =========================================================
# 🔥 SOLVELITIGATION CORE INTELLIGENCE ENGINE
# =========================================================
#
# ENGINE:
# CASE IDENTITY ENGINE
#
# PURPOSE:
# Canonical legal identity resolution.
#
# RESPONSIBILITIES:
# - Case Number Resolution
# - Court Resolution
# - Party Resolution
# - Judge Resolution
# - Judgment Date Resolution
# - Citation Identity
#
# AUTHORITATIVE OUTPUT:
# canonical_case_object
#
# =========================================================

import re

# =========================================================
# 🔥 CANONICAL CASE PATTERNS
# =========================================================

CASE_PATTERNS = [

    # -----------------------------------------------------
    # 🔥 CRIMINAL APPEALS
    # -----------------------------------------------------

    r"(CRIMINAL\s+APPEAL\s+NO\.?\s*[\w\-\/]+\s*OF\s*\d{4})",

    r"(CRIMINAL\s+APPEAL\s+NOS\.?\s*[\w\-\/,\s]+\s*OF\s*\d{4})",

    r"(CRL\.?A\.?\s*NO\.?\s*[\w\-\/]+)",

    # -----------------------------------------------------
    # 🔥 CIVIL APPEALS
    # -----------------------------------------------------

    r"(CIVIL\s+APPEAL\s+NO\.?\s*[\w\-\/]+\s*OF\s*\d{4})",

    r"(CIVIL\s+APPEAL\s+NOS\.?\s*[\w\-\/,\s]+\s*OF\s*\d{4})",


    # 🔥 SPECIAL LEAVE PETITIONS
    # -----------------------------------------------------

    r"(SPECIAL\s+LEAVE\s+PETITION\s*\(.*?\)\s*NO\.?\s*[\w\-\/]+\s*OF\s*\d{4})",

    r"(SLP\s*\(C\)\s*NO\.?\s*[\w\-\/]+)",

    r"(SLP\s*\(CRL\.?\)\s*NO\.?\s*[\w\-\/]+)",

    # -----------------------------------------------------
    # 🔥 WRIT PETITIONS
    # -----------------------------------------------------

    r"(WRIT\s+PETITION\s*\(.*?\)\s*NO\.?\s*[\w\-\/]+\s*OF\s*\d{4})",

    r"(W\.P\.\s*NO\.?\s*[\w\-\/]+)",

    # -----------------------------------------------------
    # 🔥 REVIEW PETITIONS
    # -----------------------------------------------------

    r"(REVIEW\s+PETITION\s*\(.*?\)\s*NO\.?\s*[\w\-\/]+)",

    # -----------------------------------------------------
    # 🔥 TRANSFER PETITIONS
    # -----------------------------------------------------

    r"(TRANSFER\s+PETITION\s*\(.*?\)\s*NO\.?\s*[\w\-\/]+)",

    # -----------------------------------------------------
    # 🔥 DIARY NUMBERS
    # -----------------------------------------------------

    r"(DIARY\s+NO\.?\s*[\w\-\/]+)",

    # -----------------------------------------------------
    # 🔥 MISC APPLICATIONS
    # -----------------------------------------------------

    r"(MISC\.?\s+APPLICATION\s+NO\.?\s*[\w\-\/]+)",
]


# =========================================================
# 🔥 EXTRACT CASE NUMBER
# =========================================================

def extract_case_number(text):

    if not text:
        return {
            "value": "Unknown Case",
            "confidence": 0,
            "source": "case_identity_engine"
        }

    header_text = text[:15000]

    header_text = re.sub(
        r"\s+",
        " ",
        header_text
    )

    header_text = re.sub(
        r"[^A-Za-z0-9\-\/\(\)\.,:\s]",
        " ",


        header_text
    )


    for pattern in CASE_PATTERNS:

        match = re.search(
            pattern,
            header_text,
            re.IGNORECASE
        )

        if match:

            print("✅ CASE NUMBER MATCH FOUND:")
            print(match.group(1))


            value = re.sub(
                r'\s+',
                ' ',
                match.group(1)
            ).strip().upper()

            return {
                "value": value,
                "confidence": 95,
                "source": "case_identity_engine"
            }

    return {
        "value": "Unknown Case",
        "confidence": 10,
        "source": "case_identity_engine"
    }

# =========================================================
# 🔥 BUILD CANONICAL CASE OBJECT
# =========================================================

def build_canonical_case_object(full_text=""):

    case_number = extract_case_number(full_text)

    return {
        "canonical_case_id": case_number.get("value"),
        "case_number": case_number,
        "confidence": case_number.get("confidence", 0),
        "validation": {},
        "contradictions": []
    }

