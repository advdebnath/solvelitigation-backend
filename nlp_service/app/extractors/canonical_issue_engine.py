import re

CANONICAL_ISSUE_PATTERNS = {
    "Premature Release Of Life Convicts": [
        r"premature release",
        r"life convict",
        r"remission",
        r"article\s+161",
        r"life sentence",
        r"prison authorities",
    ],
    "Quashing Of Criminal Proceedings": [
        r"quash(ed|ing)?",
        r"section\s+482",
        r"criminal proceedings",
        r"fir",
        r"charge sheet",
    ],
    "Preventive Detention": [
        r"preventive detention",
        r"detenu",
        r"detention order",
        r"national security",
    ],
    "Service Reinstatement": [
        r"reinstatement",
        r"departmental proceeding",
        r"termination",
        r"dismissal from service",
    ],
    "Land Acquisition Compensation": [
        r"land acquisition",
        r"compensation",
        r"acquired land",
        r"market value",
    ],
    "Arbitration Enforcement": [
        r"arbitral award",
        r"section\s+34",
        r"section\s+37",
        r"arbitration",
    ],
}


def detect_canonical_issues(full_text):

    if not full_text:
        return {"dominant_issue": "General", "sub_issues": [], "confidence": 0}

    text = full_text.lower()

    scores = {}

    for issue, patterns in CANONICAL_ISSUE_PATTERNS.items():

        semantic_reject = False

        if issue == "Quashing Of Criminal Proceedings":

            quash_evidence = [
                "section 482",
                "482 crpc",
                "quash the proceedings",
                "criminal proceedings quashed",
                "fir quashed",
                "charge sheet quashed",
                "proceedings deserve to be quashed",
                "abuse of process",
                "inherent powers under section 482",
            ]

            evidence_hits = sum(1 for ev in quash_evidence if ev in text)

            if evidence_hits < 2:
                semantic_reject = True

        if semantic_reject:
            continue

        score = 0

        for pattern in patterns:

            matches = re.findall(pattern, text)

            score += len(matches) * 15

        if score > 0:
            scores[issue] = score

    if not scores:

        return {"dominant_issue": "General", "sub_issues": [], "confidence": 25}

    dominant_issue = max(scores, key=scores.get)

    sub_issues = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[1:5]

    confidence = min(95, scores[dominant_issue])

    return {
        "dominant_issue": dominant_issue,
        "sub_issues": sub_issues,
        "confidence": confidence,
    }
