import re

# =========================================================
# 🔥 PRECEDENT TREATMENT WORDS
# =========================================================

TREATMENT_PATTERNS = {
    "followed": ["followed", "relied upon", "applied"],
    "distinguished": ["distinguished"],
    "overruled": ["overruled"],
    "affirmed": ["affirmed"],
    "reversed": ["reversed", "set aside"],
    "referred": ["referred to", "cited"],
}

# =========================================================
# 🔥 CASE NAME + CITATION PATTERN
# =========================================================

CASE_PATTERN = re.compile(
    r"([A-Z][A-Za-z\.\s&]+v(?:s\.?|ersus)\s*[A-Z][A-Za-z\.\s&]+)", flags=re.IGNORECASE
)

CITATION_PATTERN = re.compile(
    r"(\(\d{4}\)\s*\d+\s*SCC\s*\d+|AIR\s*\d{4}\s*SC\s*\d+|\d{4}\s*SCC\s*OnLine\s*SC\s*\d+)",
    flags=re.IGNORECASE,
)

# =========================================================
# 🔥 DETECT TREATMENT
# =========================================================


def detect_treatment(context):

    lowered = context.lower()

    for treatment, keywords in TREATMENT_PATTERNS.items():

        for keyword in keywords:

            if keyword in lowered:
                return treatment

    return "referred"


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def extract_precedents(full_text=""):

    try:

        if not isinstance(full_text, str):

            full_text = str(full_text)

        precedents = []

        seen = set()

        lines = full_text.splitlines()

        for line in lines:

            case_match = CASE_PATTERN.search(line)

            citation_match = CITATION_PATTERN.search(line)

            if not case_match:
                continue

            case_name = re.sub(r"\s+", " ", case_match.group(1)).strip()

            citation = None

            if citation_match:

                citation = re.sub(r"\s+", " ", citation_match.group(1)).strip()

            key = f"{case_name}_{citation}"

            if key in seen:
                continue

            seen.add(key)

            precedents.append(
                {
                    "case": case_name,
                    "citation": citation,
                    "treatment": detect_treatment(line),
                    "canonical": True,
                }
            )

        print("✅ Precedents Extracted:")
        print(precedents)

        return {"precedents": precedents, "count": len(precedents), "confidence": 90}

    except Exception as e:

        print("❌ Precedent Extraction Error:")
        print(str(e))

        return {"precedents": [], "count": 0, "confidence": 0}
