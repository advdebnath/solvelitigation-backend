import re

# ============================================
# 🔥 LEGAL KNOWLEDGE BASE (CORE MEANINGS)
# ============================================

SECTION_MEANINGS = {
    "302": "murder",
    "304": "culpable homicide",
    "307": "attempt to murder",
    "326": "grievous hurt",
    "420": "cheating",

    "73": "compensation for breach of contract",
    "74": "penalty damages",
}

COMMON_SECTIONS = {
    "34": "common intention",
    "149": "unlawful assembly",
}

IGNORE_SECTIONS = {"320", "323", "341"}


# ============================================
# 🔥 OUTCOME DETECTION (ADVANCED)
# ============================================

OUTCOME_PATTERNS = {
    "conviction upheld": ["conviction upheld", "convicted"],
    "acquittal": ["acquitted", "not guilty"],
    "appeal dismissed": ["appeal dismissed", "dismissed"],
    "appeal allowed": ["appeal allowed", "set aside"],
    "remand": ["remanded", "remit"],
    "bail granted": ["bail granted"],
}


def detect_outcome(text):
    t = text.lower()

    for outcome, patterns in OUTCOME_PATTERNS.items():
        for p in patterns:
            if p in t:
                return outcome

    return "decision"


# ============================================
# 🔥 NORMALIZE SECTIONS
# ============================================

def normalize_sections(sections):
    result = []

    for s in sections:
        num = re.findall(r"\d+", s)
        if not num:
            continue

        n = num[0]

        if n in IGNORE_SECTIONS:
            continue

        result.append(n)

    return sorted(set(result), key=lambda x: int(x))


# ============================================
# 🔥 BUILD SECTION STRING
# ============================================

def build_section_string(primary, common):
    if not primary:
        return ""

    if common:
        return f"Sections {', '.join(primary)} r/w {', '.join(common)}"

    return f"Section {primary[0]}" if len(primary) == 1 else f"Sections {', '.join(primary)}"


# ============================================
# 🔥 DETECT LEGAL ISSUE
# ============================================

def detect_issue(primary_sections):
    for sec in primary_sections:
        if sec in SECTION_MEANINGS:
            return SECTION_MEANINGS[sec]

    return "legal issue"


# ============================================
# 🔥 DETECT SERVICE / CIVIL ISSUES
# ============================================

def detect_context_issue(text, category):
    t = text.lower()

    if category == "Service":
        if "termination" in t:
            return "termination"
        if "reinstatement" in t:
            return "reinstatement"
        if "departmental proceeding" in t:
            return "departmental proceeding"

    if category == "Civil":
        if "contract" in t:
            return "contract dispute"
        if "property" in t:
            return "property dispute"
        if "injunction" in t:
            return "injunction"

    return None


# ============================================
# 🔥 MAIN FUNCTION (FINAL ENGINE)
# ============================================

def extract_point_of_law(text, category, acts, sections):
    section_nums = normalize_sections(sections)

    primary = []
    common = []

    for sec in section_nums:
        if sec in COMMON_SECTIONS:
            common.append(sec)
        else:
            primary.append(sec)

    if not primary:
        primary = section_nums

    # 🔥 ACT (priority)
    act = acts[0] if acts else "Law"

    # 🔥 ISSUE (priority: section meaning → context → fallback)
    issue = detect_issue(primary)

    if issue == "legal issue":
        context_issue = detect_context_issue(text, category)
        if context_issue:
            issue = context_issue

    # 🔥 COMMON TAG (extra clarity)
    common_tag = None
    for c in common:
        if c in COMMON_SECTIONS:
            common_tag = COMMON_SECTIONS[c]

    # 🔥 OUTCOME
    outcome = detect_outcome(text)

    # 🔥 SECTION STRING
    section_str = build_section_string(primary, common)

    # ============================================
    # 🔥 FINAL BUILD (COURT FORMAT)
    # ============================================

    parts = [category, act]

    if section_str:
        parts.append(section_str)

    if issue:
        parts.append(issue)

    if common_tag:
        parts.append(common_tag)

    if outcome:
        parts.append(outcome)

    return " – ".join(parts)
