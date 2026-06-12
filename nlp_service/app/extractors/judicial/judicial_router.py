import re

# =========================================================
# 🔥 JUDICIAL ROUTER
# =========================================================

from app.extractors.judicial.high_court_extractor import extract_hc_case_number
from app.extractors.judicial.supreme_court_extractor import \
    extract_sc_case_number
from app.extractors.judicial.tribunal_extractor import \
    extract_tribunal_case_number


def extract_case_number_v2(text):

    upper = str(text).upper()

    header_text = upper[:5000]

    print("🔥 ROUTER INPUT SAMPLE START 🔥")
    print(upper[:2500])
    print("🔥 ROUTER INPUT SAMPLE END 🔥")

    print(
        "SC:",
        bool(
            re.search(
                r"SUPREME\s+COURT+T*\s+OF\s+INDIA",
                header_text,
                re.I
            )
        )
    )

    print(
        "HC:",
        bool(
            re.search(
                r"(HIGH COURT OF|IN THE HIGH COURT)",
                header_text,
                re.I
            )
        )
    )

    print(
        "TRIBUNAL:",
        bool(
            re.search(
                r"\b(TRIBUNAL|NCLT|NCLAT|ITAT|CAT)\b",
                header_text,
                re.I
            )
        )
    )
    # =====================================================
    # 🔥 SUPREME COURT ROUTING
    # =====================================================

    if re.search(
        r"SUPREME\s+COURT+T*\s+OF\s+INDIA",
        header_text,
        re.I
    ) or re.search(
        r"S\s*U\s*P\s*R\s*E\s*M\s*E\s*C\s*O\s*U\s*R\s*T\s*O\s*F\s*I\s*N\s*D\s*I\s*A",
        header_text,
        re.I
    ) or re.search(
        r"CIVIL\s+APPELLATE\s+JURISDICTION",
        header_text,
        re.I
    ) or re.search(
        r"CRIMINAL\s+APPELLATE\s+JURISDICTION",
        header_text,
        re.I
    ):

        print("🔥 ROUTED TO SUPREME COURT ENGINE 🔥")

        result = extract_sc_case_number(text)

        if result:
            return result


    elif re.search(
        r"(HIGH COURT OF|IN THE HIGH COURT)",
        header_text,
        re.I
    ):

        print("🔥 ROUTED TO HIGH COURT ENGINE 🔥")

        result = extract_hc_case_number(text)

        if result:
            return result

    elif re.search(
        r"\b(TRIBUNAL|NCLT|NCLAT|ITAT|CAT)\b",
        header_text,
        re.I
    ):

        print("🔥 ROUTED TO TRIBUNAL ENGINE 🔥")

        result = extract_tribunal_case_number(text)

        if result:
            return result

    return {
        "case_number": "Unknown Case",
        "normalized_case_number": "UNKNOWN CASE",
        "court_type": "UNKNOWN",
        "case_type": "UNKNOWN",
        "confidence": 0,
        "source": "JUDICIAL_ROUTER_V2",
        "validation_passed": False,
    }
