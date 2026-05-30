from collections import defaultdict

# =========================================================
# 🔥 SAFE YEAR EXTRACTOR
# =========================================================


def extract_year(case_number):

    if not case_number:
        return None

    case_number = str(case_number)

    import re

    match = re.search(r"(19|20)\d{2}", case_number)

    if match:
        return int(match.group())

    return None


# =========================================================
# 🔥 STANCE DETECTOR
# =========================================================


def detect_stance(text):

    if not text:
        return "NEUTRAL"

    text = str(text).upper()

    liberal_hints = [
        "LIBERAL",
        "BENEFICIAL",
        "EXPANSIVE",
        "PURPOSIVE",
        "CONSTITUTIONAL MORALITY",
        "SUBSTANTIAL JUSTICE",
    ]

    strict_hints = [
        "STRICT",
        "LITERAL",
        "NARROW",
        "TECHNICAL",
        "LIMITED INTERPRETATION",
    ]

    liberal_score = 0
    strict_score = 0

    for hint in liberal_hints:

        if hint in text:
            liberal_score += 1

    for hint in strict_hints:

        if hint in text:
            strict_score += 1

    if liberal_score > strict_score:
        return "LIBERAL"

    if strict_score > liberal_score:
        return "STRICT"

    return "NEUTRAL"


# =========================================================
# 🔥 DOCTRINE EVOLUTION ENGINE
# =========================================================


def build_doctrine_evolution(doctrine_name, judgments):

    result = {"doctrine": doctrine_name, "timeline": [], "evolution_pattern": "STABLE"}

    if not judgments:
        return result

    timeline = []

    for doc in judgments:

        case_number = doc.get("caseNumber", "")

        year = extract_year(case_number)

        if not year:
            continue

        stance = detect_stance(doc.get("ratio", ""))

        timeline.append({"year": year, "case": case_number, "stance": stance})

    timeline = sorted(timeline, key=lambda x: x["year"])

    result["timeline"] = timeline

    # -----------------------------------------------------
    # 🔥 EVOLUTION DETECTION
    # -----------------------------------------------------

    stances = [item["stance"] for item in timeline]

    if "STRICT" in stances and "LIBERAL" in stances:

        first = stances[0]
        last = stances[-1]

        if first == "STRICT" and last == "LIBERAL":

            result["evolution_pattern"] = "STRICT_TO_LIBERAL"

        elif first == "LIBERAL" and last == "STRICT":

            result["evolution_pattern"] = "LIBERAL_TO_STRICT"

    return result


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    sample_judgments = [
        {
            "caseNumber": "1998 SLSC 10",
            "ratio": ("Strict interpretation " "must apply."),
        },
        {
            "caseNumber": "2018 SLSC 101",
            "ratio": ("Beneficial and expansive " "constitutional interpretation."),
        },
    ]

    result = build_doctrine_evolution(
        doctrine_name="REINSTATEMENT", judgments=sample_judgments
    )

    print(result)
