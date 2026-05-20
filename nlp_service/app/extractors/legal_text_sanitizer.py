import re

# =========================================================
# 🔥 OCR / FOOTER / TIMESTAMP CLEANER
# =========================================================

NOISE_PATTERNS = [

    # -----------------------------------------------------
    # TIMESTAMPS
    # -----------------------------------------------------

    r'\b\d{1,2}:\d{2}:\d{2}\b',

    r'\b\d{2}\.\d{2}\.\d{4}\b',

    r'\b\d{4}\.\d{2}\.\d{2}\b',

    # -----------------------------------------------------
    # DIGITAL SIGNATURES
    # -----------------------------------------------------

    r'Digitally signed by.*',

    r'Signed by.*',

    r'Verified digitally.*',

    # -----------------------------------------------------
    # OCR FOOTERS
    # -----------------------------------------------------

    r'IST Reason:.*',

    r'Downloaded on :.*',

    r'Page \d+ of \d+',

    r'::: Uploaded on.*',

    r'http[s]?://\S+',

    # -----------------------------------------------------
    # COURT REPORT HEADER BLEED
    # -----------------------------------------------------

    r'SUPREME COURT REPORTS.*',

    r'HIGH COURT OF .*',

    # -----------------------------------------------------
    # REPEATED SYMBOLS
    # -----------------------------------------------------

    r'[_\-]{5,}',

    r'[=]{5,}',

    # -----------------------------------------------------
    # BROKEN OCR SPACING
    # -----------------------------------------------------

    r'\b(?:[A-Za-z]\s){3,}[A-Za-z]\b'
]

# =========================================================
# 🔥 NORMALIZATION
# =========================================================

def normalize_spacing(
    text
):

    # collapse whitespace

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    # collapse repeated punctuation

    text = re.sub(
        r'([.,])\1+',
        r'\1',
        text
    )

    return text.strip()

# =========================================================
# 🔥 MAIN SANITIZER
# =========================================================

def sanitize_legal_text(
    text=""
):

    if not text:
        return ""

    cleaned = text

    # -----------------------------------------------------
    # REMOVE NOISE
    # -----------------------------------------------------

    for pattern in NOISE_PATTERNS:

        cleaned = re.sub(

            pattern,

            ' ',

            cleaned,

            flags=re.I
        )

    # -----------------------------------------------------
    # REMOVE MULTIPLE SPACES
    # -----------------------------------------------------

    cleaned = normalize_spacing(
        cleaned
    )

    # -----------------------------------------------------
    # REMOVE SHORT OCR GARBAGE LINES
    # -----------------------------------------------------

    lines = cleaned.splitlines()

    final_lines = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        # reject garbage fragments

        if len(stripped) < 3:
            continue

        final_lines.append(
            stripped
        )

    cleaned = "\n".join(final_lines)

    # -----------------------------------------------------
    # FINAL NORMALIZATION
    # -----------------------------------------------------

    cleaned = normalize_spacing(
        cleaned
    )

    return cleaned
