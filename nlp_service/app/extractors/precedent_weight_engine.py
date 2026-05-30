import re

# =========================================================
# 🔥 PRECEDENT VALUE WEIGHTS
# =========================================================

VALUE_WEIGHTS = {
    "Relied On": 30,
    "Followed": 25,
    "Approved": 24,
    "Distinguished": 15,
    "Referred": 10,
    "Reversed": 5,
    "Overruled": 0,
}


# =========================================================
# 🔥 COURT LEVEL WEIGHTS
# =========================================================

COURT_WEIGHTS = {"Supreme Court": 40, "High Court": 25, "Tribunal": 10}


# =========================================================
# 🔥 DETECT COURT LEVEL
# =========================================================


def detect_court_level(citation):

    citation = citation.upper()

    if "SC" in citation:

        return "Supreme Court"

    if "HC" in citation:

        return "High Court"

    return "Tribunal"


# =========================================================
# 🔥 DETECT CONSTITUTION BENCH
# =========================================================


def detect_constitution_bench(context):

    patterns = [
        r"constitution\s+bench",
        r"five[- ]judge",
        r"seven[- ]judge",
        r"nine[- ]judge",
    ]

    for pattern in patterns:

        if re.search(pattern, context, re.I):

            return True

    return False


# =========================================================
# 🔥 CALCULATE WEIGHT
# =========================================================


def calculate_precedent_weight(precedent):

    citation = precedent.get("citation", "")

    value = precedent.get("precedent_value", "Referred")

    context = precedent.get("context", "")

    # =====================================================
    # 🔥 BASE VALUE
    # =====================================================

    weight = VALUE_WEIGHTS.get(value, 10)

    # =====================================================
    # 🔥 COURT LEVEL
    # =====================================================

    court_level = detect_court_level(citation)

    weight += COURT_WEIGHTS.get(court_level, 0)

    # =====================================================
    # 🔥 CONSTITUTION BENCH BOOST
    # =====================================================

    constitution_bench = detect_constitution_bench(context)

    if constitution_bench:

        weight += 20

    # =====================================================
    # 🔥 NORMALIZE
    # =====================================================

    weight = min(weight, 100)

    authority_strength = "Weak"

    if weight >= 80:

        authority_strength = "Very Strong"

    elif weight >= 60:

        authority_strength = "Strong"

    elif weight >= 40:

        authority_strength = "Moderate"

    # =====================================================
    # 🔥 RESULT
    # =====================================================

    result = {
        "citation": citation,
        "precedent_value": value,
        "court_level": court_level,
        "constitution_bench": constitution_bench,
        "precedent_weight": weight,
        "authority_strength": authority_strength,
        "context": context[:500],
    }

    return result


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def rank_precedents(precedents):

    try:

        ranked = []

        for precedent in precedents:

            ranked.append(calculate_precedent_weight(precedent))

        ranked.sort(key=lambda x: x["precedent_weight"], reverse=True)

        result = {"ranked_precedents": ranked, "confidence": 95}

        print("✅ Precedent Weight Engine:")

        print(result)

        return result

    except Exception as e:

        print("❌ Precedent Weight Error:", str(e))

        return {"ranked_precedents": [], "confidence": 0}


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = [
        {
            "citation": "AIR 1967 SC 574",
            "precedent_value": "Relied On",
            "context": "Constitution Bench relied on AIR 1967 SC 574",
        },
        {
            "citation": "(2010) 8 SCC 726",
            "precedent_value": "Followed",
            "context": "The judgment was followed",
        },
        {
            "citation": "AIR 1958 HC 141",
            "precedent_value": "Distinguished",
            "context": "Distinguished on facts",
        },
    ]

    print(rank_precedents(sample))
