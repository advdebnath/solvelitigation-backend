# =========================================================
# 🔥 JUDICIAL ROUTER
# =========================================================

from app.extractors.judicial.supreme_court_extractor import (
    extract_sc_case_number
)

from app.extractors.judicial.high_court_extractor import (
    extract_hc_case_number
)

from app.extractors.judicial.tribunal_extractor import (
    extract_tribunal_case_number
)


def extract_case_number_v2(text):

    upper = str(text).upper()

    # =====================================================
    # 🔥 SUPREME COURT ROUTING
    # =====================================================

    if "SUPREME COURT OF INDIA" in upper:

        print("🔥 ROUTED TO SUPREME COURT ENGINE 🔥")

        result = extract_sc_case_number(
            text
        )

        if result:
            return result

    elif "HIGH COURT" in upper:

        print("🔥 ROUTED TO HIGH COURT ENGINE 🔥")

        result = extract_hc_case_number(
            text
        )

        if result:
            return result

    elif (
        "TRIBUNAL" in upper
        or "NCLT" in upper
        or "NCLAT" in upper
        or "ITAT" in upper
        or "CAT" in upper
    ):

        print("🔥 ROUTED TO TRIBUNAL ENGINE 🔥")

        result = extract_tribunal_case_number(
            text
        )

        if result:
            return result

    return {

        "case_number": "Unknown Case",

        "normalized_case_number": "UNKNOWN CASE",

        "court_type": "UNKNOWN",

        "case_type": "UNKNOWN",

        "confidence": 0,

        "source": "JUDICIAL_ROUTER_V2",

        "validation_passed": False
    }
