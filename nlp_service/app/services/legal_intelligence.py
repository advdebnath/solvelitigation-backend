import re


# =========================================
# 🔥 CLEAN TEXT (GLOBAL FIX)
# =========================================
def clean_text(text: str):
    return (
        text.replace("\xa0", " ")
        .replace("\n", " ")
        .replace("\t", " ")
        .strip()
    )


# =========================================
# 🔥 SENTENCE EXTRACTION (VERY IMPORTANT)
# =========================================
def extract_sentences(text: str):
    text = clean_text(text)

    sentences = re.split(r'(?<=[.!?])\s+', text)

    # filter meaningful sentences
    return [
        s.strip()
        for s in sentences
        if len(s.strip()) > 40
    ]


# =========================================
# 🔥 ARGUMENT EXTRACTION (IMPROVED)
# =========================================
def extract_arguments(text: str):
    sentences = extract_sentences(text)

    appellant = []
    respondent = []

    for s in sentences:
        s_lower = s.lower()

        if any(k in s_lower for k in [
            "counsel for the appellant",
            "appellant submitted",
            "it is contended",
        ]):
            appellant.append(s)

        if any(k in s_lower for k in [
            "counsel for the respondent",
            "respondent submitted",
            "on the other hand",
        ]):
            respondent.append(s)

    return {
        "appellant": list(set(appellant))[:5] or ["Arguments inferred"],
        "respondent": list(set(respondent))[:5] or ["Arguments inferred"],
    }


# =========================================
# 🔥 ISSUE DETECTION (IMPROVED)
# =========================================
def extract_issue(text: str):
    sentences = extract_sentences(text)

    for s in sentences:
        s_lower = s.lower()

        if any(k in s_lower for k in [
            "whether",
            "the question is",
            "issue is",
        ]):
            return s.strip()

    return "Legal issue inferred from context"


# =========================================
# 🔥 RATIO DECIDENDI (UPGRADED)
# =========================================
def extract_ratio(text: str):
    sentences = extract_sentences(text)

    ratio = []

    for s in sentences:
        s_lower = s.lower()

        if any(k in s_lower for k in [
            "held that",
            "it is settled",
            "it is clear that",
            "we hold",
            "therefore",
            "thus",
        ]):
            ratio.append(s)

    # remove duplicates
    ratio = list(dict.fromkeys(ratio))

    return ratio[:5] or ["Ratio inferred from judgment"]


# =========================================
# 🔥 REASONING EXTRACTION (UPGRADED)
# =========================================
def extract_reasoning(text: str):
    sentences = extract_sentences(text)

    reasoning = []

    for s in sentences:
        s_lower = s.lower()

        if any(k in s_lower for k in [
            "because",
            "in view of",
            "it is evident",
            "we find",
            "thus",
            "therefore",
        ]):
            # ❌ avoid statute-only lines
            if any(x in s_lower for x in ["section", "article", "rule"]):
                continue

            reasoning.append(s)

    # remove duplicates
    reasoning = list(dict.fromkeys(reasoning))

    return reasoning[:5] or sentences[:2]


# =========================================
# 🔥 CITATION EXTRACTION (IMPROVED)
# =========================================
def extract_citations(text: str):
    pattern = r"[A-Z][a-zA-Z]+ v\. [A-Z][a-zA-Z]+"
    matches = re.findall(pattern, text)

    return list(set(matches))


# =========================================
# 🔥 MAIN INTELLIGENCE ENGINE
# =========================================
def build_legal_intelligence(text: str):
    text = clean_text(text)

    return {
        "arguments": extract_arguments(text),
        "issue": extract_issue(text),
        "ratio": extract_ratio(text),
        "reasoning": extract_reasoning(text),
        "citations": extract_citations(text),
    }
