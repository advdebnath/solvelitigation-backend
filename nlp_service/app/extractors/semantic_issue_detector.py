import re

ISSUE_PATTERNS = [

    r"whether\s+.*?\.",
    r"question\s+for\s+consideration.*?\.",
    r"point[s]?\s+for\s+determination.*?\.",
    r"short\s+question.*?\.",
    r"core\s+issue.*?\.",
    r"controversy\s+involved.*?\.",
    r"substantial\s+question\s+of\s+law.*?\.",
]

ISSUE_TYPES = {

    "natural justice": "natural_justice",
    "jurisdiction": "jurisdiction",
    "limitation": "limitation",
    "termination": "service_termination",
    "dismissal": "service_termination",
    "bail": "bail",
    "quashing": "quashing",
    "arbitration": "arbitration",
    "contract": "contract_breach",
    "evidence": "evidence",
    "circumstantial evidence": "evidence",
    "assessment": "tax_assessment",
    "premature release": "premature_release",
    "life convict": "premature_release",
    "remission": "premature_release",
    "article 161": "premature_release",
    "clemency": "premature_release",
    "reformative justice": "premature_release",
    "prison conduct": "premature_release",
}


def classify_issue(issue_text: str):

    issue_lower = issue_text.lower()

    for keyword, label in ISSUE_TYPES.items():

        if keyword in issue_lower:
            return label

    return "general"


def detect_semantic_issues(text: str):

    if not text:
        return []

    issues = []

    text = re.sub(r"\s+", " ", text)

    for pattern in ISSUE_PATTERNS:

        matches = re.findall(pattern, text, flags=re.I)

        for match in matches:

            issue = match.strip()

            if len(issue) < 25:
                continue

            issues.append({

                "issue": issue,

                "normalizedIssue": issue.lower(),

                "issueType": classify_issue(issue),

                "confidence": 85
            })

    unique = []

    seen = set()

    for item in issues:

        key = item["normalizedIssue"]

        if key not in seen:

            seen.add(key)

            unique.append(item)

 
    # =====================================================
    # 🔥 REMISSION JURISPRUDENCE PRIORITY BOOST
    # =====================================================

    remission_signals = [
        "premature release",
        "life convict",
        "remission",
        "article 161",
        "clemency",
        "reformative justice"
    ]

    remission_hits = 0

    lower_text = text.lower()

    for signal in remission_signals:

        if signal in lower_text:

           remission_hits += 1

    if remission_hits >= 2:

        for item in unique:

           if item.get("issueType") == "premature_release":

              item["confidence"] += remission_hits * 10

    unique.sort(
        key=lambda x: x.get("confidence", 0),
        reverse=True
    )

    return unique[:20]
