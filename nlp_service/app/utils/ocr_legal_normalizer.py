import re

OCR_REPAIRS = [
    # =====================================================
    # TOKEN RECONSTRUCTION
    # =====================================================
    (r"S\s+L\s+P\s*\(\s*C\s*\)", "SLP(C)"),
    (r"S\s*\n\s*L\s*\n\s*P\s*\n\s*\(\s*\n\s*C\s*\n\s*\)", "SLP(C)"),
    (r"W\s+P\s*\(\s*C\s*\)", "WP(C)"),
    (r"W\s*\n\s*P\s*\n\s*\(\s*\n\s*C\s*\n\s*\)", "WP(C)"),
    (r"CIVIL\s*\n\s*APPEAL", "CIVIL APPEAL"),
    # =====================================================
    # OCR GLYPH REPAIR
    # =====================================================
    (r"AppeaI", "Appeal"),
    (r"civiI", "civil"),
    (r"CriminaI", "Criminal"),
    (r"SIP", "SLP"),
    (r"No\s*\.", "No."),
]


def normalize_ocr_legal_text(text):

    if not text:
        return text

    for bad, good in OCR_REPAIRS:

        text = re.sub(bad, good, text, flags=re.I)

    return text
