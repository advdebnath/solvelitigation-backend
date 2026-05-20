import re


# =========================================================
# 🔥 REASONING PATTERNS
# =========================================================

REASONING_PATTERNS = [

    r"we are of the opinion that",

    r"it is clear that",

    r"the court held that",

    r"it is settled law",

    r"therefore",

    r"accordingly",

    r"in our considered opinion",

    r"we find that",

    r"it is evident that",

    r"the legal position is"
]


# =========================================================
# 🔥 LEGAL PRINCIPLE PATTERNS
# =========================================================

LEGAL_PRINCIPLE_PATTERNS = [

    r"principle of natural justice",

    r"burden of proof",

    r"presumption of innocence",

    r"wakf property",

    r"constitutional mandate",

    r"rule of law",

    r"mens rea",

    r"proof beyond reasonable doubt",

    r"doctrine of proportionality",

    r"doctrine of legitimate expectation"
]


# =========================================================
# 🔥 CLEAN
# =========================================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# 🔥 SPLIT SENTENCES
# =========================================================

def split_sentences(text):

    return re.split(

        r'(?<=[.!?])\s+',

        text
    )


# =========================================================
# 🔥 DETECT PRINCIPLES
# =========================================================

def detect_legal_principles(text):

    principles = []

    for pattern in LEGAL_PRINCIPLE_PATTERNS:

        matches = re.findall(
            pattern,
            text,
            re.I
        )

        for match in matches:

            principle = clean_text(match)

            if principle not in principles:

                principles.append(
                    principle
                )

    return principles


# =========================================================
# 🔥 EXTRACT REASONING
# =========================================================

def extract_judicial_reasoning(text):

    try:

        text = clean_text(text)

        sentences = split_sentences(text)

        reasoning_blocks = []

        # =================================================
        # 🔥 PROCESS SENTENCES
        # =================================================

        for idx, sentence in enumerate(sentences):

            lower = sentence.lower()

            matched = False

            for pattern in REASONING_PATTERNS:

                if re.search(
                    pattern,
                    lower,
                    re.I
                ):

                    matched = True
                    break

            if not matched:
                continue

            # =============================================
            # 🔥 LOCAL REASONING WINDOW
            # =============================================

            context = " ".join(

                sentences[
                    idx:
                    min(len(sentences), idx + 2)
                ]
            )

            context = clean_text(
                context
            )

            # =============================================
            # 🔥 PRINCIPLES
            # =============================================

            principles = detect_legal_principles(
                context
            )

            reasoning_blocks.append({

                "reasoning":
                    context[:1200],

                "legal_principles":
                    principles
            })

        # =================================================
        # 🔥 REMOVE DUPLICATES
        # =================================================

        unique = []

        seen = set()

        for item in reasoning_blocks:

            key = item[
                "reasoning"
            ][:200].lower()

            if key in seen:
                continue

            seen.add(key)

            unique.append(item)

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {

            "judicial_reasoning":
                unique,

            "confidence":
                95
        }

        print(
            "✅ Judicial Reasoning Extracted:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Judicial Reasoning Error:",
            str(e)
        )

        return {

            "judicial_reasoning": [],
            "confidence": 0
        }


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    We are of the opinion that Wakf property
    cannot be alienated by the karta.

    The principle of natural justice
    requires hearing of all parties.

    Therefore, the High Court judgment
    deserves to be set aside.
    """

    print(
        extract_judicial_reasoning(sample)
    )
