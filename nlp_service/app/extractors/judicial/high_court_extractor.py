# =========================================================
# 🔥 HIGH COURT EXTRACTOR
# =========================================================

import re

from app.extractors.judicial.shared_utils import (
    normalize_ocr,
    clean_case_number,
    build_case_object
)


HC_PATTERNS = [

    (
        r'(WP\s*\(?C\)?\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "WRIT"
    ),

    (
        r'(CRL\.?A\.?\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "CRIMINAL"
    ),

    (
        r'(RSA\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "CIVIL"
    ),

    (
        r'(RFA\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "CIVIL"
    ),

    (
        r'(LPA\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "APPEAL"
    ),

    (
        r'(MACA\s*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "MOTOR_ACCIDENT"
    ),

    (
        r'(CRM[\-\sA-Z]*NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})',
        "CRIMINAL"
    )
]


def extract_hc_case_number(text):

    text = normalize_ocr(text)

    upper = text.upper()

    for pattern, case_type in HC_PATTERNS:

        try:

            matches = re.findall(
                pattern,
                upper,
                flags=re.I
            )

        except Exception as e:

            print("❌ HC REGEX ERROR:")
            print(str(e))

            continue

        for match in matches:

            value = clean_case_number(match)

            print("🔥 HC MATCH:")
            print(value)

            if re.search(r'\d{2,}', value):

                return build_case_object(

                    case_number=value,

                    court_type="HIGH COURT",

                    case_type=case_type,

                    confidence=95,

                    source="HC_EXTRACTOR_V2"
                )

    return None
