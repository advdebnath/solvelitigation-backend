# =========================================================
# 🔥 SHARED JUDICIAL UTILITIES
# =========================================================

import re


def normalize_ocr(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(r"\s+", " ", text)

    text = text.replace("\n", " ")

    text = text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

    # =====================================================
    # 🔥 UNIVERSAL LEGAL OCR NORMALIZATION
    # =====================================================

    OCR_REPAIRS = [
        (r"\bNO\s+N\s+S\s*\.?", "NOS."),
        (r"\bNO\s+S\s*\.?", "NOS."),
        (r"\bNO\s*\(\s*S\s*\)\.?\b", "NOS."),
        (r"\bNO\s*\(S\)\.?\b", "NOS."),

        (r"\bC\s*R\s*L\b", "CRL"),
        (r"\bW\s*P\b", "WP"),
        (r"\bS\s*L\s*P\b", "SLP"),
        (r"\bT\s*P\b", "TP"),

        (r"\bA\s*P\s*P\s*E\s*A\s*L\b", "APPEAL"),
        (r"\bP\s*E\s*T\s*I\s*T\s*I\s*O\s*N\b", "PETITION"),
        (r"\bJ\s*U\s*R\s*I\s*S\s*D\s*I\s*C\s*T\s*I\s*O\s*N\b", "JURISDICTION"),
    ]

    for pattern, replacement in OCR_REPAIRS:
        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.I
        )

    # =====================================================
    # 🔥 UNIVERSAL LEGAL OCR NORMALIZATION
    # =====================================================

    OCR_REPAIRS = [

        # NO(S) variants
        (r"\bNO\s+N\s+S\s*\.?", "NOS."),
        (r"\bNO\s+S\s*\.?", "NOS."),
        (r"\bNO\s*\(\s*S\s*\)\.?\b", "NOS."),
        (r"\bNO\s*\(S\)\.?\b", "NOS."),

        # OCR punctuation variants
        (r"NO\s*\.\s*S\b", "NOS."),

        # Common legal abbreviations
        (r"\bC\s*R\s*L\s*\.\s*\b", "CRL."),
        (r"\bI\s*A\s*\.\s*\b", "IA."),
        (r"\bM\s*A\s*\.\s*\b", "MA."),
        (r"\bS\s*L\s*P\s*\.\s*\b", "SLP."),
        (r"\bW\s*P\s*\.\s*\b", "WP."),
        (r"\bT\s*P\s*\.\s*\b", "TP."),
    ]

    for pattern, replacement in OCR_REPAIRS:

        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.I
        )

    return text.strip()


def clean_case_number(value):

    if not value:
        return ""

    value = str(value)

    value = re.sub(r"\s+", " ", value)

    value = re.sub(r"\s*/\s*", "/", value)

    value = value.strip(" .,:;-")

    return value.strip()


def build_case_object(
    case_number="",
    court_type="UNKNOWN",
    case_type="UNKNOWN",
    confidence=0,
    source="UNKNOWN",
):

    normalized = clean_case_number(case_number).upper()

    year_match = re.search(r"(19|20)\d{2}", normalized)

    return {
        "case_number": normalized,
        "normalized_case_number": normalized,
        "court_type": court_type,
        "case_type": case_type,
        "jurisdiction": "INDIA",
        "year": (year_match.group(0) if year_match else None),
        "confidence": confidence,
        "source": source,
        "validation_passed": True,
    }
