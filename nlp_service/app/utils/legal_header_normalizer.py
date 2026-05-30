import re


def normalize_legal_header(text: str) -> str:

    if not text:
        return ""

    # =====================================================
    # 🔥 BASIC OCR CLEANING
    # =====================================================

    text = re.sub(r"http[s]?://\S+", " ", text, flags=re.I)

    text = re.sub(r"Page\s+\d+\s+of\s+\d+", " ", text, flags=re.I)

    # =====================================================
    # 🔥 PRESERVE LEGAL LABELS
    # =====================================================

    text = re.sub(r"CASE\s+NO\.?\s*:", " CASE NO: ", text, flags=re.I)

    text = re.sub(r"PETITIONER\s*:", " PETITIONER: ", text, flags=re.I)

    text = re.sub(r"RESPONDENT\s*:", " RESPONDENT: ", text, flags=re.I)

    text = re.sub(r"JUDGMENT\s*:", " JUDGMENT: ", text, flags=re.I)

    # =====================================================
    # 🔥 OCR LINEBREAK NORMALIZATION
    # =====================================================

    text = re.sub(r"[\r\n]+", " ", text)

    # =====================================================
    # 🔥 MULTISPACE COLLAPSE
    # =====================================================

    text = re.sub(r"\s+", " ", text)

    return text.strip()
