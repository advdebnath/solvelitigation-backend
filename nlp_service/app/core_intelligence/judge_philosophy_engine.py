from collections import defaultdict


# =========================================================
# 🔥 PHILOSOPHY SIGNALS
# =========================================================

PHILOSOPHY_PATTERNS = {

    "CONSTITUTIONAL_LIBERALISM": [

        "constitutional morality",
        "liberty",
        "fundamental rights",
        "expansive interpretation",
        "substantial justice",
        "human dignity",
        "beneficial interpretation"
    ],

    "STRICT_STATUTORY_APPROACH": [

        "strict interpretation",
        "literal interpretation",
        "plain meaning",
        "technical compliance",
        "narrow interpretation"
    ],

    "PROCEDURAL_FAIRNESS": [

        "natural justice",
        "fair hearing",
        "audi alteram partem",
        "due process",
        "procedural safeguard"
    ],

    "CIVIL_LIBERTY_ORIENTATION": [

        "personal liberty",
        "bail",
        "freedom",
        "article 21",
        "individual liberty"
    ],

    "PRO_REVENUE_APPROACH": [

        "tax recovery",
        "revenue interest",
        "strict tax enforcement",
        "fiscal discipline"
    ]
}


# =========================================================
# 🔥 SAFE NORMALIZER
# =========================================================

def normalize_text(text):

    if not text:
        return ""

    return str(text).lower()


# =========================================================
# 🔥 SCORE DETECTOR
# =========================================================

def detect_philosophy_scores(text):

    text = normalize_text(text)

    scores = defaultdict(int)

    for philosophy, patterns in PHILOSOPHY_PATTERNS.items():

        for pattern in patterns:

            if pattern in text:

                scores[philosophy] += 1

    return dict(scores)


# =========================================================
# 🔥 PROFILE BUILDER
# =========================================================

def build_judge_philosophy_profile(

    judge_name,

    judgments
):

    aggregate_scores = defaultdict(int)

    total_docs = 0

    for doc in judgments:

        ratio = doc.get(
            "ratio",
            ""
        )

        scores = detect_philosophy_scores(
            ratio
        )

        for key, value in scores.items():

            aggregate_scores[key] += value

        total_docs += 1

    normalized_profile = {}

    for key, value in aggregate_scores.items():

        score = int(
            (value / max(total_docs, 1)) * 35
        )

        score = min(score, 100)

        normalized_profile[key.lower()] = score

    dominant = "NEUTRAL"

    if normalized_profile:

        dominant = max(

            normalized_profile,

            key=normalized_profile.get
        ).upper()

    return {

        "judge": judge_name,

        "philosophy_profile": normalized_profile,

        "dominant_philosophy": dominant,

        "documents_analyzed": total_docs
    }


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    sample_judgments = [

        {

            "ratio": (
                "Constitutional morality and "
                "personal liberty require "
                "expansive interpretation."
            )
        },

        {

            "ratio": (
                "Natural justice and fair hearing "
                "must be protected."
            )
        }
    ]

    result = build_judge_philosophy_profile(

        judge_name="Justice Chandrachud",

        judgments=sample_judgments
    )

    print(result)
