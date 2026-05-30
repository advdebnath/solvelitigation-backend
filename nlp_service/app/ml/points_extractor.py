import re

# ============================================
# 🔥 SECTION → LEGAL MEANING (CORE ENGINE)
# ============================================
SECTION_MEANING = {
    # IPC
    "302": "Punishment for murder",
    "304": "Culpable homicide not amounting to murder",
    "420": "Cheating and dishonestly inducing delivery of property",
    "34": "Acts done by several persons in furtherance of common intention",
    # NI Act
    "138": "Dishonour of cheque for insufficiency of funds",
    # Contract Act
    "73": "Compensation for loss or damage caused by breach of contract",
    "74": "Compensation for breach of contract where penalty stipulated",
}

# ============================================
# 🔥 LEGAL KEYWORD → POINTS (INTELLIGENT)
# ============================================
LEGAL_KEYWORDS = {
    "breach": "Breach of Contract",
    "negligence": "Negligence",
    "fraud": "Fraud",
    "cheque": "Dishonour of Cheque",
    "agreement": "Formation of Contract",
    "offer": "Offer and Acceptance",
    "acceptance": "Offer and Acceptance",
    "damages": "Claim for Damages",
    "liability": "Legal Liability",
}


# ============================================
# 🔥 MAIN FUNCTION (FINAL)
# ============================================
def extract_points(text: str):
    if not text:
        return []

    text_lower = text.lower()
    points = set()

    # ============================================
    # 🔍 KEYWORD-BASED LEGAL POINTS
    # ============================================
    for key, value in LEGAL_KEYWORDS.items():
        if key in text_lower:
            points.add(value)

    # ============================================
    # 🔍 SECTION EXTRACTION + MEANING
    # ============================================
    sections = re.findall(r"section\s+(\d+)", text_lower)

    for sec in sections:
        if sec in SECTION_MEANING:
            points.add(f"Section {sec} – {SECTION_MEANING[sec]}")
        else:
            points.add(f"Section {sec}")

    # ============================================
    # 🔍 CONTEXTUAL INTELLIGENCE (ADVANCED)
    # ============================================

    # Criminal inference
    if "murder" in text_lower:
        points.add("Offence of Murder")

    if "cheque" in text_lower and "dishonour" in text_lower:
        points.add("Dishonour of Cheque")

    if "breach" in text_lower and "contract" in text_lower:
        points.add("Breach of Contract")

    # ============================================
    # 🔍 CLEAN OUTPUT
    # ============================================
    return sorted(points)
