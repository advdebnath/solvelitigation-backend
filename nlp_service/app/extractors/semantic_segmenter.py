import re

SECTION_PATTERNS = {
    "facts": [
        r"\bfacts\b",
        r"\bbrief facts\b",
        r"\bbackground\b",
    ],
    "petitioner_arguments": [
        r"\blearned counsel for the petitioner\b",
        r"\bpetitioner submitted\b",
        r"\bit was contended\b",
    ],
    "respondent_arguments": [
        r"\blearned counsel for the respondent\b",
        r"\brespondent submitted\b",
        r"\bstate submitted\b",
    ],
    "issues": [
        r"\bquestion for consideration\b",
        r"\bpoint for determination\b",
        r"\bissues?\b",
        r"\bwhether\b",
    ],
    "analysis": [
        r"\bwe have considered\b",
        r"\bafter hearing\b",
        r"\bon perusal\b",
    ],
    "findings": [
        r"\bwe hold\b",
        r"\bwe conclude\b",
        r"\bit is held\b",
        r"\btherefore\b",
    ],
    "final_order": [
        r"\bappeal is allowed\b",
        r"\bappeal is dismissed\b",
        r"\bpetition is allowed\b",
        r"\bpetition is dismissed\b",
        r"\bordered accordingly\b",
    ],
}


def semantic_segment(text: str):

    if not text:
        return {}

    text_lower = text.lower()

    blocks = {}

    for section, patterns in SECTION_PATTERNS.items():

        matches = []

        for pattern in patterns:

            for match in re.finditer(pattern, text_lower):

                start = match.start()

                end = min(start + 5000, len(text))

                snippet = text[start:end]

                matches.append(snippet)

        blocks[section] = "\n".join(matches[:5])

    return blocks
