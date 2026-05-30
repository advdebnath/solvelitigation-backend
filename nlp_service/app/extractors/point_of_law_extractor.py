import re
from collections import defaultdict

from app.legal_ontology.canonical_legal_object_engine import (
    build_canonical_legal_object, canonicalize_point_of_law)

# =========================================================
# 🔥 LEGAL ISSUE ONTOLOGY
# =========================================================

# =========================================================
# 🔥 CONTEXTUAL ISSUE SUPPRESSION
# =========================================================

# =========================================================
# 🔥 STRICT DOCTRINAL VALIDATION
# =========================================================

STRICT_POINT_VALIDATION = {
    "Joint Hindu Family": ["karta", "coparcener"],
    "Tenancy Surrender": ["surrender", "tenancy"],
    "Wakf Property Dispute": ["wakf", "tribunal"],
    "Constitutional Jurisdiction": ["article 226", "writ"],
    "Murder": ["section 302", "homicide"],
}


POINT_SUPPRESSION_RULES = {"Murder": ["civil appeal", "wakf"]}


CRIMINAL_DOMINANCE_TERMS = [
    "ndps",
    "narcotic",
    "contraband",
    "ganja",
    "heroin",
    "cocaine",
    "charas",
    "psychotropic",
    "fir",
    "chargesheet",
    "charge sheet",
    "criminal appeal",
    "section 302",
    "section 307",
    "section 376",
    "section 498a",
    "section 420",
    "ipc",
    "crpc",
    "pocso",
    "money laundering",
    "prevention of corruption",
    "bail",
    "custody",
    "acquittal",
    "conviction",
    "sentence",
    "prosecution",
    "appellant accused",
    "accused appellant",
]


LEGAL_POINT_PATTERNS = {
    "Wakf Property Dispute": {
        "patterns": ["wakf property", "wakf board", "wakf tribunal"],
        "category": "Civil",
    },
    "Tenancy Surrender": {
        "patterns": [
            "surrender tenancy",
            "tenancy rights",
            "lease dispute",
        ],
        "category": "Civil",
    },
    "Joint Hindu Family": {
        "patterns": [
            "joint hindu family",
            "karta",
            "coparcener",
        ],
        "category": "Civil",
    },
    "Constitutional Jurisdiction": {
        "patterns": [
            "article 226",
            "article 227",
            "writ petition",
            "constitutional remedy",
            "judicial review",
        ],
        "category": "Constitutional",
    },
    "Hereditary Tenancy": {
        "patterns": [
            r"\bhereditary\s+tenancy\b",
            r"\btenancy\s+inheritance\b",
            r"\btenant\s+inheritance\b",
            r"\boccupancy\s+rights\b",
            r"\btenancy\s+succession\b",
        ],
        "category": "Civil",
    },
    "Landlord Tenant Dispute": {
        "patterns": [
            r"\blandlord\s+tenant\b",
            r"\btenant\s+eviction\b",
            r"\beviction\s+petition\b",
            r"\brent\s+control\b",
            r"\blease\s+agreement\b",
            r"\btenancy\s+rights?\b",
            r"\btenant\s+default\b",
        ],
        "category": "Civil",
    },
    "Property Possession": {
        "patterns": [
            r"\bpossession\b",
            r"\btitle\s+suit\b",
            r"\bproperty\s+dispute\b",
            r"\bownership\s+dispute\b",
            r"\bimmovable\s+property\b",
        ],
        "category": "Civil",
    },
    "Wakf Tribunal Jurisdiction": {
        "patterns": [
            r"\bwakf\s+tribunal\b",
            r"\bsection\s+83\b",
            r"\bsection\s+85\b",
            r"\btribunal\s+jurisdiction\b",
            r"\bwakf\s+jurisdiction\b",
        ],
        "category": "Civil",
    },
    "Bail": {
        "patterns": [
            r"\banticipatory\s+bail\b",
            r"\bregular\s+bail\b",
            r"\bgrant\s+of\s+bail\b",
            r"\bbail\s+application\b",
        ],
        "category": "Criminal",
    },
    "Murder": {
        "patterns": ["section 302", "murder", "homicide", "culpable homicide"],
        "category": "Criminal",
    },
    "Benefit Of Doubt": {
        "patterns": [
            "benefit of doubt",
            "reasonable doubt",
            "failed to prove",
            "prosecution failed",
            "suspicion cannot take the place of proof",
        ],
        "category": "Criminal",
    },
    "Conviction Set Aside": {
        "patterns": [
            "set aside the conviction",
            "orders of conviction set aside",
            "conviction and sentence set aside",
            "acquitted",
            "set at liberty",
        ],
        "category": "Criminal",
    },
    "Article 32 Remedy": {
        "patterns": [
            "article 32",
            "writ petition under article 32",
            "constitutional remedy",
            "enforcement of fundamental rights",
        ],
        "category": "Constitutional",
    },
    "Fundamental Rights Enforcement": {
        "patterns": [
            "article 14",
            "article 19",
            "article 21",
            "fundamental rights",
            "constitutional protection",
        ],
        "category": "Constitutional",
    },
    "Natural Justice": {
        "patterns": [
            "natural justice",
            "audi alteram partem",
            "fair hearing",
            "principles of natural justice",
            "opportunity of hearing",
        ],
        "category": "Procedural",
    },
    "Judicial Review": {
        "patterns": [
            "judicial review",
            "constitutional validity",
            "ultra vires",
            "arbitrary state action",
        ],
        "category": "Constitutional",
    },
    "Reinstatement In Service": {
        "patterns": [
            "reinstated in service",
            "reinstatement",
            "continuity of service",
            "back wages",
            "termination set aside",
        ],
        "category": "Service",
    },
    "Departmental Proceeding": {
        "patterns": [
            "departmental proceeding",
            "disciplinary authority",
            "charge memorandum",
            "misconduct",
            "service rules",
        ],
        "category": "Service",
    },
    "FIR Quashing": {
        "patterns": [
            "quashing of fir",
            "section 482",
            "criminal proceedings quashed",
            "abuse of process of law",
            "charge sheet quashed",
        ],
        "category": "Criminal",
    },
    "NDPS Recovery": {
        "patterns": [
            "ndps act",
            "contraband",
            "ganja",
            "heroin",
            "psychotropic substances",
            "commercial quantity",
        ],
        "category": "Criminal",
    },
    "GST Input Tax Credit": {
        "patterns": ["input tax credit", "itc", "gst", "fake invoices", "tax credit"],
        "category": "Taxation",
    },
    "Reassessment": {
        "patterns": [
            "escaped assessment",
            "reassessment",
            "reopening of assessment",
            "income escaped assessment",
        ],
        "category": "Taxation",
    },
}
# =========================================================


def boost(score_map, category, score):

    if not category:
        return

    score_map[category] += score


# =========================================================
# 🔒 IMMUTABLE POINT OBJECT ENGINE
# =========================================================


def build_point_object(point_name, category=None, confidence=0):

    canonical_point = canonicalize_point_of_law(point_name)

    canonical_object = build_canonical_legal_object(canonical_point, "POINT_OF_LAW")

    return {
        "point": canonical_point,
        "category": category,
        "confidence": max(0, min(100, int(confidence))),
        "canonical_point_object": canonical_object,
    }


# =========================================================
# 🔥 POINT CATEGORY DETECTOR
# =========================================================


def detect_point_category(point_name, full_text="", acts=None):

    if acts is None:
        acts = []

    text = full_text.lower()

    category_scores = defaultdict(int)

    # -----------------------------------------------------
    # 🔥 DEFAULT ONTOLOGY CATEGORY
    # -----------------------------------------------------

    ontology = LEGAL_POINT_PATTERNS.get(point_name)

    if ontology:

        boost(category_scores, ontology.get("category"), 100)

    # -----------------------------------------------------
    # 🔥 JURISDICTION PRIORITY
    # -----------------------------------------------------

    if (
        "civil appellate jurisdiction" in text
        or "civil appeal" in text
        or "writ petition (civil)" in text
    ):

        boost(category_scores, "Civil", 120)

    if (
        "criminal appellate jurisdiction" in text
        or "criminal appeal" in text
        or "bail application" in text
    ):

        boost(category_scores, "Criminal", 120)

    # -----------------------------------------------------
    # 🔥 ACT INFERENCE
    # -----------------------------------------------------

    acts_lower = [str(a).lower() for a in acts]

    if any("wakf" in a for a in acts_lower):

        boost(category_scores, "Civil", 80)

    if any("contract" in a for a in acts_lower):

        boost(category_scores, "Civil", 60)

    if any("constitution" in a for a in acts_lower):

        boost(category_scores, "Constitutional", 80)

    if any(
        x in a
        for a in acts_lower
        for x in ["criminal procedure", "penal code", "ndps", "pocso"]
    ):

        boost(category_scores, "Criminal", 80)

    # -----------------------------------------------------
    # 🔥 CONTEXT KEYWORDS
    # -----------------------------------------------------

    civil_words = [
        "tenant",
        "lease",
        "property",
        "title suit",
        "ownership",
        "partition",
        "family property",
    ]

    criminal_words = [
        "accused",
        "conviction",
        "charge sheet",
        "custody",
        "prosecution",
        "offence",
    ]

    constitutional_words = [
        "article 226",
        "article 227",
        "fundamental rights",
        "judicial review",
    ]

    for word in civil_words:

        if word in text:

            boost(category_scores, "Civil", 5)

    for word in criminal_words:

        if word in text:

            boost(category_scores, "Criminal", 5)

    for word in constitutional_words:

        if word in text:

            boost(category_scores, "Constitutional", 5)

    # -----------------------------------------------------
    # 🔥 FINAL CATEGORY
    # -----------------------------------------------------

    if not category_scores:

        return "General"

    return max(category_scores, key=category_scores.get)


# =========================================================
# 🔥 MAIN EXTRACTOR
# =========================================================


def extract_points_of_law(full_text="", acts=None, clustered_issues=None):

    if acts is None:
        acts = []

    if clustered_issues is None:
        clustered_issues = []

    text = full_text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    print("🔥 POINT OF LAW TEXT SAMPLE:")
    print(text[:5000])

    detected = defaultdict(int)

    # =====================================================
    # 🔥 SEMANTIC CRIMINAL DOMINANCE ENGINE
    # =====================================================

    criminal_semantic_score = 0

    for criminal_term in CRIMINAL_DOMINANCE_TERMS:

        if criminal_term in text:

            criminal_semantic_score += 1

    print("🔥 CRIMINAL SEMANTIC SCORE:")
    print(criminal_semantic_score)

    # -----------------------------------------------------
    # 🔥 PRIORITY 1 → CLUSTERED ISSUES
    # -----------------------------------------------------

    for issue in clustered_issues:

        if not isinstance(issue, dict):
            continue

        issue_name = issue.get("issue", "").strip()

        score = issue.get("score", 0)

        if not issue_name:
            continue

        detected[issue_name] += 100 + score

    # -----------------------------------------------------
    # 🔥 PRIORITY 2 → LEGAL PHRASES
    # -----------------------------------------------------

    for point, config in LEGAL_POINT_PATTERNS.items():

        patterns = config.get("patterns", [])

        for pattern in patterns:

            try:

                hits = len(re.findall(pattern, text, flags=re.I))

            except Exception as regex_error:

                print("❌ REGEX ERROR:")
                print(pattern)
                print(str(regex_error))

                hits = 0

            if hits:

                detected[point] += hits * 25

                # ---------------------------------------------
                # 🔥 CRIMINAL CONTEXT CIVIL SUPPRESSION
                # ---------------------------------------------

                if criminal_semantic_score >= 3 and point in [
                    "Property Possession",
                    "Landlord Tenant Dispute",
                    "Hereditary Tenancy",
                    "Tenancy Surrender",
                ]:

                    detected[point] -= 40

                # ---------------------------------------------
                # 🔥 CRIMINAL DOMINANCE BOOST
                # ---------------------------------------------

                if (
                    criminal_semantic_score >= 3
                    and config.get("category") == "Criminal"
                ):

                    detected[point] += 60

    acts_lower = [str(a).lower() for a in acts]

    if any("wakf" in a for a in acts_lower):

        detected["Wakf Property Dispute"] += 100

    if any("constitution" in a for a in acts_lower):

        detected["Constitutional Jurisdiction"] += 50

    # -----------------------------------------------------
    # 🔥 FINAL SORTING
    # -----------------------------------------------------

    print("🔥 RAW ISSUE SCORES:")
    print(detected)

    final_points = sorted(detected.items(), key=lambda x: x[1], reverse=True)

    cleaned = []

    seen = set()

    for point, score in final_points:

        if score < 10:
            continue

        normalized = point.strip()

        suppress = False

        suppression_terms = POINT_SUPPRESSION_RULES.get(normalized, [])

        for term in suppression_terms:

            try:

                suppression_hits = re.findall(
                    rf"\\b{re.escape(term.lower())}\\b", text, flags=re.I
                )

                if len(suppression_hits) >= 3:

                    suppress = True
                    break

            except Exception as suppression_error:

                print("❌ SUPPRESSION ERROR:")
                print(term)
                print(str(suppression_error))

        if suppress:

            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        point_category = LEGAL_POINT_PATTERNS.get(normalized, {}).get(
            "category", "General"
        )

        # -----------------------------------------------------
        # 🔥 FINAL CRIMINAL FALSE POSITIVE FILTER
        # -----------------------------------------------------

        if point_category == "Criminal":

            criminal_context = any(
                keyword in text.lower()
                for keyword in [
                    "ipc",
                    "crpc",
                    "conviction",
                    "accused",
                    "prosecution",
                    "complainant",
                    "bail",
                    "fir",
                    "chargesheet",
                    "charge sheet",
                    "murder",
                    "rape",
                    "ndps",
                ]
            )

            if not criminal_context:
                continue

        # -----------------------------------------------------
        # 🔥 SEMANTIC EVIDENCE FIREWALL
        # -----------------------------------------------------

        semantic_reject = False

        if normalized == "Murder":

            murder_evidence = [
                "section 302",
                "homicide",
                "deceased",
                "dead body",
                "postmortem",
                "fatal injuries",
            ]

            evidence_hits = sum(1 for ev in murder_evidence if ev in text)

            if evidence_hits < 2:
                semantic_reject = True

        if normalized == "Conviction Set Aside":

            conviction_evidence = [
                "conviction set aside",
                "acquitted",
                "benefit of doubt",
                "sentence set aside",
            ]

            evidence_hits = sum(1 for ev in conviction_evidence if ev in text)

            if evidence_hits < 1:
                semantic_reject = True

        if normalized == "Wakf Tribunal Jurisdiction":

            wakf_evidence = [
                "wakf tribunal",
                "wakf property",
                "section 83",
                "section 85",
            ]

            evidence_hits = sum(1 for ev in wakf_evidence if ev in text)

            if evidence_hits < 2:
                semantic_reject = True

        # -----------------------------------------------------
        # 🔥 SERVICE LAW FALSE POSITIVE FIREWALL
        # -----------------------------------------------------

        if normalized == "Departmental Proceeding":

            service_evidence = [
                "departmental proceeding",
                "disciplinary authority",
                "departmental enquiry",
                "service rules",
                "conduct rules",
                "suspension",
                "dismissal from service",
                "termination from service",
                "enquiry officer",
                "service jurisprudence",
            ]

            service_hits = sum(1 for ev in service_evidence if ev in text)

            criminal_conflict = any(
                keyword in text
                for keyword in [
                    "ipc",
                    "crpc",
                    "murder",
                    "accused",
                    "conviction",
                    "prosecution",
                    "chargesheet",
                    "charge sheet",
                    "trial court",
                ]
            )

            if service_hits < 2 or criminal_conflict:
                semantic_reject = True

        if semantic_reject:

            print("❌ SEMANTICALLY REJECTED:")
            print(normalized)

            continue

        cleaned.append(
            {"point": normalized, "category": point_category, "score": score}
        )

    # -----------------------------------------------------
    # 🔥 LIMIT
    # -----------------------------------------------------

    cleaned = cleaned[:6]

    # -----------------------------------------------------
    # 🔥 OVERALL DOMINANT CATEGORY
    # -----------------------------------------------------

    overall_scores = defaultdict(int)

    for item in cleaned:

        overall_scores[item["category"]] += 1

    if overall_scores:

        dominant_category = max(overall_scores, key=overall_scores.get)

    else:

        dominant_category = "Unknown"

    # =====================================================
    # 🔒 IMMUTABLE POINT PROPAGATION
    # =====================================================

    immutable_points = []

    for item in cleaned:

        if isinstance(item, dict):

            point_name = item.get("point")

            category = item.get("category", dominant_category)

            confidence = item.get("confidence", 70)

        else:

            point_name = str(item)

            category = dominant_category

            confidence = 70

        immutable_points.append(
            build_point_object(
                point_name=point_name, category=category, confidence=confidence
            )
        )

    return {
        # backward compatibility
        "points_of_law": cleaned,
        # enterprise immutable ontology
        "immutable_points_of_law": immutable_points,
        "category": dominant_category,
        "confidence": min(95, 60 + len(cleaned) * 5),
    }


# =========================================================
# 🔥 LEGACY COMPATIBILITY
# =========================================================


def extract_canonical_points_of_law(full_text="", acts=None, clustered_issues=None):

    return extract_points_of_law(
        full_text=full_text, acts=acts, clustered_issues=clustered_issues
    )


# =========================================================
# 🔥 SERVICE LAW ONTOLOGY
# =========================================================

LEGAL_POINT_PATTERNS.update(
    {
        "Equal Pay For Equal Work": {
            "patterns": [
                r"\bequal\s+pay\s+for\s+equal\s+work\b",
                r"\bpay\s+parity\b",
                r"\brevised\s+pay\s+scale\b",
                r"\bpay\s+scale\b",
                r"\bdeputation\b",
                r"\bservice\s+benefits\b",
                r"\bsalary\s+discrimination\b",
                r"\bfinancial\s+burden\b",
                r"\bregularization\b",
                r"\bservice\s+jurisprudence\b",
            ],
            "category": "Service",
        },
        "Service Regularization": {
            "patterns": [
                r"\bregularization\b",
                r"\bregularized\b",
                r"\btemporary\s+employee\b",
                r"\bcontractual\s+employee\b",
                r"\bdaily\s+wager\b",
                r"\bcontinuity\s+of\s+service\b",
            ],
            "category": "Service",
        },
        "Departmental Proceeding": {
            "patterns": [
                r"\bdepartmental\s+proceeding\b",
                r"\bdisciplinary\s+authority\b",
                r"\bmisconduct\b",
                r"\bcharge\s+sheet\b",
                r"\benquiry\s+officer\b",
                r"\bservice\s+rules\b",
            ],
            "category": "Service",
        },
        "Benefit Of Doubt": {
            "patterns": [
                r"\bbenefit\s+of\s+doubt\b",
                r"\breasonable\s+doubt\b",
                r"\bfailed\s+to\s+prove\b",
                r"\bprosecution\s+failed\b",
                r"\bsuspicion\s+cannot\s+take\s+the\s+place\s+of\s+proof\b",
            ],
            "category": "Criminal",
        },
        "Conviction Set Aside": {
            "patterns": [
                r"\bset\s*aside\s+the\s+conviction\b",
                r"\borders\s+of\s+conviction\s+set\s*aside\b",
                r"\bconviction\s+and\s+sentence\s+set\s*aside\b",
                r"\bacquitted\b",
                r"\bset\s*aside\s+the\s+orders\s+of\s+conviction\b",
                r"\bset\s+at\s+liberty\b",
                r"\bset\s+at\s+liberty\s+forthwith\b",
                r"\bset\s+at\s+liberty\b",
            ],
            "category": "Criminal",
        },
    }
)
