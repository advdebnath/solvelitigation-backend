import re

from app.utils.ocr_legal_normalizer import (
    normalize_ocr_legal_text
)

from app.legal_ontology.proceeding_family_ontology import (
    PROCEEDING_FAMILY_ONTOLOGY
)


RAW_CAPTION_PATTERNS = [

    {
        "family": "CIVIL_APPEAL",

        "pattern":
            r'(Appeal\s*\((?:civil|criminal)\)\s*'
            r'[\d\-\/]+\s*of\s*\d{4})'
    },

    {
        "family": "CIVIL_APPEAL",

        "pattern":
            r'(Civil\s+Appeal\s+No\.?\s*'
            r'[\d\-\/]+\s*of\s*\d{4})'
    },

    {
        "family": "CRIMINAL_APPEAL",

        "pattern":
            r'(Criminal\s+Appeal\s+No\.?\s*'
            r'[\d\-\/]+\s*of\s*\d{4})'
    },

    {
        "family": "SPECIAL_LEAVE_PETITION_CIVIL",

        "pattern":
            r'(SLP\s*\(C\)\s*No\.?\s*'
            r'[\d\-\/]+\s*of\s*\d{4})'
    },

    {
        "family": "WRIT_PETITION_CIVIL",

        "pattern":
            r'(WP\s*\(C\)\s*No\.?\s*'
            r'[\d\-\/]+\s*of\s*\d{4})'
    },

    {
        "family": "ORIGINAL_APPLICATION",

        "pattern":
            r'(OA\s*No\.?\s*'
            r'[\d\-\/]+(?:\/\d{4})?(?:\s*OF\s*\d{4})?)'
    },
]


def preserve_raw_caption(header):

    if not header:

        return None


    # =====================================================
    # 🔥 SHARED OCR LEGAL NORMALIZATION
    # =====================================================

    header = normalize_ocr_legal_text(
        header
    )

    for entry in RAW_CAPTION_PATTERNS:

        family = entry["family"]

        pattern = entry["pattern"]

        try:

            match = re.search(
                pattern,
                header,
                flags=re.I
            )

            if not match:
                continue

            caption = re.sub(
                r'\s+',
                ' ',
                match.group(0)
            ).strip().upper()

            
            family_data = (
                PROCEEDING_FAMILY_ONTOLOGY.get(
                    family,
                    {}
                )
            )

            case_type = family_data.get(
                "case_type"
            )

            court_type = family_data.get(
                "court_type"
            )


            return {
                "case_number": caption,
                "canonical_case_number": caption,
                "normalized_case_number": caption,
                "case_type": case_type,
                "court_type": court_type,
                "source": "RAW_CAPTION_ENGINE",
                "validation_status": "VALID",
                "confidence": 100
            }

        except Exception as e:

            print("❌ CAPTION PRESERVATION ERROR:")
            print(e)

    return None
