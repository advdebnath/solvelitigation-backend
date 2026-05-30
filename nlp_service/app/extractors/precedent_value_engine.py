import re

# =========================================================
# 🔥 PRECEDENT VALUE PATTERNS
# =========================================================

PRECEDENT_PATTERNS = {
    "Relied On": [
        r"relied\s+on",
        r"placed\s+reliance\s+upon",
        r"reliance\s+placed\s+on",
        r"reliance\s+was\s+placed\s+on",
        r"following\s+the\s+decision\s+in",
    ],
    "Followed": [r"\bfollowed\b", r"we\s+follow", r"respectfully\s+followed"],
    "Distinguished": [
        r"\bdistinguished\b",
        r"clearly\s+distinguishable",
        r"facts\s+are\s+different",
        r"distinguishable\s+on\s+facts",
    ],
    "Overruled": [r"\boverruled\b", r"no\s+longer\s+good\s+law"],
    "Approved": [r"\bapproved\b", r"approval\s+of"],
    "Reversed": [r"\breversed\b", r"set\s+aside"],
    "Referred": [r"referred\s+to", r"reference\s+made\s+to", r"\bcited\b"],
}


# =========================================================
# 🔥 CITATION REGEX
# =========================================================

CITATION_REGEX = re.compile(
    r"(AIR\s+\d{4}\s+SC\s+\d+)" r"|" r"(\(\d{4}\)\s+\d+\s+SCC\s+\d+)", re.I
)


# =========================================================
# 🔥 CLEAN TEXT
# =========================================================


def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 DETECT PRECEDENT VALUE
# =========================================================


def detect_precedent_value(context):

    precedent_type = "Referred"

    best_score = 0

    for label, patterns in PRECEDENT_PATTERNS.items():

        local_score = 0

        for pattern in patterns:

            matches = re.findall(pattern, context, re.I)

            local_score += len(matches)

        if local_score > best_score:

            best_score = local_score

            precedent_type = label

    return precedent_type


# =========================================================
# 🔥 EXTRACT PRECEDENT VALUES
# =========================================================


def extract_precedent_values(text):

    try:

        text = clean_text(text)

        # =================================================
        # 🔥 SENTENCE SPLIT
        # =================================================

        sentences = re.split(r"(?<=[.!?])\s+", text)

        precedents = []

        # =================================================
        # 🔥 PROCESS SENTENCES
        # =================================================

        for sentence in sentences:

            citations = CITATION_REGEX.findall(sentence)

            if not citations:
                continue

            context = sentence.strip()

            precedent_type = detect_precedent_value(context)

            citation_texts = []

            for group in citations:

                for c in group:

                    if c:

                        citation_texts.append(c.strip())

            for citation in citation_texts:

                precedents.append(
                    {
                        "citation": citation,
                        "precedent_value": precedent_type,
                        "context": context[:500],
                    }
                )

        # =================================================
        # 🔥 REMOVE DUPLICATES
        # =================================================

        unique = []

        seen = set()

        for item in precedents:

            key = (item["citation"].lower(), item["precedent_value"].lower())

            if key in seen:
                continue

            seen.add(key)

            unique.append(item)

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {"precedents": unique, "confidence": 95}

        print("✅ Precedent Values Extracted:")

        print(result)

        return result

    except Exception as e:

        print("❌ Precedent Engine Error:", str(e))

        return {"precedents": [], "confidence": 0}


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = """
    Reliance was placed on AIR 1967 SC 574.
    The judgment reported in (2010) 8 SCC 726 was followed.
    AIR 1958 SC 141 is distinguished on facts.
    """

    print(extract_precedent_values(sample))
