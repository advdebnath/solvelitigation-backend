import re

# =========================================================
# 🔥 INVALID RATIO PATTERNS
# =========================================================

INVALID_RATIO_PATTERNS = [
    "criminal appeal no",
    "civil appeal no",
    "special leave petition",
    "arising out of",
    "learned counsel",
    "appearance",
    "advocate",
    "headnote",
    "table of contents",
    "index",
    "present",
    "coram",
    "versus",
    "vs.",
    "date:",
    "reason:",
    "appellant",
    "respondent",
    "petitioner",
]

# =========================================================
# 🔥 LEGAL REASONING TERMS
# =========================================================

LEGAL_REASONING_TERMS = [
    "we are of the opinion",
    "it is evident",
    "it is clear",
    "held that",
    "the court held",
    "therefore",
    "hence",
    "accordingly",
    "in our opinion",
    "in view of",
    "it cannot be said",
    "it is settled law",
    "the legal position",
    "we hold",
    "thus",
]

# =========================================================
# 🔥 CLEAN TEXT
# =========================================================


def clean_text(text):

    if not text:

        return ""

    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# =========================================================
# 🔥 SPLIT PARAGRAPHS
# =========================================================


def split_paragraphs(text):

    parts = re.split(r"\n\s*\n", text)

    cleaned = []

    for p in parts:

        para = p.strip()

        if len(para) > 80:

            cleaned.append(para)

    return cleaned


# =========================================================
# 🔥 INVALID PARAGRAPH
# =========================================================


def is_invalid_paragraph(para):

    lower = para.lower()

    for pattern in INVALID_RATIO_PATTERNS:

        if pattern in lower:

            return True

    return False


# =========================================================
# 🔥 SCORE LEGAL REASONING
# =========================================================


def score_ratio_paragraph(para):

    lower = para.lower()

    if is_invalid_paragraph(para):

        return 0

    score = 0

    # =====================================================
    # LEGAL REASONING BOOST
    # =====================================================

    for term in LEGAL_REASONING_TERMS:

        if term in lower:

            score += 20

    # =====================================================
    # LEGAL LENGTH BOOST
    # =====================================================

    if 300 <= len(para) <= 2500:

        score += 10

    # =====================================================
    # SECTION / ARTICLE BOOST
    # =====================================================

    if re.search(r"(section|article)\s+\d+", lower):

        score += 15

    return score


# =========================================================
# 🔥 EXTRACT PARA NUMBER
# =========================================================


def extract_para_number(para):

    patterns = [
        r"\b(\d{1,3})\.\s",
        r"\((\d{1,3})\)",
        r"paragraph\s+(\d{1,3})",
    ]

    for pattern in patterns:

        match = re.search(pattern, para, re.I)

        if match:

            return f"para-{match.group(1)}"

    return "para-unknown"


# =========================================================
# 🔥 MAIN RATIO ENGINE
# =========================================================


def extract_ratio(text):

    try:

        if not text:

            return {
                "ratio": None,
                "para": None,
                "confidence": 0,
            }

        text = clean_text(text)

        paragraphs = split_paragraphs(text)

        if not paragraphs:

            return {
                "ratio": None,
                "para": None,
                "confidence": 0,
            }

        # =================================================
        # IGNORE FIRST 15%
        # =================================================

        start_index = int(len(paragraphs) * 0.15)

        target_paragraphs = paragraphs[start_index:]

        best_score = 0

        best_para = None

        # =================================================
        # FIND BEST LEGAL REASONING
        # =================================================

        for para in target_paragraphs:

            score = score_ratio_paragraph(para)

            if score > best_score:

                best_score = score

                best_para = para

        # =================================================
        # RESULT
        # =================================================

        if not best_para:

            return {
                "ratio": None,
                "para": None,
                "confidence": 0,
            }

        result = {
            "ratio": best_para[:2500],
            "para": extract_para_number(best_para),
            "confidence": min(99, best_score),
        }

        print("✅ Ratio Extracted:")

        print(result)

        return result

    except Exception as e:

        print("❌ RATIO EXTRACTION ERROR:", e)

        return {
            "ratio": None,
            "para": None,
            "confidence": 0,
        }


# =========================================================
# 🔥 DIRECT TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    42. We are of the opinion that
    the conviction cannot be sustained
    in absence of credible evidence.

    Therefore, the accused is entitled
    to acquittal.
    """

    print(extract_ratio(sample))
