import re

# =========================================================
# 🔥 LEGAL OCR WORD RECONSTRUCTION
# =========================================================

LEGAL_WORD_FIXES = {
    "ques ion": "question",
    "plain iff": "plaintiff",
    "defendan ": "defendant",
    "enancy": "tenancy",
    "judgmen ": "judgment",
    "appealan ": "appellant",
    "responden ": "respondent",
    "cons i u ion": "constitution",
    "ribunal": "tribunal",
    "ac ": "act",
    "cour ": "court",
    "pe i ion": "petition",
    "s a e": "state",
    "wri ": "writ",
    "direc ion": "direction",
    "managemen ": "management",
    "rela ion": "relation",
    "ques ions": "questions",
}


# =========================================================
# 🔥 REMOVE OCR GARBAGE
# =========================================================


def remove_ocr_noise(text):

    NOISE_PATTERNS = [
        r"n===\s*===",
        r"nda e:",
        r"nreason:",
        r"\d{4}\.\d{2}\.\d{2}",
        r"\bis\b\s*nreason",
        r"digitally signed",
        r"signature not verified",
    ]

    for pattern in NOISE_PATTERNS:

        text = re.sub(pattern, " ", text, flags=re.I)

    return text


# =========================================================
# 🔥 FIX SPACED LETTERS
# =========================================================


def fix_spaced_letters(text):

    def repl(match):

        token = match.group(0)

        cleaned = token.replace(" ", "")

        if len(cleaned) >= 4:
            return cleaned

        return token

    return re.sub(r"(?:\b[a-zA-Z]\s+){3,}[a-zA-Z]\b", repl, text)


# =========================================================
# 🔥 APPLY LEGAL VOCABULARY FIXES
# =========================================================


def apply_legal_word_fixes(text):

    for bad, good in LEGAL_WORD_FIXES.items():

        text = re.sub(re.escape(bad), good, text, flags=re.I)

    return text


# =========================================================
# 🔥 MASTER CANONICALIZATION
# =========================================================


def canonicalize_legal_text(text):

    if not text:
        return ""

    text = remove_ocr_noise(text)

    text = fix_spaced_letters(text)

    text = apply_legal_word_fixes(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
