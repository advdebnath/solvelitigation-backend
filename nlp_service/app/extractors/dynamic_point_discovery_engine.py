import re
from collections import Counter


STOP_TERMS = {
    "court",
    "appeal",
    "judge",
    "learned",
    "petitioner",
    "respondent",
    "appellant",
    "order",
    "judgment",
    "paragraph",
    "therefore",
    "however"
}


def discover_dynamic_points(
    full_text="",
    semantic_issues=None
):

    try:

        if not full_text:

            return {
                "dynamic_points": []
            }

        text = full_text.lower()

        phrase_matches = re.findall(
            r"\b[a-z]{4,}(?:\s+[a-z]{4,}){1,4}\b",
            text
        )

        cleaned = []

        for phrase in phrase_matches:

            phrase = phrase.strip()

            words = phrase.split()

            if any(
                word in STOP_TERMS
                for word in words
            ):
                continue

            if len(words) < 2:
                continue

            cleaned.append(phrase)

        freq = Counter(cleaned)

        candidates = []

        for phrase, count in freq.most_common(20):

            if count < 3:
                continue

            candidates.append({
                "candidate_point": phrase.title(),
                "frequency": count,
                "confidence": min(
                    95,
                    40 + count * 5
                )
            })

        return {
            "dynamic_points": candidates
        }

    except Exception as e:

        print("❌ DYNAMIC POINT DISCOVERY ERROR:")
        print(str(e))

        return {
            "dynamic_points": []
        }
