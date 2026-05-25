import re

from app.extractors.case_number_bridge import (
    extract_case_number
)

# =========================================================
# 🔒 CANONICAL CASE IDENTITY ENGINE
# =========================================================

def build_canonical_case_identity(
    raw_legal_text,
    header_text="",
    court="Unknown Court"
):

    if not raw_legal_text:
        return {
            "case_number": "Unknown Case",
            "confidence": 0,
            "canonical_id": None
        }

    raw_legal_text = str(
        raw_legal_text
    )

    header_text = str(
        header_text or raw_legal_text[:12000]
    )

    # -----------------------------------------------------
    # 🔒 PRIMARY EXTRACTION
    # -----------------------------------------------------

    extracted = extract_case_number(
        header_text
    )

    case_number = extracted.get(
        "case_number",
        "Unknown Case"
    )

    confidence = extracted.get(
        "confidence",
        0
    )

    # -----------------------------------------------------
    # 🔒 SECONDARY RECOVERY
    # -----------------------------------------------------

    if (
        not case_number
        or case_number == "Unknown Case"
    ):

        fallback_patterns = [

            r"(CRIMINAL\s+APPEAL\s+NO\.?\s*[\d\/\-]+\s+OF\s+\d{4})",

            r"(CIVIL\s+APPEAL\s+NO\.?\s*[\d\/\-]+\s+OF\s+\d{4})",

            r"(WRIT\s+PETITION\s*\(.+?\)\s*NO\.?\s*[\d\/\-]+\s+OF\s+\d{4})",

            r"(SPECIAL\s+LEAVE\s+PETITION.+?OF\s+\d{4})",

            r"(TRANSFER\s+PETITION.+?OF\s+\d{4})"
        ]

        for pattern in fallback_patterns:

            match = re.search(
                pattern,
                raw_legal_text[:25000],
                flags=re.I
            )

            if match:

                case_number = (
                    match.group(1)
                    .strip()
                )

                confidence = 70

                break

    # -----------------------------------------------------
    # 🔒 FINAL NORMALIZATION
    # -----------------------------------------------------

    case_number = re.sub(
        r"\s+",
        " ",
        str(case_number)
    ).strip()

    if not case_number:
        case_number = "Unknown Case"

    # -----------------------------------------------------
    # 🔒 IMMUTABLE CANONICAL ID
    # -----------------------------------------------------

    # -----------------------------------------------------
    # 🔒 UNKNOWN CASE FALLBACK LOCK
    # -----------------------------------------------------

    if case_number == "Unknown Case":

        fallback_hash = abs(
            hash(
                raw_legal_text[:5000]
            )
        )

        canonical_id = (
            f"{court}::UNKNOWN::{fallback_hash}"
        )

    else:

        canonical_id = (
            f"{court}::{case_number}"
        )

    return {
        "case_number": case_number,
        "confidence": confidence,
        "canonical_id": canonical_id
    }
