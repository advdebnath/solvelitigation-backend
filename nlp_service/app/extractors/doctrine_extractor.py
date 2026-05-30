import re

# =========================================================
# 🔥 CANONICAL DOCTRINE PATTERNS
# =========================================================

DOCTRINE_PATTERNS = {
    "Doctrine Of Natural Justice": [
        r"natural justice",
        r"audi alteram partem",
        r"bias",
        r"nemo judex",
    ],
    "Doctrine Of Proportionality": [
        r"proportionality",
        r"proportionate punishment",
        r"disproportionate",
    ],
    "Doctrine Of Legitimate Expectation": [r"legitimate expectation"],
    "Doctrine Of Basic Structure": [r"basic structure"],
    "Doctrine Of Severability": [r"severability"],
    "Doctrine Of Eclipse": [r"doctrine of eclipse"],
    "Doctrine Of Waiver": [r"waiver", r"waived"],
    "Doctrine Of Estoppel": [r"estoppel", r"promissory estoppel"],
    "Doctrine Of Ultra Vires": [r"ultra vires"],
    "Doctrine Of Res Judicata": [r"res judicata"],
    "Doctrine Of Laches": [r"laches", r"delay and laches"],
    "Doctrine Of Pith And Substance": [r"pith and substance"],
    "Doctrine Of Colourable Legislation": [r"colourable legislation"],
}

# =========================================================
# 🔥 DETECT DOCTRINE
# =========================================================


def detect_doctrine_context(text, doctrine_name):

    lowered = text.lower()

    score = 0

    keywords = doctrine_name.lower().split()

    for keyword in keywords:

        if keyword in lowered:
            score += 10

    return min(score, 100)


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def extract_doctrines(full_text=""):

    try:

        if not isinstance(full_text, str):

            full_text = str(full_text)

        lowered = full_text.lower()

        doctrines = []

        seen = set()

        for doctrine, patterns in DOCTRINE_PATTERNS.items():

            matched = False

            for pattern in patterns:

                if re.search(pattern, lowered, flags=re.IGNORECASE):

                    matched = True
                    break

            if not matched:
                continue

            if doctrine in seen:
                continue

            seen.add(doctrine)

            doctrines.append(
                {
                    "doctrine": doctrine,
                    "confidence": detect_doctrine_context(lowered, doctrine),
                    "canonical": True,
                }
            )

        print("✅ Doctrines Extracted:")
        print(doctrines)

        return {
            "doctrine_evolution": doctrines,
            "count": len(doctrines),
            "confidence": 90,
        }

    except Exception as e:

        print("❌ Doctrine Extraction Error:")
        print(str(e))

        return {"doctrine_evolution": [], "count": 0, "confidence": 0}
