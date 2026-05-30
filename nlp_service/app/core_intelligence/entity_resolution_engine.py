import re
from difflib import SequenceMatcher

# =========================================================
# 🔥 NORMALIZATION
# =========================================================


def normalize_entity(text):

    if not text:
        return ""

    text = str(text).upper()

    text = re.sub(r"[^A-Z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================================================
# 🔥 FUZZY SCORE
# =========================================================


def similarity_score(a, b):

    a = normalize_entity(a)
    b = normalize_entity(b)

    if not a or not b:
        return 0

    return int(SequenceMatcher(None, a, b).ratio() * 100)


# =========================================================
# 🔥 ENTITY RESOLUTION
# =========================================================


def resolve_entities(entity_a, entity_b):

    a = normalize_entity(entity_a)
    b = normalize_entity(entity_b)

    score = similarity_score(a, b)

    same_entity = score >= 85

    match_type = "NO_MATCH"

    if same_entity:

        if score >= 98:
            match_type = "EXACT_CANONICAL_MATCH"

        elif score >= 90:
            match_type = "HIGH_CONFIDENCE_FUZZY_MATCH"

        else:
            match_type = "FUZZY_CANONICAL_MATCH"

    return {
        "entity_a": a,
        "entity_b": b,
        "same_entity": same_entity,
        "confidence": score,
        "match_type": match_type,
    }


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    result = resolve_entities("BHAGWAN DASS RAMA SHANKER", "BHAGWAN DASS RAMASHANKER")

    print(result)
