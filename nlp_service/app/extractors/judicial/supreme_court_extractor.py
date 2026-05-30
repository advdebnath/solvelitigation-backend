# =========================================================
# 🔥 SUPREME COURT EXTRACTOR
# =========================================================

import re

from app.extractors.judicial.shared_utils import (build_case_object,
                                                  clean_case_number,
                                                  normalize_ocr)

SC_PATTERNS = [
    (r"(CIVIL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d{4})", "CIVIL"),
    (r"(CRIMINAL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d{4})", "CRIMINAL"),
    (r"(SLP.*?NO\.?\s*\d+\s+OF\s+\d{4})", "SPECIAL_LEAVE"),
    (r"(WRIT\s+PETITION.*?NO\.?\s*\d+\s+OF\s+\d{4})", "WRIT"),
    (r"(REVIEW\s+PETITION.*?NO\.?\s*\d+\s+OF\s+\d{4})", "REVIEW"),
]


def extract_sc_case_number(text):

    text = normalize_ocr(text)

    upper = text.upper()

    for pattern, case_type in SC_PATTERNS:

        try:

            matches = re.findall(pattern, upper, flags=re.I)

        except Exception as e:

            print("❌ SC REGEX ERROR:")
            print(str(e))

            continue

        for match in matches:

            value = clean_case_number(match)

            print("🔥 SC MATCH:")
            print(value)

            if re.search(r"\d{2,}", value):

                return build_case_object(
                    case_number=value,
                    court_type="SUPREME COURT",
                    case_type=case_type,
                    confidence=100,
                    source="SC_EXTRACTOR_V2",
                )

    return None
