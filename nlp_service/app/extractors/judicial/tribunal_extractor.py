# =========================================================
# 🔥 TRIBUNAL EXTRACTOR
# =========================================================

import re

from app.extractors.judicial.shared_utils import (
    normalize_ocr,
    clean_case_number,
    build_case_object
)


TRIBUNAL_PATTERNS = [

    # =====================================================
    # 🔥 CENTRAL ADMINISTRATIVE TRIBUNAL
    # =====================================================

    (
        r'(OA\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "SERVICE"
    ),

    (
        r'(TA\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "SERVICE"
    ),

    # =====================================================
    # 🔥 NCLT / NCLAT
    # =====================================================

    (
        r'(CP\s*\(IB\)\s*NO\.?\s*[\d\/A-Z\-]+\s*OF\s*\d{4})',
        "INSOLVENCY"
    ),

    (
        r'(IA\s*\(IB\)\s*NO\.?\s*[\d\/A-Z\-]+\s*OF\s*\d{4})',
        "INSOLVENCY"
    ),

    (
        r'(COMPANY\s+PETITION\s+NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "COMPANY"
    ),

    # =====================================================
    # 🔥 ITAT
    # =====================================================

    (
        r'(ITA\s*NO\.?\s*[\d\/A-Z\-]+\s*OF\s*\d{4})',
        "TAX"
    ),

    # =====================================================
    # 🔥 GST
    # =====================================================

    (
        r'(GST\s+APPEAL\s+NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "GST"
    )
]


def extract_tribunal_case_number(text):

    text = normalize_ocr(text)

    upper = text.upper()

    for pattern, case_type in TRIBUNAL_PATTERNS:

        try:

            matches = re.findall(
                pattern,
                upper,
                flags=re.I
            )

        except Exception as e:

            print("❌ TRIBUNAL REGEX ERROR:")
            print(str(e))

            continue

        for match in matches:

            value = clean_case_number(match)

            print("🔥 TRIBUNAL MATCH:")
            print(value)

            if re.search(r'\d{2,}', value):

                return build_case_object(

                    case_number=value,

                    court_type="TRIBUNAL",

                    case_type=case_type,

                    confidence=93,

                    source="TRIBUNAL_EXTRACTOR_V2"
                )

    return None
