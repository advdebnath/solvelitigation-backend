import re


def normalize_case_number_object(case_data):

    # =====================================================
    # 🔥 DEFAULT OBJECT
    # =====================================================

    normalized = {
        "case_number": "Unknown",
        "normalized_case_number": "UNKNOWN",
        "case_type": "UNKNOWN",
        "court_type": "UNKNOWN",
        "year": None,
        "confidence": 0,
        "validation_status": "INVALID",
        "source": "post_processor",

        "jurisdiction": "UNKNOWN",
        "proceeding_family": "UNKNOWN",
        "is_primary_matter": True,
        "is_connected_matter": False,
        "is_review": False,
        "is_curative": False,
        "is_interlocutory": False,
        "parent_case": None,
        "originating_case": None,
        "linked_cases": [],
        "appellate_chain": [],
        "review_chain": [],
        "constitutional_cluster": None
    }

    # =====================================================
    # 🔥 STRING INPUT
    # =====================================================

    if isinstance(case_data, str):

        case_data = {
            "case_number": case_data,
            "confidence": 50
        }

    # =====================================================
    # 🔥 INVALID INPUT
    # =====================================================

    if not isinstance(case_data, dict):
        return normalized

    raw_case = str(
        case_data.get(
            "case_number",
            "Unknown"
        )
    ).strip()

    raw_case = re.sub(
        r"\s+",
        " ",
        raw_case
    )

    normalized["case_number"] = raw_case

    normalized["normalized_case_number"] = (
        raw_case.upper()
    )

    normalized["confidence"] = int(
        case_data.get(
            "confidence",
            0
        )
    )

    # =====================================================
    # 🔥 YEAR EXTRACTION
    # =====================================================

    year_match = re.search(
        r"\b(19|20)\d{2}\b",
        raw_case
    )

    if year_match:
        normalized["year"] = year_match.group(0)

    upper = raw_case.upper()

    # =====================================================
    # 🔥 CASE NUMBER ONTOLOGY ENGINE
    # =====================================================

    if "CIVIL APPEAL" in upper:
        normalized["jurisdiction"] = "CIVIL"

    elif "CRIMINAL APPEAL" in upper:
        normalized["jurisdiction"] = "CRIMINAL"

    elif "WRIT PETITION" in upper:
        normalized["jurisdiction"] = "CONSTITUTIONAL"

    elif "SLP" in upper:
        normalized["jurisdiction"] = "SPECIAL_LEAVE"

    # =====================================================
    # 🔥 PROCEEDING FAMILY
    # =====================================================

    if "REVIEW" in upper:

        normalized["proceeding_family"] = "REVIEW"
        normalized["is_review"] = True
        normalized["is_primary_matter"] = False

    elif "CURATIVE" in upper:

        normalized["proceeding_family"] = "CURATIVE"
        normalized["is_curative"] = True
        normalized["is_primary_matter"] = False

    elif "IA NO" in upper or "INTERLOCUTORY" in upper:

        normalized["proceeding_family"] = "INTERLOCUTORY"
        normalized["is_interlocutory"] = True
        normalized["is_primary_matter"] = False

    elif "CONNECTED" in upper:

        normalized["proceeding_family"] = "CONNECTED"
        normalized["is_connected_matter"] = True
        normalized["is_primary_matter"] = False

    else:

        normalized["proceeding_family"] = "PRIMARY"

    # =====================================================
    # 🔥 PARENT CASE LINKAGE ENGINE
    # =====================================================

    parent_patterns = [

        r"IN\s+(SLP\(C\).*?NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})",

        r"IN\s+(CIVIL\s+APPEAL\s+NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})",

        r"IN\s+(CRIMINAL\s+APPEAL\s+NO\.?\s*[\d\/\-]+\s*OF\s*\d{4})",

        r"ARISING\s+OUT\s+OF\s+(.*?)$",

        r"CONNECTED\s+WITH\s+(.*?)$"
    ]

    linked_cases = []

    for pattern in parent_patterns:

        try:

            matches = re.findall(
                pattern,
                upper,
                flags=re.I | re.M
            )

            for match in matches:

                cleaned = re.sub(
                    r"\s+",
                    " ",
                    str(match)
                ).strip()

                if cleaned and cleaned not in linked_cases:

                    linked_cases.append(cleaned)

        except Exception:
            pass

    if linked_cases:

        normalized["linked_cases"] = linked_cases

        normalized["parent_case"] = linked_cases[0]

    # =====================================================
    # 🔥 APPELLATE / REVIEW CHAINS
    # =====================================================

    if normalized.get("is_review"):

        normalized["review_chain"] = linked_cases

    if normalized.get("jurisdiction") in [
        "CIVIL",
        "CRIMINAL",
        "SPECIAL_LEAVE"
    ]:

        normalized["appellate_chain"] = linked_cases

    # =====================================================
    # 🔥 CONSTITUTIONAL CLUSTERING
    # =====================================================

    if (
        "ARTICLE 32" in upper
        or "ARTICLE 226" in upper
        or "WRIT PETITION" in upper
    ):

        normalized["constitutional_cluster"] = (
            "CONSTITUTIONAL_LITIGATION"
        )

    # =====================================================
    # 🔥 CASE TYPE INFERENCE
    # =====================================================

    CASE_TYPES = [

        "CIVIL APPEAL",
        "CRIMINAL APPEAL",
        "SPECIAL LEAVE PETITION",
        "SLP",
        "WRIT PETITION",
        "REVIEW PETITION",
        "TRANSFER PETITION",
        "CURATIVE PETITION",
        "DIARY",
        "WP(C)",
        "WP(CRL)",
        "CRL.REV",
        "BAIL APPLN",
        "OA",
        "TA",
        "MA"
    ]

    for item in CASE_TYPES:

        if item in upper:

            normalized["case_type"] = item
            break

    # =====================================================
    # 🔥 COURT INFERENCE
    # =====================================================

    if any(
        x in upper
        for x in [
            "SLP",
            "CIVIL APPEAL",
            "CRIMINAL APPEAL",
            "CURATIVE",
            "TRANSFER PETITION"
        ]
    ):

        normalized["court_type"] = "SUPREME COURT"

    elif any(
        x in upper
        for x in [
            "WP(C)",
            "CRM-M",
            "RSA",
            "CRL.REV"
        ]
    ):

        normalized["court_type"] = "HIGH COURT"

    elif any(
        x in upper
        for x in [
            "OA",
            "TA",
            "MA"
        ]
    ):

        normalized["court_type"] = "TRIBUNAL"

    # =====================================================
    # 🔥 VALIDATION
    # =====================================================

    if (
        normalized["case_number"] != "Unknown"
        and re.search(r"\d", raw_case)
    ):

        normalized["validation_status"] = "VALID"

    return normalized
