import re
import unicodedata

# =========================================================
# 🔥 INVISIBLE / BAD CHARACTERS
# =========================================================

BAD_UNICODE = [
    "\u200b",  # zero-width space
    "\ufeff",  # BOM
    "\u00a0",  # non-breaking space
]

# =========================================================
# 🔥 NORMALIZE UNICODE
# =========================================================


def normalize_unicode(text):

    if not text:

        return ""

    text = unicodedata.normalize("NFKC", text)

    for bad in BAD_UNICODE:

        text = text.replace(bad, " ")

    return text


# =========================================================
# 🔥 OCR NORMALIZATION
# =========================================================


def normalize_ocr(text):

    if not text:

        return ""

    # =====================================================
    # 🔥 DASH NORMALIZATION
    # =====================================================

    text = text.replace("—", "-")

    text = text.replace("–", "-")

    # =====================================================
    # 🔥 QUOTES
    # =====================================================

    text = text.replace("“", '"')

    text = text.replace("”", '"')

    text = text.replace("‘", "'")

    text = text.replace("’", "'")

    # =====================================================
    # 🔥 OCR DOTS
    # =====================================================

    text = text.replace("…", "...")

    return text


# =========================================================
# 🔥 REMOVE PAGE NUMBERS
# =========================================================


def remove_page_numbers(text):

    # PAGE NUMBER ALONE

    text = re.sub(r"(?m)^\s*\d+\s*$", " ", text)

    # PAGE X OF Y

    text = re.sub(r"(?i)page\s+\d+\s+of\s+\d+", " ", text)

    return text


# =========================================================
# 🔥 REMOVE HEADER / FOOTER NOISE
# =========================================================


def remove_header_footer_noise(text):

    patterns = [
        r"REPORTABLE",
        r"NON[- ]REPORTABLE",
        r"ITEM\s+NO\.\s*\d+",
        r"COURT\s+NO\.\s*\d+",
        r"SECTION\s+[A-Z]+",
        r"SUPREME COURT REPORTS",
        r"Downloaded\s+on\s+\:\s+.*",
        r"https?\:\/\/\S+",
        r"Digitally signed by.*",
        r"Signature Not Verified",
        r"Page \d+",
        r"BAR\s*CODE",
        r"SCANNED COPY",
    ]

    for pattern in patterns:

        text = re.sub(pattern, " ", text, flags=re.I)

    return text


# =========================================================
# 🔥 REMOVE EXCESS SYMBOLS
# =========================================================


def remove_symbol_noise(text):

    # LONG SYMBOL CHAINS

    text = re.sub(r"[_=~`]{2,}", " ", text)

    # EXCESS DOTS

    text = re.sub(r"\.{4,}", "...", text)

    return text


# =========================================================
# 🔥 FIX BROKEN LINES
# =========================================================


def fix_broken_lines(text):

    # =====================================================
    # 🔥 JOIN WORD BREAKS
    # =====================================================

    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # =====================================================
    # 🔥 JOIN SENTENCE WRAPS
    # =====================================================

    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    return text


# =========================================================
# 🔥 NORMALIZE SPACES
# =========================================================


def normalize_spaces(text):

    text = re.sub(r"\r", "\n", text)

    text = re.sub(r"\t", " ", text)

    text = re.sub(r"[ ]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# =========================================================
# 🔥 FINAL CLEANING
# =========================================================


def final_cleanup(text):

    # REMOVE EXCESS WHITESPACE

    text = re.sub(r"[ ]{2,}", " ", text)

    # REMOVE EMPTY LINES

    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    return text.strip()


# =========================================================
# 🔥 MAIN CLEANER
# =========================================================


def clean_legal_text(text):

    try:

        if not text:

            return ""

        original_length = len(text)

        # =====================================================
        # 🔥 STEP 1 — UNICODE
        # =====================================================

        text = normalize_unicode(text)

        # =====================================================
        # 🔥 STEP 2 — OCR NORMALIZATION
        # =====================================================

        text = normalize_ocr(text)

        # =====================================================
        # 🔥 STEP 3 — REMOVE PAGE NUMBERS
        # =====================================================

        text = remove_page_numbers(text)

        # =====================================================
        # 🔥 STEP 4 — REMOVE HEADER/FOOTER
        # =====================================================

        text = remove_header_footer_noise(text)

        # =====================================================
        # 🔥 STEP 5 — REMOVE SYMBOL NOISE
        # =====================================================

        text = remove_symbol_noise(text)

        # =====================================================
        # 🔥 STEP 6 — FIX BROKEN LINES
        # =====================================================

        text = fix_broken_lines(text)

        # =====================================================
        # 🔥 STEP 7 — NORMALIZE SPACES
        # =====================================================

        text = normalize_spaces(text)

        # =====================================================
        # 🔥 STEP 8 — FINAL CLEANUP
        # =====================================================

        text = final_cleanup(text)

        print(f"✅ Text Cleaned: " f"{original_length} → {len(text)} chars")

        return text

    except Exception as e:

        print("❌ TEXT CLEANER ERROR:", e)

        return text
