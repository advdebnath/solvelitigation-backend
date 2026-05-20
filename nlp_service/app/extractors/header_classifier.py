import re
from typing import Dict


# =========================================================
# 🔥 BODY START MARKERS
# =========================================================

BODY_START_MARKERS = [

    "JUDGMENT",
    "J U D G M E N T",
    "ORDER",
    "O R D E R"
]


# =========================================================
# 🔥 HEADER CLASSIFIER
# =========================================================

def classify_and_clean_header(
    text: str
) -> Dict:

    if not text:

        return {

            "reportable_status": None,
            "court": None,
            "jurisdiction": None,
            "body_start_found": False,
            "clean_text": ""
        }

    original_text = text

    upper_text = text.upper()

    # =====================================================
    # 🔥 REPORTABLE STATUS
    # =====================================================

    reportable_status = None

    if "NON-REPORTABLE" in upper_text:

        reportable_status = "NON-REPORTABLE"

    elif "REPORTABLE" in upper_text:

        reportable_status = "REPORTABLE"

    # =====================================================
    # 🔥 COURT DETECTION
    # =====================================================

    court = None

    if "SUPREME COURT OF INDIA" in upper_text:

        court = "Supreme Court Of India"

    else:

        high_court_match = re.search(

            r'HIGH COURT OF ([A-Z ]+)',
            upper_text
        )

        if high_court_match:

            court = (

                "High Court Of "
                + high_court_match.group(1).title()
            )

    # =====================================================
    # 🔥 JURISDICTION DETECTION
    # =====================================================

    jurisdiction = None

    jurisdiction_patterns = [

        "CIVIL APPELLATE JURISDICTION",
        "CRIMINAL APPELLATE JURISDICTION",
        "CIVIL ORIGINAL JURISDICTION",
        "CRIMINAL ORIGINAL JURISDICTION",
        "WRIT JURISDICTION"
    ]

    for pattern in jurisdiction_patterns:

        if pattern in upper_text:

            jurisdiction = pattern.title()

            break

    # =====================================================
    # 🔥 BODY START DETECTION
    # =====================================================

    clean_text = original_text

    body_start_found = False

    for marker in BODY_START_MARKERS:

        pos = upper_text.find(marker)

        if pos != -1:

            clean_text = original_text[pos:]

            body_start_found = True

            break

    # =====================================================
    # 🔥 FINAL CLEANUP
    # =====================================================

    clean_text = re.sub(

        r'[ \t]+',
        ' ',
        clean_text
    )

    clean_text = re.sub(

        r'\n{3,}',
        '\n\n',
        clean_text
    ).strip()

    return {

        "reportable_status": reportable_status,

        "court": court,

        "jurisdiction": jurisdiction,

        "body_start_found": body_start_found,

        "clean_text": clean_text
    }
