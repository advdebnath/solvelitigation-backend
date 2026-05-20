import re
from typing import Dict


# =========================================================
# 🔥 JURISPRUDENTIAL ROLE PATTERNS
# =========================================================

ROLE_PATTERNS = {

    "FACTS": [

        r"\bfacts?\b",
        r"\bbrief facts\b",
        r"\bbackground\b",
        r"\bthe prosecution case\b",
        r"\bit is alleged\b",
        r"\baccording to the plaintiff\b",
        r"\bthe case of the plaintiff\b",
        r"\bthe case of the prosecution\b",
        r"\bit was pleaded\b",
        r"\bit was asserted\b",
        r"\bit is stated\b",
        r"\bthe respondent contended\b",
        r"\bthe appellant contended\b",
    ],

    "PROCEDURAL_HISTORY": [

        r"\bchallenge in the present appeal\b",
        r"\bappeal is directed against\b",
        r"\bimpugned judgment\b",
        r"\border passed by the high court\b",
        r"\bhigh court held\b",
        r"\btrial court held\b",
        r"\bwrit petition\b",
        r"\brevision petition\b",
        r"\bpetition was allowed\b",
        r"\bpetition was dismissed\b",
        r"\bsuit was filed\b",
        r"\bapplication was filed\b",
        r"\bthe present appeal arises\b",
        r"\baggrieved by the judgment\b",
        r"\blearned single judge\b",
        r"\bdivision bench\b",
        r"\btribunal held\b",
    ],

    "ARGUMENT": [

        r"\blearned counsel\b",
        r"\bsubmitted\b",
        r"\bcontended\b",
        r"\bargued\b",
        r"\bit was urged\b",
    ],

    "ISSUE": [

        r"\bquestion for consideration\b",
        r"\bissue\b",
        r"\bpoint for determination\b",
    ],

    "PRECEDENT": [

        r"\brelied upon\b",
        r"\bplaced reliance\b",
        r"\b[A-Z][A-Za-z]+\s+v\.\s+[A-Z]",
        r"\bthis court held\b",
    ],

    "DOCTRINE": [

        r"\bit is well settled\b",
        r"\bsettled law\b",
        r"\bthe legal position\b",
    ],

    "ANALYSIS": [

        r"\bwe have considered\b",
        r"\bon perusal\b",
        r"\bafter hearing\b",
        r"\bin our opinion\b",
        r"\bwe are of the view\b",
    ],

    "FINDING": [

        r"\bwe are satisfied\b",
        r"\bwe find\b",
        r"\bwe are of the opinion\b",
        r"\bwe are convinced\b",
        r"\bthere is no merit\b",
        r"\bthe contention cannot be accepted\b",
        r"\bthe submission is rejected\b",
    ],

    "RATIO": [

        r"\bwe hold\b",
        r"\bwe accordingly hold\b",
        r"\bit is held\b",
        r"\btherefore held\b",
        r"\bthus held\b",
        r"\bthe law laid down\b",
        r"\bthe legal principle\b",
        r"\bwe conclude\b",
        r"\bwe find that\b",
        r"\bit follows that\b",
    ],

    "OPERATIVE": [

        r"\bappeal is allowed\b",
        r"\bappeal is dismissed\b",
        r"\bpetition is allowed\b",
        r"\bpetition is dismissed\b",
        r"\bordered accordingly\b",
        r"\bconviction upheld\b",
        r"\bacquitted\b",
        r"\bset aside\b",
        r"\bquashed\b",
    ]
}



# =========================================================
# 🔥 MAIN ROLE CLASSIFIER
# =========================================================

def classify_sentence_role(sentence: str) -> Dict:

    if not sentence:

        return {

            "role": "UNKNOWN",
            "confidence": 0,
            "matched_patterns": []
        }

    lower = sentence.lower()

    sentence_length = len(
        sentence.split()
    )

    best_role = "UNKNOWN"

    best_score = 0

    matched_patterns = []

    for role, patterns in ROLE_PATTERNS.items():

        score = 0

        role_matches = []

        for pattern in patterns:

            if re.search(pattern, lower):

                score += 25

                role_matches.append(pattern)

        if len(role_matches) >= 2:

            score += 15

        if role in [
            "OPERATIVE",
            "RATIO",
            "FINDING"
        ]:

            score += 10

        if sentence_length > 80:

            score += 5

        if score > best_score:

            best_score = score

            best_role = role

            matched_patterns = role_matches

    return {

        "role": best_role,

        "confidence": min(best_score, 95),

        "matched_patterns": matched_patterns
    }

