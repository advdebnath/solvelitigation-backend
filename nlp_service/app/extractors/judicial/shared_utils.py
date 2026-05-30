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
