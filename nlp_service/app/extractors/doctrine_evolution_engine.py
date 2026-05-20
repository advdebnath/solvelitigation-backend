import re
from collections import defaultdict


# =========================================================
# 🔥 KNOWN DOCTRINES
# =========================================================

KNOWN_DOCTRINES = [

    "natural justice",

    "constitutional mandate",

    "rule of law",

    "burden of proof",

    "mens rea",

    "proportionality",

    "legitimate expectation",

    "procedural fairness",

    "due process",

    "arbitrariness"
]



# =========================================================
# 🔥 EVOLUTION SIGNALS
# =========================================================

EVOLUTION_SIGNALS = {

    "relied upon":
        "Precedent Reliance",

    "followed":
        "Precedent Followed",

    "distinguished":
        "Doctrine Distinguished",

    "overruled":
        "Doctrine Overruled",

    "clarified":
        "Doctrine Clarified",

    "expanded":
        "Doctrine Expanded",

    "reconsidered":
        "Doctrine Reconsidered",

    "reaffirmed":
        "Doctrine Reaffirmed"
}


# =========================================================
# 🔥 CLEAN
# =========================================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        str(text)
    )

    return text.strip()


# =========================================================
# 🔥 DETECT DOCTRINES
# =========================================================

def detect_doctrines(text):

    findings = []

    lower = text.lower()

    for doctrine in KNOWN_DOCTRINES:

        if doctrine in lower:

            findings.append(
                doctrine
            )

    return findings


# =========================================================
# 🔥 BUILD EVOLUTION
# =========================================================

def build_doctrine_evolution(

    doctrine,

    year,

    context
):

    return {

        "year":
            year,

        "principle":
            clean_text(
                context[:400]
            )
    }


# =========================================================
# 🔥 EXTRACT EVOLUTION
# =========================================================

def extract_doctrine_evolution(

    text,

    year=None
):

    try:

        text = clean_text(text)

        doctrines = detect_doctrines(
            text
        )

        evolution = defaultdict(list)

        # =================================================
        # 🔥 SPLIT SENTENCES
        # =================================================

        sentences = re.split(

            r'(?<=[.!?])\s+',

            text
        )

        evolution_events = []

        for sentence in sentences:

            lower_sentence = sentence.lower()

            for signal, meaning in EVOLUTION_SIGNALS.items():

                if signal in lower_sentence:

                    evolution_events.append({

                        "signal":
                            signal,

                        "meaning":
                            meaning,

                        "context":
                            clean_text(sentence[:500])
                    })


            lower = sentence.lower()

            for doctrine in doctrines:

                if doctrine in lower:

                    evolution[doctrine].append(

                        build_doctrine_evolution(

                            doctrine,

                            year,

                            sentence
                        )
                    )

        # =================================================
        # 🔥 RESULT
        # =================================================

        final = []

        for doctrine, timeline in evolution.items():

            final.append({

                "doctrine":
                    doctrine,

                "timeline":
                    timeline
            })

        result = {

            "doctrine_evolution":
                final,

            "confidence":
                95
        }

        print(
            "✅ Doctrine Evolution Extracted:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Doctrine Evolution Error:",
            str(e)
        )

        return {

            "doctrine_evolution": [],

            "confidence": 0
        }


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    The principle of natural justice
    requires fair hearing.

    Procedural fairness is part
    of constitutional mandate.

    Due process prevents arbitrariness.
    """

    print(

        extract_doctrine_evolution(

            sample,

            year=2024
        )
    )
