# =========================================================
# 🔥 TEMPORAL JURISPRUDENCE EVOLUTION ENGINE
# =========================================================

import re

# =========================================================
# 🔥 TEMPORAL DOCTRINE SIGNALS
# =========================================================

TEMPORAL_PATTERNS = {
    "Article 21 Expansion": [
        r"right\s+to\s+privacy",
        r"dignity",
        r"personal\s+liberty",
        r"constitutional\s+morality",
    ],
    "Minimal Arbitration Interference": [
        r"limited\s+scope\s+of\s+interference",
        r"arbitral\s+award",
        r"judicial\s+restraint",
        r"section\s+34",
    ],
    "Liberty Oriented Bail Jurisprudence": [
        r"bail\s+is\s+the\s+rule",
        r"personal\s+liberty",
        r"article\s+21",
        r"custodial\s+interrogation",
    ],
    "Natural Justice Expansion": [
        r"natural\s+justice",
        r"audi\s+alteram\s+partem",
        r"fair\s+hearing",
        r"procedural\s+fairness",
    ],
    "Strict NI Act Enforcement": [
        r"legally\s+enforceable\s+debt",
        r"presumption\s+under\s+section\s+139",
        r"cheque\s+dishonour",
        r"burden\s+of\s+proof",
    ],
}


# =========================================================
# 🔥 CLEAN TEXT
# =========================================================


def normalize_text(text):

    text = re.sub(r"\s+", " ", str(text))

    return text.strip().lower()


# =========================================================
# 🔥 DETECT TEMPORAL DOCTRINES
# =========================================================


def detect_temporal_doctrines(text):

    text = normalize_text(text)

    findings = []

    for doctrine, patterns in TEMPORAL_PATTERNS.items():

        score = 0

        matched = []

        for pattern in patterns:

            results = re.findall(pattern, text, re.I)

            if results:

                score += len(results) * 10

                matched.extend(results)

        if score > 0:

            findings.append(
                {
                    "doctrine": doctrine,
                    "score": min(score, 100),
                    "signals": list(set(matched)),
                }
            )

    return findings


# =========================================================
# 🔥 BUILD TEMPORAL EVOLUTION
# =========================================================


def build_temporal_jurisprudence(
    full_text="", judgment_date=None, dominant_issue=None, judges=None
):

    try:

        dominant_issue = str(dominant_issue).strip() or "General"

        temporal_data = {
            "judgment_year": None,
            "dominant_issue": dominant_issue,
            "doctrinal_movements": [],
            "dominant_doctrine": "General",
            "judges": judges or [],
            "confidence": 0,
        }

        # -------------------------------------------------
        # YEAR EXTRACTION
        # -------------------------------------------------

        if isinstance(judgment_date, dict):

            raw_date = str(judgment_date.get("date", ""))

            year_match = re.search(r"(19|20)\d{2}", raw_date)

            if year_match:

                temporal_data["judgment_year"] = year_match.group(0)

        # -------------------------------------------------
        # DOMINANT ISSUE
        # -------------------------------------------------

        if isinstance(dominant_issue, dict):

            temporal_data["dominant_issue"] = dominant_issue.get(
                "dominant_issue", "General"
            )

        # -------------------------------------------------
        # DOCTRINE DETECTION
        # -------------------------------------------------

        doctrines = detect_temporal_doctrines(full_text)

        temporal_data["doctrinal_movements"] = doctrines

        # -------------------------------------------------
        # DOMINANT DOCTRINE
        # -------------------------------------------------

        top_score = 0

        dominant_doctrine = "General"

        for item in doctrines:

            score = item.get("score", 0)

            if score > top_score:

                top_score = score

                dominant_doctrine = item.get("doctrine", "General")

        temporal_data["dominant_doctrine"] = dominant_doctrine

        temporal_data["confidence"] = min(95, 50 + top_score)

        print("✅ Temporal Jurisprudence:")

        print(temporal_data)

        return temporal_data

    except Exception as e:

        print("❌ Temporal Jurisprudence Error:", str(e))

        return {
            "judgment_year": None,
            "dominant_issue": "General",
            "doctrinal_movements": [],
            "dominant_doctrine": "General",
            "judges": judges or [],
            "confidence": 0,
        }
