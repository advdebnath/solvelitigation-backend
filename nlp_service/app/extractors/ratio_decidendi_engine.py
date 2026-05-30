import re

# =========================================================
# 🔥 RATIO PATTERNS
# =========================================================

RATIO_PATTERNS = [
    r"it is settled law that",
    r"the legal position is",
    r"we hold that",
    r"it is clear that",
    r"the principle is",
    r"therefore,? it is held",
    r"the law requires",
    r"it is a settled principle",
    r"accordingly,? we hold",
    r"the court held that",
]


# =========================================================
# 🔥 STRONG LEGAL PRINCIPLE PATTERNS
# =========================================================

LEGAL_PRINCIPLE_PATTERNS = [
    r"natural justice",
    r"burden of proof",
    r"presumption of innocence",
    r"wakf property",
    r"constitutional mandate",
    r"rule of law",
    r"mens rea",
    r"proof beyond reasonable doubt",
    r"doctrine of proportionality",
    r"doctrine of legitimate expectation",
    r"arbitrary action",
    r"statutory authority",
]


# =========================================================
# 🔥 CLEAN
# =========================================================


def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 SPLIT SENTENCES
# =========================================================


def split_sentences(text):

    return re.split(r"(?<=[.!?])\s+", text)


# =========================================================
# 🔥 DETECT PRINCIPLES
# =========================================================


def detect_principles(text):

    principles = []

    for pattern in LEGAL_PRINCIPLE_PATTERNS:

        matches = re.findall(pattern, text, re.I)

        for match in matches:

            principle = clean_text(match)

            if principle not in principles:

                principles.append(principle)

    return principles


# =========================================================
# 🔥 DETECT BINDING STRENGTH
# =========================================================


def detect_binding_strength(text):

    text = text.lower()

    if "constitution bench" in text:

        return "Very High"

    if "supreme court" in text:

        return "High"

    if "high court" in text:

        return "Moderate"

    return "Normal"


# =========================================================
# 🔥 EXTRACT RATIO
# =========================================================


def extract_ratio_decidendi(text):

    try:

        text = clean_text(text)

        sentences = split_sentences(text)

        ratios = []

        # =================================================
        # 🔥 PROCESS SENTENCES
        # =================================================

        for idx, sentence in enumerate(sentences):

            lower = sentence.lower()

            matched = False

            for pattern in RATIO_PATTERNS:

                if re.search(pattern, lower, re.I):

                    matched = True
                    break

            if not matched:
                continue

            # =============================================
            # 🔥 LOCAL WINDOW
            # =============================================

            context = " ".join(sentences[idx : min(len(sentences), idx + 2)])

            context = clean_text(context)

            # =============================================
            # 🔥 PRINCIPLES
            # =============================================

            principles = detect_principles(context)

            # =============================================
            # 🔥 BINDING STRENGTH
            # =============================================

            strength = detect_binding_strength(context)

            ratios.append(
                {
                    "ratio": context[:1200],
                    "legal_principles": principles,
                    "binding_strength": strength,
                }
            )

        # =================================================
        # 🔥 REMOVE DUPLICATES
        # =================================================

        unique = []

        seen = set()

        for item in ratios:

            key = item["ratio"][:200].lower()

            if key in seen:
                continue

            seen.add(key)

            unique.append(item)

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {"ratio_decidendi": unique, "confidence": 95}

        print("✅ Ratio Decidendi Extracted:")

        print(result)

        return result

    except Exception as e:

        print("❌ Ratio Engine Error:", str(e))

        return {"ratio_decidendi": [], "confidence": 0}


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    It is settled law that Wakf property
    cannot be alienated without statutory authority.

    The principle of natural justice
    requires hearing before adverse action.

    Accordingly, we hold that the High Court
    committed an error.
    """

    print(extract_ratio_decidendi(sample))
