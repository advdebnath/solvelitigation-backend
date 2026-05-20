import re

# =========================
# 🔹 KEYWORDS
# =========================

ACT_KEYWORDS = [
    "act,",
    "act ",
    "code of",
    "regulation",
    "statute"
]

RULE_KEYWORDS = [
    "rules,",
    "rules ",
    "rule ",
    "framed under"
]

NOTIFICATION_KEYWORDS = [
    "notification no",
    "gazette",
    "issued by",
    "hereby notified"
]

CIRCULAR_KEYWORDS = [
    "circular no",
    "rbi circular",
    "office memorandum",
    "guidelines issued"
]

JUDGMENT_KEYWORDS = [
    "supreme court",
    "high court",
    "judgment",
    "appellant",
    "respondent",
    "versus"
]

# =========================
# 🔥 DETECTION ENGINE
# =========================

def detect_document_type_from_text(text: str) -> str:
    if not text:
        return "JUDGMENT"

    t = text.lower()

    scores = {
        "ACT": 0,
        "RULE": 0,
        "NOTIFICATION": 0,
        "CIRCULAR": 0,
        "JUDGMENT": 0
    }

    def count_hits(keywords, label):
        for k in keywords:
            if k in t:
                scores[label] += 1

    count_hits(ACT_KEYWORDS, "ACT")
    count_hits(RULE_KEYWORDS, "RULE")
    count_hits(NOTIFICATION_KEYWORDS, "NOTIFICATION")
    count_hits(CIRCULAR_KEYWORDS, "CIRCULAR")
    count_hits(JUDGMENT_KEYWORDS, "JUDGMENT")

    # 🔥 Pick highest score
    best = max(scores, key=scores.get)

    # ⚠️ fallback safety
    if scores[best] == 0:
        return "JUDGMENT"

    return best
