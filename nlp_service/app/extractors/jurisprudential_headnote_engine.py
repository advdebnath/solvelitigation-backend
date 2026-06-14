import re
from collections import Counter

# =========================================================
# 🔥 CLEAN TEXT
# =========================================================


def clean_text(text):

    if not text:

        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 SPLIT PARAGRAPHS
# =========================================================


def split_paragraphs(text):

    # =====================================================
    # 🔥 NORMALIZE OCR / PDF STRUCTURE
    # =====================================================

    text = re.sub(r"\\r", "\\n", text)

    # -----------------------------------------------------
    # 🔥 FORCE SPLIT BEFORE NUMBERED PARAS
    # -----------------------------------------------------

    text = re.sub(r"(?<!\\n)(\\b\\d{1,3}\\.\\s+)", r"\\n\\n\\1", text)

    # -----------------------------------------------------
    # 🔥 FORCE SPLIT BEFORE ROMAN SUBPARTS
    # -----------------------------------------------------

    text = re.sub(r"(?<!\\n)(\\([ivxIVX]+\\))", r"\\n\\n\\1", text)

    # -----------------------------------------------------
    # 🔥 CLEAN MULTIPLE NEWLINES
    # -----------------------------------------------------

    text = re.sub(r"\\n{2,}", "\\n\\n", text)

    paragraphs = re.split(r"\\n\\s*\\n", text)

    cleaned = []

    for p in paragraphs:

        p = clean_text(p)

        if not p:

            continue

        # =============================================
        # 🔥 REJECT MICRO FRAGMENTS
        # =============================================

        if len(p) < 40:

            continue

        # =============================================
        # 🔥 REJECT TITLE BLOCKS
        # =============================================

        lower = p.lower()

        rejection_terms = [
            "reportable",
            "in the supreme court",
            "high court of",
            "petitioner",
            "respondent",
            "versus",
            "appearance",
            "coram",
            "advocate",
            "diary no",
        ]

        rejection_hits = sum(1 for term in rejection_terms if term in lower)

        if rejection_hits >= 4:

            continue

        cleaned.append(p)

    return cleaned


# =========================================================
# 🔥 EXTRACT PARA NUMBER
# =========================================================


def extract_para_number(para):

    patterns = [r"\b(\d{1,3})\.\s", r"\((\d{1,3})\)", r"paragraph\s+(\d{1,3})"]

    for pattern in patterns:

        match = re.search(pattern, para, re.I)

        if match:

            return f"para-{match.group(1)}"

    return "para-unknown"


# =========================================================
# 🔥 RATIO INDICATORS
# =========================================================

RATIO_PATTERNS = [
    r"\bheld that\b",
    r"\bit is settled law\b",
    r"\bthe court held\b",
    r"\bthere is no merit\b",
    r"\bliable to be set aside\b",
    r"\bdeserves to be allowed\b",
    r"\bdeserves dismissal\b",
    r"\bjurisdiction\b",
    r"\bnot sustainable\b",
    r"\bwithout jurisdiction\b",
    r"\bcontrary to law\b",
    r"\bprinciple\b",
    r"\blegal position\b",
    r"\bbarred by\b",
    r"\bvalidly exercised\b",
    r"\bwe direct\b",
    r"\bwe therefore direct\b",
    r"\bit is necessary\b",
    r"\bit is mandatory\b",
    r"\bcandidate shall\b",
    r"\bpolitical parties shall\b",
    r"\bvoter has a right to know\b",
    r"\bright to know\b",
    r"\bconstitutional mandate\b",
    r"\bfree and fair elections\b",
    r"\bpurity of elections\b",
    r"\bdemocracy\b",
    r"\bcriminal antecedents\b",
    r"\bmust disclose\b",
    r"\bshall disclose\b",
    r"\bthe directions issued\b",
]

# =========================================================
# 🔥 CATEGORY PROPOSITIONS
# =========================================================

CATEGORY_PROPOSITIONS = {
    "Criminal": [
        "conviction",
        "sentence",
        "acquittal",
        "bail",
        "prosecution",
        "evidence",
    ],
    "Civil": [
        "title",
        "ownership",
        "lease",
        "agreement",
        "tenancy",
        "specific performance",
    ],
    "Taxation": [
        "assessment",
        "reassessment",
        "deduction",
        "assessee",
        "tax liability",
        "exemption",
    ],
    "Service": [
        "termination",
        "departmental proceeding",
        "reinstatement",
        "disciplinary authority",
    ],
    "Constitutional": [
        "article 14",
        "article 21",
        "writ jurisdiction",
        "fundamental rights",
    ],
}

# =========================================================
# 🔥 RATIO SCORING
# =========================================================


def score_ratio_paragraph(para, category=None):

    lower = para.lower()

    score = 0

    # =====================================================
    # 🔥 RATIO SIGNALS
    # =====================================================

    for pattern in RATIO_PATTERNS:

        if re.search(pattern, lower, re.I):

            score += 60

    # =====================================================
    # 🔥 CATEGORY BOOST
    # =====================================================

    if category:

        words = CATEGORY_PROPOSITIONS.get(category, [])

        for word in words:

            if word in lower:

                score += 35

    # =====================================================
    # 🔥 SHORT AUTHORITATIVE PARA
    # =====================================================

    if 250 <= len(lower) <= 1200:

        score += 40

    # =====================================================
    # 🔥 DECLARATORY / CONSTITUTIONAL BOOST
    # =====================================================

    declaratory_terms = [
        "we hold",
        "it is held",
        "we direct",
        "we therefore direct",
        "constitutional mandate",
        "constitutional obligation",
        "right to know",
        "free and fair elections",
        "purity of elections",
        "criminal antecedents",
        "must disclose",
        "shall disclose",
        "candidate shall",
        "political parties shall",
        "voter awareness",
        "rule of law",
        "democracy",
        "constitutional courts",
        "election commission",
    ]

    declaratory_hits = sum(1 for term in declaratory_terms if term in lower)

    score += declaratory_hits * 180

    return score


# =========================================================
# 🔥 EXTRACT RATIO
# =========================================================


def extract_ratio(text, category=None):

    # =====================================================
    # 🔥 STRUCTURAL NORMALIZATION
    # =====================================================

    text = re.sub(r"\n\s*(\d{1,3})\.\s+", r"\n\nPARA_SPLIT_\\1. ", text)

    text = re.sub(r"\n\s*(\([ivxIVX]+\))", r"\n\n\\1", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    paragraphs = [
        p.strip() for p in re.split(r"\n\n+|PARA_SPLIT_\d+\.", text) if p.strip()
    ]

    if not paragraphs:

        return None, None

    # =====================================================
    # 🔥 FULL DOCUMENT ANALYTICAL SCAN
    # =====================================================

    target = paragraphs

    best_para = None

    best_score = 0

    for para in target:

        para_clean = clean_text(para)

        para_lower = para_clean.lower()

        # =============================================
        # 🔥 HARD STRUCTURAL REJECTION
        # =============================================

        structural_rejections = [
            "reportable",
            "in the supreme court of india",
            "high court of",
            "civil appeal no",
            "criminal appeal no",
            "writ petition",
            "contempt petition",
            "petitioner",
            "respondent",
            "appellant",
            "versus",
            "appearance",
            "for petitioner",
            "for respondent",
            "coram",
            "present:",
            "j u d g m e n t",
            "per court",
            "advocate",
            "diary no",
        ]

        rejection_hits = sum(1 for term in structural_rejections if term in para_lower)

        if rejection_hits >= 3:

            continue

        # =============================================
        # 🔥 HEADER / TITLE REJECTION
        # =============================================

        rejection_patterns = [
            "reportable",
            "in the supreme court",
            "high court of",
            "civil appeal no",
            "criminal appeal no",
            "writ petition",
            "versus",
            "petitioner",
            "respondent",
            "appellant",
            "appearance",
            "for petitioner",
            "for respondent",
            "present:",
            "coram",
            "j u d g m e n t",
            "per court",
            "advocate",
            "diary no",
            "contempt petition",
        ]

        if any(pattern in para_lower for pattern in rejection_patterns):

            continue

        # =============================================
        # 🔥 FACTUAL NARRATION REJECTION
        # =============================================

        factual_patterns = [
            "facts of the case",
            "brief facts",
            "the petitioner herein",
            "the respondent herein",
            "has filed the present",
            "the present petition",
            "the case of the petitioner",
            "the facts leading",
            "in the instant case",
        ]

        factual_hits = sum(1 for pattern in factual_patterns if pattern in para_lower)

        if factual_hits >= 2:

            continue

        # =============================================
        # 🔥 LENGTH FILTER
        # =============================================

        if len(para_clean) < 120:

            continue

        if len(para_clean) > 2500:

            continue

        # =============================================
        # 🔥 SCORE
        # =============================================

        score = score_ratio_paragraph(para_clean, category)

        # =============================================
        # 🔥 PROCEDURAL PENALTY
        # =============================================

        procedural_terms = [
            "petition has been filed",
            "petitioner herein",
            "the present petition",
            "brief facts",
            "facts of the case",
            "the petitioner submits",
            "learned counsel",
            "notice was issued",
            "the instant petition",
            "the present appeal",
            "the appellant contends",
            "the respondent submits",
        ]

        procedural_hits = sum(1 for term in procedural_terms if term in para_lower)

        score -= procedural_hits * 40

        # =============================================
        # 🔥 ANALYTICAL BOOST
        # =============================================

        analytical_terms = [
            "we hold",
            "it is settled",
            "therefore",
            "thus",
            "in our opinion",
            "we are of the view",
            "held that",
            "we find",
            "it is clear",
            "the law is well settled",
        ]

        analytical_hits = sum(1 for term in analytical_terms if term in para_lower)

        score += analytical_hits * 80

        # =============================================
        # 🔥 DOCTRINAL BOOST
        # =============================================

        doctrinal_terms = [
            "constitutional mandate",
            "rule of law",
            "free and fair elections",
            "democracy",
            "fundamental rights",
            "constitutional obligation",
            "constitutional courts",
            "judicial review",
            "interpretation of",
            "constitutional scheme",
            "public interest",
            "electoral reforms",
            "criminal antecedents",
            "voter awareness",
            "purity of elections",
            "constitutional morality",
        ]

        doctrinal_hits = sum(1 for term in doctrinal_terms if term in para_lower)

        score += doctrinal_hits * 120

        # =============================================
        # 🔥 LATER PARAGRAPH BONUS
        # =============================================

        para_position = target.index(para)

        if para_position > len(target) * 0.5:

            score += 20

        # =============================================
        # 🔥 ANALYTICAL ADMISSION FILTER
        # =============================================

        admission_terms = [
            "we hold",
            "held that",
            "it is clear",
            "therefore",
            "thus",
            "we are of the view",
            "constitutional",
            "fundamental rights",
            "rule of law",
            "judicial review",
            "free and fair elections",
            "criminal antecedents",
            "electoral reforms",
            "voter awareness",
            "purity of elections",
            "democracy",
        ]

        admission_hits = sum(1 for term in admission_terms if term in para_lower)

        # =============================================
        # 🔥 REJECT LOW ANALYTICAL PARAGRAPHS
        # =============================================

        if admission_hits == 0 and score < 250:

            continue

        if score > best_score:

            best_score = score

            best_para = para_clean

    if not best_para:

        return None, None

    cleaned = clean_text(best_para)

    cleaned = cleaned[:900]

    para_number = extract_para_number(best_para)

    return cleaned, para_number


# =========================================================
# 🔥 OPERATIVE SYNTHESIS
# =========================================================


def synthesize_operative(operative_data):

    if not operative_data:

        return None

    holding = operative_data.get("final_holding")

    if not holding:

        return None

    return clean_text(holding)


# =========================================================
# 🔥 POINT SYNTHESIS
# =========================================================


def synthesize_points(points_data):

    if not points_data:

        return []

    points = []

    raw = points_data.get("points_of_law", [])

    for item in raw[:4]:

        if isinstance(item, dict):

            point = item.get("point")

        else:

            point = str(item)

        point = clean_text(point)

        if point:

            points.append(point)

    return list(dict.fromkeys(points))


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================


def generate_jurisprudential_headnote(
    full_text,
    issue_data=None,
    points_data=None,
    sections_data=None,
    operative_data=None,
):

    try:

        if not full_text:

            return {
                "headnote": "",
                "ratio": None,
                "structured_headnotes": [],
                "confidence": 0,
            }

        full_text = clean_text(full_text)

        # =================================================
        # 🔥 CATEGORY
        # =================================================

        category = None

        if issue_data:

            category = issue_data.get("dominant_category")

        # =================================================
        # 🔥 DOMINANT ISSUE
        # =================================================

        dominant_issue = None

        if issue_data:

            dominant_issue = issue_data.get("dominant_issue")

        # =================================================
        # 🔥 POINTS
        # =================================================

        points = synthesize_points(points_data)

        # =================================================
        # 🔥 RATIO
        # =================================================

        ratio, ratio_para = extract_ratio(full_text, category)

        # =================================================
        # 🔥 OPERATIVE
        # =================================================

        operative = synthesize_operative(operative_data)

        # =================================================
        # 🔥 BUILD
        # =================================================

        parts = []

        structured_headnotes = []

        if dominant_issue:

            parts.append(dominant_issue)

        if points:

            parts.append(" — ".join(points[:3]))

        if ratio:

            # =============================================

            # 🔥 DOCTRINAL CLEANUP

            # =============================================

            cleaned_ratio = ratio

            cleanup_patterns = [
                r"REPORTABLE",
                r"IN THE SUPREME COURT OF INDIA",
                r"J U D G M E N T",
                r"Signature Not Verified",
                r"Digitally signed by.*",
                r"Date:\s*\d{4}.*",
                r"\b\d+\s*$",
            ]

            for pattern in cleanup_patterns:

                cleaned_ratio = re.sub(pattern, "", cleaned_ratio, flags=re.I)

            cleaned_ratio = re.sub(r"\s+", " ", cleaned_ratio).strip()

            # =============================================

            # 🔥 TRUNCATE SMARTLY

            # =============================================

            sentences = re.split(r"(?<=[.!?])\s+", cleaned_ratio)

            doctrinal_summary = " ".join(sentences[:3])

            parts.append(f"Held: {doctrinal_summary}")

            if points:

                for point in points[:10]:

                    if not point:
                        continue

                    structured_headnotes.append(
                        {
                            "point_of_law": point,
                            "holding": doctrinal_summary,
                            "paragraphs": ratio_para if ratio_para else "para-unknown",
                        }
                    )

            elif dominant_issue:

                structured_headnotes.append(
                    {
                        "point_of_law": dominant_issue,
                        "holding": doctrinal_summary,
                        "paragraphs": ratio_para if ratio_para else "para-unknown",
                    }
                )

        if operative:

            parts.append(operative)

        # =================================================

        # 🔥 DEDUP

        # =================================================

        final = []

        seen = set()

        for part in parts:

            part = clean_text(part)

            if not part:

                continue

            lower = part.lower()

            if lower in seen:

                continue

            seen.add(lower)

            final.append(part)

        # =================================================

        # 🔥 FINAL HEADNOTE

        # =================================================

        headnote = " — ".join(final)

        if ratio_para:

            headnote += f". ({ratio_para})"

        # =================================================

        # 🔥 CONFIDENCE

        # =================================================

        confidence = 75

        if dominant_issue:

            confidence += 5

        if ratio:

            confidence += 10

        if operative:

            confidence += 5

        confidence = min(confidence, 98)

        result = {
            "headnote": headnote,
            "ratio": ratio,
            "ratio_para": ratio_para,
            "structured_headnotes": structured_headnotes,
            "confidence": confidence,
        }

        print("✅ Jurisprudential Headnote Generated:")

        print(result)

        return result

    except Exception as e:

        import traceback

        print("❌ JURISPRUDENTIAL HEADNOTE ERROR:")
        traceback.print_exc()

        return {
            "headnote": "",
            "ratio": None,
            "ratio_para": None,
            "structured_headnotes": structured_headnotes,
            "confidence": 0,
        }


# =========================================================


# 🔥 BACKWARD COMPATIBILITY


# =========================================================


def generate_headnote(
    full_text,
    issue_data=None,
    points_data=None,
    sections_data=None,
    operative_data=None,
):

    return generate_jurisprudential_headnote(
        full_text, issue_data, points_data, sections_data, operative_data
    )


# =========================================================


# 🔥 DIRECT TEST


# =========================================================


if __name__ == "__main__":

    sample = """





    43. The reassessment proceedings under


    Section 147 of the Income Tax Act


    are without jurisdiction and liable


    to be set aside.





    Accordingly, the appeal is allowed.





    """

    print(
        generate_jurisprudential_headnote(
            sample,
            issue_data={
                "dominant_issue": "Income Tax Assessment",
                "dominant_category": "Taxation",
            },
            operative_data={"final_holding": "Appeal Allowed"},
        )
    )
