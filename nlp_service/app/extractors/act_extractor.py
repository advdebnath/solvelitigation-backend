import re

# =========================================================
# 🔥 EXPLICIT ACT REGISTRY
# =========================================================

ACT_REGISTRY = {
    "INDIAN PENAL CODE": {
        "canonical": "Indian Penal Code, 1860",
        "short": "IPC",
        "category": "Criminal",
        "patterns": [r"\bIPC\b", r"\bIndian Penal Code\b"],
    },
    "CRPC": {
        "canonical": "Code Of Criminal Procedure, 1973",
        "short": "CrPC",
        "category": "Criminal",
        "patterns": [r"\bCrPC\b", r"\bCode Of Criminal Procedure\b"],
    },
    "CPC": {
        "canonical": "Code Of Civil Procedure, 1908",
        "short": "CPC",
        "category": "Civil",
        "patterns": [r"\bCPC\b", r"\bCode Of Civil Procedure\b"],
    },
    "CONSTITUTION": {
        "canonical": "Constitution Of India",
        "short": "Constitution",
        "category": "Constitutional",
        "patterns": [
            r"\bConstitution Of India\b",
            r"\bConstitution\b",
        ],
    },
    "EVIDENCE": {
        "canonical": "Indian Evidence Act, 1872",
        "short": "Evidence Act",
        "category": "Civil",
        "patterns": [r"\bEvidence Act\b", r"\bIndian Evidence Act\b"],
    },
    "NEGOTIABLE": {
        "canonical": "Negotiable Instruments Act, 1881",
        "short": "NI Act",
        "category": "Criminal",
        "patterns": [r"\bNI Act\b", r"\bNegotiable Instruments Act\b"],
    },
    "WAKF": {
        "canonical": "Wakf Act, 1995",
        "short": "Wakf Act",
        "category": "Civil",
        "patterns": [r"\bWakf\b", r"\bWakf Act\b"],
    },
    "CONTRACT": {
        "canonical": "Indian Contract Act, 1872",
        "short": "Contract Act",
        "category": "Civil",
        "patterns": [r"\bContract Act\b", r"\bIndian Contract Act\b"],
    },
}

# =========================================================
# 🔥 STRICT ACT CONFIDENCE ENGINE
# =========================================================


def calculate_act_confidence(
    act_name="", text="", matched_sections=None, category=None
):

    if matched_sections is None:
        matched_sections = []

    score = 0

    text_lower = text.lower()

    act_lower = act_name.lower()

    # -----------------------------------------------------
    # 🔥 DIRECT ACT MENTION
    # -----------------------------------------------------

    if act_lower in text_lower:

        score += 50

    # -----------------------------------------------------
    # 🔥 SHORT TOKEN BOOST
    # -----------------------------------------------------

    short_tokens = [
        "ipc",
        "crpc",
        "constitution",
        "wakf",
        "contract act",
        "evidence act",
        "ni act",
    ]

    for token in short_tokens:

        if token in text_lower and token in act_lower:

            score += 20

    # -----------------------------------------------------
    # 🔥 SECTION SUPPORT
    # -----------------------------------------------------

    if matched_sections:

        score += min(30, len(matched_sections) * 10)

    # -----------------------------------------------------
    # 🔥 CATEGORY CONSISTENCY
    # -----------------------------------------------------

    if category == "Criminal":

        criminal_words = ["fir", "bail", "accused", "conviction", "sentence"]

        if any(x in text_lower for x in criminal_words):

            if any(x in act_lower for x in ["penal", "criminal", "ndps", "pocso"]):

                score += 20

    if category == "Civil":

        civil_words = ["property", "wakf", "agreement", "tenancy", "partition"]

        if any(x in text_lower for x in civil_words):

            if any(x in act_lower for x in ["wakf", "contract", "property"]):

                score += 20

    # -----------------------------------------------------
    # 🔥 WEAK ACT PENALTY
    # -----------------------------------------------------

    weak_words = ["procedure", "miscellaneous", "general"]

    if any(x in act_lower for x in weak_words):

        if score < 60:

            score -= 25

    return max(score, 0)


# =========================================================
# 🔥 NORMALIZATION
# =========================================================


def normalize_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 SECTION LINK BOOST
# =========================================================

SECTION_ACT_MAP = {
    "482": "Code Of Criminal Procedure, 1973",
    "138": "Negotiable Instruments Act, 1881",
    "302": "Indian Penal Code, 1860",
    "83": "Wakf Act, 1995",
    "85": "Wakf Act, 1995",
}

# =========================================================
# 🔥 EXTRACT ACTS
# =========================================================


def extract_acts(text):

    try:

        if not text:

            return {"acts": [], "matched_sections": [], "confidence": 0}

        text = normalize_text(text)

        found = {}

        # =================================================
        # 🔥 EXPLICIT PATTERN MATCHING
        # =================================================

        for _, config in ACT_REGISTRY.items():

            score = 0

            for pattern in config["patterns"]:

                matches = re.findall(pattern, text, re.I)

                if matches:

                    score += len(matches)

            if score > 0:

                canonical = config["canonical"]

                confidence = calculate_act_confidence(
                    act_name=canonical,
                    text=text,
                    matched_sections=[],
                    category=config["category"],
                )

                if confidence < 45:

                    continue

                found[canonical] = {
                    "act_name": canonical,
                    "short_name": config["short"],
                    "category": config["category"],
                    "score": score,
                    "confidence": confidence,
                }

        # =================================================
        # 🔥 SECTION LINK BOOSTING
        # =================================================

        matched_sections = []

        section_matches = re.findall(r"Section[s]?\s+(\d+[A-Za-z]*)", text, re.I)

        article_matches = re.findall(r"Article\s+(\d+[A-Za-z]*)", text, re.I)

        matched_sections.extend(section_matches)

        matched_sections.extend(article_matches)

        for sec in matched_sections:

            sec = sec.strip()

            if sec in SECTION_ACT_MAP:

                boosted_act = SECTION_ACT_MAP[sec]

                # =========================================
                # 🔥 BOOST EXISTING
                # =========================================

                frequency = matched_sections.count(sec)

                if boosted_act in found:

                    found[boosted_act]["score"] += 5 * frequency

                else:

                    # =====================================
                    # 🔥 CREATE BOOSTED ENTRY
                    # =====================================

                    category = "General"

                    short_name = boosted_act

                    for _, cfg in ACT_REGISTRY.items():

                        if cfg["canonical"] == boosted_act:

                            category = cfg["category"]

                            short_name = cfg["short"]

                    found[boosted_act] = {
                        "act_name": boosted_act,
                        "short_name": short_name,
                        "category": category,
                        "score": 5,
                    }

        # =================================================
        # 🔥 SORT BY SCORE
        # =================================================

        acts = sorted(found.values(), key=lambda x: x["score"], reverse=True)

        # =================================================
        # 🔥 REMOVE INTERNAL SCORE
        # =================================================

        for act in acts:

            act.pop("score", None)

        # =================================================
        # 🔥 CONFIDENCE
        # =================================================

        confidence = 50

        if len(acts) > 1:

            confidence += 20

        if matched_sections:

            confidence += 20

        confidence = min(confidence, 95)

        result = {
            "acts": acts,
            "matched_sections": list(set(matched_sections)),
            "confidence": confidence,
        }

        print("✅ Acts Extracted:", result)

        return result

    except Exception as e:

        print("❌ ACT EXTRACTION ERROR:", e)

        return {"acts": [], "matched_sections": [], "confidence": 0}


# =========================================================
# 🔥 DIRECT TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    Section 83 of the Wakf Act
    was challenged.

    Article 226 of the Constitution Of India
    was invoked.

    Section 482 CrPC was relied upon.

    Section 152 Contract Act
    was discussed.
    """

    print(extract_acts(sample))
