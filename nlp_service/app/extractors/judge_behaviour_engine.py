# =========================================================
# 🔥 JUDGE BEHAVIOURAL INTELLIGENCE ENGINE
# =========================================================

import re


# =========================================================
# 🔥 TRAIT SIGNALS
# =========================================================

TRAIT_PATTERNS = {

    "Liberty Oriented": [

        r"bail\s+granted",

        r"personal\s+liberty",

        r"article\s+21",

        r"liberty\s+of\s+the\s+accused"
    ],

    "Strict Proceduralist": [

        r"procedural\s+compliance",

        r"mandatory\s+requirement",

        r"statutory\s+mandate",

        r"non-compliance"
    ],

    "Constitutional Activist": [

        r"constitutional\s+morality",

        r"transformative\s+constitution",

        r"fundamental\s+rights",

        r"article\s+14",

        r"article\s+21"
    ],

    "Textualist": [

        r"plain\s+language",

        r"literal\s+interpretation",

        r"strict\s+interpretation",

        r"legislative\s+intent"
    ],

    "Administrative Protective": [

        r"tribunal\s+restored",

        r"administrative\s+fairness",

        r"natural\s+justice",

        r"administrative\s+authority"
    ],

    "Evidence Sensitive": [

        r"benefit\s+of\s+doubt",

        r"circumstantial\s+evidence",

        r"prosecution\s+failed",

        r"evidence\s+insufficient"
    ]
}


# =========================================================
# 🔥 CLEAN TEXT
# =========================================================

def normalize_text(text):

    text = re.sub(
        r"\s+",
        " ",
        str(text)
    )

    return text.strip().lower()


# =========================================================
# 🔥 DETECT TRAITS
# =========================================================

def detect_behaviour_traits(text):

    text = normalize_text(text)

    findings = {}

    for trait, patterns in TRAIT_PATTERNS.items():

        score = 0

        matches_found = []

        for pattern in patterns:

            matches = re.findall(
                pattern,
                text,
                re.I
            )

            if matches:

                score += len(matches) * 10

                matches_found.extend(matches)

        if score > 0:

            findings[trait] = {

                "score":
                    min(score, 100),

                "signals":
                    list(set(matches_found))
            }

    return findings


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================

def analyze_judge_behaviour(

    full_text="",
    judges=None,
    operative_data=None,
    dominant_issue=None
):

    try:

        behaviour = {

            "judges":
                judges or [],

            "traits":
                {},

            "dominant_behaviour":
                "Neutral",

            "confidence":
                0
        }

        # -------------------------------------------------
        # DETECT TRAITS
        # -------------------------------------------------

        traits = detect_behaviour_traits(
            full_text
        )

        behaviour["traits"] = traits

        # -------------------------------------------------
        # DOMINANT TRAIT
        # -------------------------------------------------

        highest_score = 0

        dominant_trait = "Neutral"

        for trait, data in traits.items():

            score = data.get(
                "score",
                0
            )

            if score > highest_score:

                highest_score = score

                dominant_trait = trait

        behaviour[
            "dominant_behaviour"
        ] = dominant_trait

        behaviour[
            "confidence"
        ] = min(

            95,

            50 + highest_score
        )

        # -------------------------------------------------
        # ISSUE AWARENESS
        # -------------------------------------------------

        if isinstance(dominant_issue, dict):

            behaviour[
                "dominant_issue"
            ] = dominant_issue.get(
                "dominant_issue",
                "General"
            )

        # -------------------------------------------------
        # OPERATIVE AWARENESS
        # -------------------------------------------------

        if isinstance(operative_data, dict):

            behaviour[
                "operative_holding"
            ] = operative_data.get(
                "final_holding",
                "Unknown"
            )

        print(
            "✅ Judge Behaviour Analysis:"
        )

        print(behaviour)

        return behaviour

    except Exception as e:

        print(
            "❌ Judge Behaviour Error:",
            str(e)
        )

        return {

            "judges":
                judges or [],

            "traits":
                {},

            "dominant_behaviour":
                "Neutral",

            "confidence":
                0
        }
