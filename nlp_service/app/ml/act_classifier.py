import re

# ============================================
# 🔥 NORMALIZED ACT NAMES (STANDARD)
# ============================================
ACT_NAMES = {
    "IPC": "Indian Penal Code, 1860",
    "CRPC": "Code of Criminal Procedure, 1973",
    "EVIDENCE": "Indian Evidence Act, 1872",
    "CONTRACT": "Indian Contract Act, 1872",
    "GST": "Goods and Services Tax Act, 2017",
    "INCOME_TAX": "Income Tax Act, 1961",
    "NI": "Negotiable Instruments Act, 1881",
}

# ============================================
# 🔥 PATTERN MATCHING (STRICT + CONTROLLED)
# ============================================
ACT_PATTERNS = {
    ACT_NAMES["IPC"]: [
        r"\bIPC\b",
        r"Indian Penal Code",
    ],
    ACT_NAMES["CRPC"]: [
        r"\bCrPC\b",
        r"Code of Criminal Procedure",
    ],
    ACT_NAMES["EVIDENCE"]: [
        r"Evidence Act",
        r"Indian Evidence Act",
    ],
    ACT_NAMES["CONTRACT"]: [
        r"Indian Contract Act",
        r"Contract Act",
        r"breach of contract",
        r"offer and acceptance",
    ],
    ACT_NAMES["GST"]: [
        r"\bGST\b",
        r"Goods and Services Tax",
    ],
    ACT_NAMES["INCOME_TAX"]: [
        r"Income Tax",
        r"\bIT Act\b",
    ],
    ACT_NAMES["NI"]: [
        r"Negotiable Instruments Act",
        r"cheque dishonour",
        r"section\s+138",
    ],
}

# ============================================
# 🔥 SECTION → ACT MAPPING (ENHANCED)
# ============================================
SECTION_MAP = {
    # IPC
    302: ACT_NAMES["IPC"],
    304: ACT_NAMES["IPC"],
    420: ACT_NAMES["IPC"],
    34: ACT_NAMES["IPC"],
    # NI Act
    138: ACT_NAMES["NI"],
    # Contract Act
    73: ACT_NAMES["CONTRACT"],
    74: ACT_NAMES["CONTRACT"],
}


# ============================================
# 🔥 MAIN DETECTION FUNCTION (FINAL)
# ============================================
def detect_acts(text: str):
    if not text:
        return []

    text_lower = text.lower()
    found_acts = set()

    # ============================================
    # 🔍 PATTERN MATCHING
    # ============================================
    for act, patterns in ACT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found_acts.add(act)
                break

    # ============================================
    # 🔍 SECTION-BASED DETECTION
    # ============================================
    sections = re.findall(r"section\s+(\d+)", text_lower)

    for sec in sections:
        sec_num = int(sec)
        if sec_num in SECTION_MAP:
            found_acts.add(SECTION_MAP[sec_num])

    # ============================================
    # 🔍 CONTEXTUAL FALLBACK (CONTROLLED)
    # ============================================

    # Criminal context
    if any(word in text_lower for word in ["murder", "homicide", "assault"]):
        found_acts.add(ACT_NAMES["IPC"])

    # Cheque / banking
    if "cheque" in text_lower and "dishonour" in text_lower:
        found_acts.add(ACT_NAMES["NI"])

    # Contract context (STRICT)
    if "contract" in text_lower and "breach" in text_lower:
        found_acts.add(ACT_NAMES["CONTRACT"])

    # ============================================
    # 🔍 FINAL CLEANING
    # ============================================
    return sorted(found_acts)
