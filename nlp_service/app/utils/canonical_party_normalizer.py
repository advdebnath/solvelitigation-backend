import hashlib
import re

# =========================================================
# 🔥 PROCEDURAL / LEGAL SUFFIXES
# =========================================================

GOVERNMENT_HINTS = [
    "UNION OF INDIA",
    "STATE OF",
    "COMMISSIONER",
    "SECRETARY",
    "MINISTRY",
    "DEPARTMENT",
    "CUSTOMS",
    "GST",
    "SEBI",
    "CBI",
    "NIA",
    "INCOME TAX",
    "DIRECTORATE",
    "POLICE",
]


def detect_entity_type(name):

    if not name:
        return "UNKNOWN"

    upper = name.upper()

    for hint in GOVERNMENT_HINTS:

        if hint in upper:
            return "GOVERNMENT"

    return "PRIVATE_ENTITY"


PROCEDURAL_SUFFIXES = [
    r"\bM/S\.?\b",
    r"\b(DEAD)\b",
    r"\bTHROUGH\s+L\.?R\.?S?\.?\b",
    r"\bL\.?R\.?S?\.?\b",
    r"\bLEGAL\s+REPRESENTATIVE[S]?\b",
    r"\bREPRESENTED\s+BY\b",
    r"\bAPPELLANT[S]?\b",
    r"\bPETITIONER[S]?\b",
    r"\bRESPONDENT[S]?\b",
    r"\bVERSUS\b",
    r"\bVS\.?\b",
    r"\bV\.?\b",
    r"\bAND\s+OTHERS\b",
    r"\bOTHERS\b",
    r"\bORS\.?\b",
    r"\bANR\.?\b",
    r"\bETC\.?\b",
    r"\bSINCE\s+DEAD\b",
    r"\bDECEASED\b",
]


# =========================================================
# 🔥 OCR NORMALIZATION
# =========================================================


def normalize_ocr_spacing(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 PARTY NORMALIZATION
# =========================================================


def normalize_party_name(name):

    if not name:
        return ""

    name = normalize_ocr_spacing(name)

    for pattern in PROCEDURAL_SUFFIXES:

        name = re.sub(pattern, " ", name, flags=re.I)

    name = re.sub(r"\([^)]*\)", " ", name)

    name = re.sub(r"[^A-Z0-9\s\.\&\-]", " ", name, flags=re.I)

    name = re.sub(r"\s+", " ", name).strip()

    # -----------------------------------------------------
    # 🔥 EDGE PUNCTUATION CLEANUP
    # -----------------------------------------------------

    name = re.sub(r"^[\.\&\-\s]+", "", name)

    name = re.sub(r"[\.\&\-\s]+$", "", name)

    name = re.sub(r"\s+", " ", name).strip()

    return name


# =========================================================
# 🔥 ENTITY HASH
# =========================================================


def build_entity_hash(name):

    if not name:
        return ""

    return hashlib.sha256(name.upper().encode()).hexdigest()


# =========================================================
# 🔥 FULL CAPTION NORMALIZATION
# =========================================================


def normalize_party_caption(case_title):

    if not case_title:
        return {"petitioner": "", "respondent": ""}

    title = normalize_ocr_spacing(case_title)

    split_pattern = r"\b(?:VS\.?|VERSUS|V\.?)\b"

    parts = re.split(split_pattern, title, maxsplit=1, flags=re.I)

    petitioner = ""
    respondent = ""

    if len(parts) >= 1:
        petitioner = normalize_party_name(parts[0])

    if len(parts) >= 2:
        respondent = normalize_party_name(parts[1])

    return {
        "petitioner": {
            "canonical_name": petitioner,
            "entity_type": detect_entity_type(petitioner),
            "entity_hash": build_entity_hash(petitioner),
            "confidence": 98,
        },
        "respondent": {
            "canonical_name": respondent,
            "entity_type": detect_entity_type(respondent),
            "entity_hash": build_entity_hash(respondent),
            "confidence": 98,
        },
    }


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    sample = (
        "M/S. BHAGWAN DASS RAMA SHANKER "
        "(DEAD) THROUGH L.RS. "
        "Vs. UNION OF INDIA & ORS."
    )

    print(normalize_party_caption(sample))
