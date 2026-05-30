import re
from collections import Counter

# =========================================================
# 🔥 LEGAL ISSUE ONTOLOGY
# =========================================================

ISSUE_ONTOLOGY = {
    # =====================================================
    # 🔥 CIVIL
    # =====================================================
    "Civil": {
        "Wakf Property Dispute": [r"\bwakf\b", r"\bwakf tribunal\b", r"\bmutawalli\b"],
        "Tenancy Surrender": [r"\bsurrender\b", r"\btenant\b", r"\btenancy\b"],
        "Joint Hindu Family": [
            r"\bjoint hindu family\b",
            r"\bkarta\b",
            r"\bcoparcener\b",
        ],
        "Lease Dispute": [
            r"\blease deed\b",
            r"\blessor\b",
            r"\blessee\b",
            r"\bmonthly rent\b",
            r"\brent agreement\b",
        ],
        "Specific Performance": [
            r"\bspecific performance\b",
            r"\bagreement to sell\b",
            r"\bready and willing\b",
        ],
    },
    # =====================================================
    # 🔥 CRIMINAL
    # =====================================================
    "Criminal": {
        "Murder": [r"\bsection 302\b", r"\bmurder\b", r"\bhomicide\b"],
        "Bail": [r"\bbail\b", r"\banticipatory bail\b", r"\bregular bail\b"],
        "Cheque Bounce": [
            r"\bsection 138\b",
            r"\bnegotiable instruments act\b",
            r"\bcheque dishonou?r\b",
        ],
        "NDPS Recovery": [
            r"\bndps act\b",
            r"\bnarcotic drugs\b",
            r"\bpsychotropic substances\b",
            r"\bganja\b",
            r"\bheroin\b",
            r"\bcocaine\b",
        ],
        "Criminal Procedure": [r"\bsection 482\b", r"\bcrpc\b", r"\bquashing of fir\b"],
    },
    # =====================================================
    # 🔥 TAXATION
    # =====================================================
    "Taxation": {
        "Income Tax Assessment": [
            r"\bincome tax\b",
            r"\bassessment\b",
            r"\breassessment\b",
            r"\bsection 147\b",
            r"\bsection 148\b",
            r"\bassessee\b",
            r"\bassessment year\b",
        ],
        "GST Dispute": [
            r"\bgst\b",
            r"\bcgst\b",
            r"\binput tax credit\b",
            r"\bsection 74\b",
        ],
        "Transfer Pricing": [r"\btransfer pricing\b", r"\balp\b", r"\barms length\b"],
        "Tax Tribunal Appeal": [
            r"\bitat\b",
            r"\bincome tax appellate tribunal\b",
            r"\btribunal\b",
        ],
    },
    # =====================================================
    # 🔥 SERVICE
    # =====================================================
    "Service": {
        "Departmental Proceeding": [
            r"\bdepartmental proceeding\b",
            r"\bdisciplinary proceeding\b",
            r"\bcharge sheet\b",
        ],
        "Termination": [
            r"\btermination\b",
            r"\bdismissal from service\b",
            r"\bremoval from service\b",
        ],
        "Reinstatement": [r"\breinstatement\b", r"\breinstated in service\b"],
    },
    # =====================================================
    # 🔥 CONSTITUTIONAL
    # =====================================================
    "Constitutional": {
        "Constitutional Jurisdiction": [
            r"\barticle 226\b",
            r"\barticle 227\b",
            r"\bwrit petition\b",
        ],
        "Fundamental Rights": [
            r"\barticle 14\b",
            r"\barticle 19\b",
            r"\barticle 21\b",
            r"\bfundamental rights\b",
        ],
    },
}

# =========================================================
# 🔥 ISSUE WEIGHTS
# =========================================================

ISSUE_WEIGHTS = {
    "Wakf Property Dispute": 10,
    "Tenancy Surrender": 9,
    "Joint Hindu Family": 9,
    "Lease Dispute": 8,
    "Specific Performance": 8,
    "Murder": 10,
    "Bail": 7,
    "Cheque Bounce": 8,
    "NDPS Recovery": 10,
    "Criminal Procedure": 6,
    "Income Tax Assessment": 10,
    "GST Dispute": 9,
    "Transfer Pricing": 9,
    "Tax Tribunal Appeal": 8,
    "Departmental Proceeding": 8,
    "Termination": 8,
    "Reinstatement": 8,
    "Constitutional Jurisdiction": 6,
    "Fundamental Rights": 7,
}

# =========================================================
# 🔥 NORMALIZE
# =========================================================


def normalize_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 SPLIT PARAGRAPHS
# =========================================================


def split_paragraphs(text):

    parts = re.split(r"\n\s*\n", text)

    return [p.strip() for p in parts if p.strip()]


# =========================================================
# 🔥 DETECT ISSUE MATCHES
# =========================================================


def detect_issue_matches(paragraph):

    results = []

    lower = paragraph.lower()

    for category, issues in ISSUE_ONTOLOGY.items():

        for issue, patterns in issues.items():

            count = 0

            for pattern in patterns:

                matches = re.findall(pattern, lower, re.I)

                count += len(matches)

            if count < 1:

                continue

            score = count * ISSUE_WEIGHTS.get(issue, 1)

            # =============================================
            # 🔥 CATEGORY BOOST
            # =============================================

            if category == "Taxation":

                if any(
                    word in lower
                    for word in ["income tax", "assessment", "assessee", "itat", "gst"]
                ):

                    score += 15

            if category == "Criminal":

                if any(
                    word in lower
                    for word in ["accused", "conviction", "sentence", "fir"]
                ):

                    score += 10

            results.append(
                {"category": category, "issue": issue, "matches": count, "score": score}
            )

    return results


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def cluster_legal_issues(text):

    try:

        if not text:

            return {
                "issues": [],
                "dominant_issue": None,
                "dominant_category": None,
                "confidence": 0,
            }

        text = normalize_text(text)

        paragraphs = split_paragraphs(text)

        issue_scores = Counter()

        issue_hits = Counter()

        issue_categories = {}

        issue_paragraphs = {}

        category_scores = Counter()

        # =================================================
        # 🔥 PROCESS PARAGRAPHS
        # =================================================

        for para in paragraphs:

            matches = detect_issue_matches(para)

            for item in matches:

                issue = item["issue"]

                category = item["category"]

                score = item["score"]

                issue_scores[issue] += score

                issue_hits[issue] += item["matches"]

                category_scores[category] += score

                issue_categories[issue] = category

                if issue not in issue_paragraphs:

                    issue_paragraphs[issue] = []

                if len(issue_paragraphs[issue]) < 3:

                    issue_paragraphs[issue].append(para[:500])

        # =================================================
        # 🔥 DOMINANT CATEGORY
        # =================================================

        dominant_category = None

        if category_scores:

            dominant_category = max(category_scores, key=category_scores.get)

        # =================================================
        # 🔥 BUILD RANKED LIST
        # =================================================

        ranked = []

        for issue in issue_scores:

            category = issue_categories.get(issue)

            if dominant_category and category != dominant_category:

                continue

            if issue_scores[issue] < 8:

                continue

            ranked.append(
                {
                    "issue": issue,
                    "category": category,
                    "score": issue_scores[issue],
                    "hits": issue_hits[issue],
                    "sample_paragraphs": issue_paragraphs.get(issue, []),
                }
            )

        # =================================================
        # 🔥 JURISPRUDENTIAL PRIORITY BOOST
        # =================================================

        constitutional_priority = [
            "Electoral Transparency",
            "Criminal Antecedent Disclosure",
            "Election Commission Compliance",
            "Free And Fair Election",
            "Constitutional Governance",
            "Contempt Jurisdiction",
        ]

        for item in ranked:

            if item["issue"] in constitutional_priority:

                item["score"] += 40

        ranked.sort(key=lambda x: x["score"], reverse=True)

        # =================================================
        # 🔥 DOMINANT ISSUE
        # =================================================

        dominant_issue = None

        if ranked:

            dominant_issue = ranked[0]["issue"]

        # =================================================
        # 🔥 CONFIDENCE
        # =================================================

        confidence = 40

        if dominant_category:

            confidence += 20

        if dominant_issue:

            confidence += 20

        if len(ranked) >= 2:

            confidence += 10

        confidence = min(confidence, 95)

        result = {
            "issues": ranked,
            "dominant_issue": dominant_issue,
            "dominant_category": dominant_category,
            "confidence": confidence,
        }

        print("✅ Legal Issues Clustered:")

        print(result)

        return result

    except Exception as e:

        print("❌ ISSUE CLUSTER ERROR:", e)

        return {
            "issues": [],
            "dominant_issue": None,
            "dominant_category": None,
            "confidence": 0,
        }


# =========================================================
# 🔥 DIRECT TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    The reassessment proceedings under
    Section 147 of the Income Tax Act
    were challenged before the ITAT.

    The assessee disputed the assessment year.

    """

    print(cluster_legal_issues(sample))
