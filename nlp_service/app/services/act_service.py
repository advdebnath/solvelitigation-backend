import re


# ============================================
# 🔥 NORMALIZE TEXT
# ============================================
def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


# ============================================
# 🔥 SAFE KEYWORD MAP (STRICT ONLY)
# ============================================
STANDARD_ACTS = {
    "contract": "Indian Contract Act, 1872",
    "agreement": "Indian Contract Act, 1872",
    "breach": "Indian Contract Act, 1872",
    "damages": "Indian Contract Act, 1872",
    "ipc": "Indian Penal Code, 1860",
    "penal code": "Indian Penal Code, 1860",
    "crpc": "Code of Criminal Procedure, 1973",
    "criminal procedure": "Code of Criminal Procedure, 1973",
    "cpc": "Code of Civil Procedure, 1908",
    "civil procedure": "Code of Civil Procedure, 1908",
}


# ============================================
# 🔥 STRICT ACT REGEX (WITH YEAR ONLY)
# ============================================
ACT_REGEX = re.compile(r"\b([A-Z][A-Za-z\s]{3,50}Act,\s?\d{4})\b")


# ============================================
# 🔥 MAIN FUNCTION
# ============================================
def extract_acts(text):
    acts = set()

    text_clean = normalize(text)
    text_lower = text_clean.lower()

    # ============================================
    # 🔥 STEP 1 — STRICT REGEX EXTRACTION
    # ============================================
    matches = ACT_REGEX.findall(text_clean)

    for m in matches:
        act = normalize(m)

        # 🔥 reject long garbage (sentence-like)
        if len(act.split()) > 6:
            continue

        acts.add(act)

    # ============================================
    # 🔥 STEP 2 — CONTEXT DETECTION
    # ============================================
    for keyword, act_name in STANDARD_ACTS.items():
        if keyword in text_lower:
            acts.add(act_name)

    # ============================================
    # 🔥 STEP 3 — FALLBACK (VERY IMPORTANT)
    # ============================================
    if not acts:
        if "university of delhi act" in text_lower:
            acts.add("University of Delhi Act, 1922")

        elif "contract" in text_lower:
            acts.add("Indian Contract Act, 1872")

        elif "penal code" in text_lower:
            acts.add("Indian Penal Code, 1860")

    # ============================================
    # 🔥 STEP 4 — NORMALIZATION
    # ============================================
    cleaned = set()

    for act in acts:
        a = act.lower()

        if "contract act" in a:
            cleaned.add("Indian Contract Act, 1872")

        elif "penal code" in a or "ipc" in a:
            cleaned.add("Indian Penal Code, 1860")

        elif "civil procedure" in a or "cpc" in a:
            cleaned.add("Code of Civil Procedure, 1908")

        elif "criminal procedure" in a or "crpc" in a:
            cleaned.add("Code of Criminal Procedure, 1973")

        else:
            cleaned.add(normalize(act))

    return sorted(list(cleaned))
