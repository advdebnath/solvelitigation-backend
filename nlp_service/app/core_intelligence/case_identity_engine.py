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

from app.extractors.case_number_extractor import (
    extract_case_number as authoritative_extract_case_number
)


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
            "case_number": "Unknown Case",
            "value": "Unknown Case",
            "confidence": 0,
            "source": "case_identity_engine"
        }

    # =====================================================
    # 🔒 AUTHORITATIVE CASE NUMBER EXTRACTION
    # =====================================================

    extracted = authoritative_extract_case_number(
        text
    )

    extracted_case_number = extracted.get(
        "case_number",
        "Unknown Case"
    )

    confidence = extracted.get(
        "confidence",
        0
    )

    print("🔥 AUTHORITATIVE CASE NUMBER:")
    print(extracted)

    return {
        "case_number": extracted_case_number,
        "value": extracted_case_number,
        "confidence": confidence,
        "source": "case_identity_engine"
    }

# =========================================================
# 🔥 BUILD CANONICAL CASE OBJECT
# =========================================================

def build_canonical_case_object(full_text=""):

    case_number = extract_case_number(full_text)

    return {
        "canonical_case_id": case_number.get("case_number", "Unknown Case"),
        "case_number": case_number,
        "confidence": case_number.get("confidence", 0),
        "validation": {},
        "contradictions": []
    }

