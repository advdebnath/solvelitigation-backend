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
        "constitutional_cluster": None,
    }

    # =====================================================
    # 🔥 STRING INPUT
    # =====================================================

    if isinstance(case_data, str):

        case_data = {"case_number": case_data, "confidence": 50}

    # =====================================================
    # 🔥 INVALID INPUT
    # =====================================================

    if not isinstance(case_data, dict):
        return normalized

    # =====================================================
    # 🔒 AUTHORITATIVE EXTRACTION PRESERVATION FIREWALL
    # =====================================================

    authoritative_sources = [

        # =================================================
        # SUPREME COURT AUTHORITATIVE ENGINES
        # =================================================

        "SC_EXTRACTOR_V2",
        "SC_NUMBERED_CASE_OVERRIDE",
        "SC_HISTORICAL_FALLBACK",

        # ============================================
        # 🔒 IN RE / SUO MOTU AUTHORITATIVE ENGINES
        # ============================================

        "IN_RE_ENGINE",
        "SUO_MOTU_ENGINE",

        # =================================================
        # LEGACY AUTHORITATIVE ENGINES
        # =================================================

        "LOCKED_JUDICIARY_ENGINE",
        "ULTRA_PRIORITY_SC_LOCK",
        "PETITIONER_RESPONDENT_CAPTION",
        "HIGH_CONFIDENCE_HEADER_ENGINE",
        "CANONICAL_CAPTION_ENGINE",
    ]

    incoming_source = str(case_data.get("source", ""))

    incoming_confidence = int(case_data.get("confidence", 0))

    incoming_case = str(case_data.get("case_number", "")).strip()

    print("🔥 NORMALIZER INPUT:")
    print(case_data)

    if (
        incoming_source in authoritative_sources
        and incoming_confidence >= 90
    ):

        print("🔒 AUTHORITATIVE CASE PRESERVATION LOCK")
        print(case_data)

        preserved = dict(case_data)

        preserved["validation_status"] = "VALID"

        if not preserved.get("normalized_case_number"):

            preserved["normalized_case_number"] = incoming_case.upper()

        if not preserved.get("case_number"):

            preserved["case_number"] = incoming_case

        return preserved

    raw_case = str(case_data.get("case_number", "Unknown")).strip()

    raw_case = re.sub(r"\s+", " ", raw_case)

    normalized["case_number"] = raw_case

    normalized["normalized_case_number"] = raw_case.upper()

    normalized["confidence"] = int(case_data.get("confidence", 0))

    # =====================================================
    # 🔥 PRESERVE EXTRACTOR SEMANTIC METADATA
    # =====================================================

    normalized["case_type"] = case_data.get("case_type", normalized["case_type"])

    normalized["court_type"] = case_data.get("court_type", normalized["court_type"])

    normalized["jurisdiction"] = case_data.get(
        "jurisdiction", normalized["jurisdiction"]
    )

    normalized["proceeding_family"] = case_data.get(
        "proceeding_family", normalized["proceeding_family"]
    )

    normalized["source"] = case_data.get("source", normalized["source"])

    normalized["validation_status"] = case_data.get(
        "validation_status",
        normalized["validation_status"]
    )

    # =====================================================
    # 🔥 AUTHORITATIVE COURT LOCK
    # =====================================================

    authoritative_court = str(
        normalized.get(
            "court_type",
            ""
        )
    ).upper()

    normalized["_court_locked"] = (
        authoritative_court in [
            "SUPREME_COURT",
            "HIGH_COURT",
            "TRIBUNAL"
        ]
    )

    print("🔥 COURT LOCK STATUS:")
    print(normalized.get("_court_locked"))

    print("🔥 COURT TYPE BEFORE INFERENCE:")
    print(normalized.get("court_type"))

    # =====================================================
    # 🔥 YEAR EXTRACTION
    # =====================================================

    year_match = re.search(r"\b(19|20)\d{2}\b", raw_case)

    if year_match:
        normalized["year"] = year_match.group(0)

    upper = raw_case.upper()

    if (
        not normalized.get("_court_locked")
        and (
            "CRL.A" in upper
            or "SLP" in upper
            or "CIVIL APPEAL" in upper
            or "CRIMINAL APPEAL" in upper
        )
    ):
        normalized["court_type"] = "SUPREME_COURT"

    # =====================================================
    # 🔥 CASE NUMBER ONTOLOGY ENGINE
    # =====================================================

    if "CIVIL APPEAL" in upper:
        normalized["jurisdiction"] = "CIVIL"

    elif "CRIMINAL APPEAL" in upper:
        normalized["jurisdiction"] = "CRIMINAL"
        normalized["case_type"] = "CRIMINAL"

    elif "CRL.A" in upper or "CRL." in upper:
        normalized["jurisdiction"] = "CRIMINAL"
        normalized["case_type"] = "CRIMINAL"

    elif "C.A." in upper or "CIV.A" in upper:
        normalized["jurisdiction"] = "CIVIL"
        normalized["case_type"] = "CIVIL"

    elif "WP(" in upper:
        normalized["jurisdiction"] = "CONSTITUTIONAL"
        normalized["case_type"] = "WRIT"

    elif "SLP" in upper:
        normalized["jurisdiction"] = "SPECIAL_LEAVE"
        normalized["case_type"] = "SPECIAL_LEAVE"

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
        r"CONNECTED\s+WITH\s+(.*?)$",
    ]

    linked_cases = []

    for pattern in parent_patterns:

        try:

            matches = re.findall(pattern, upper, flags=re.I | re.M)

            for match in matches:

                cleaned = re.sub(r"\s+", " ", str(match)).strip()

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

    if normalized.get("jurisdiction") in ["CIVIL", "CRIMINAL", "SPECIAL_LEAVE"]:

        normalized["appellate_chain"] = linked_cases

    # =====================================================
    # 🔥 CONSTITUTIONAL CLUSTERING
    # =====================================================

    if "ARTICLE 32" in upper or "ARTICLE 226" in upper or "WRIT PETITION" in upper:

        normalized["constitutional_cluster"] = "CONSTITUTIONAL_LITIGATION"

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
        "MA",
    ]

    for item in CASE_TYPES:

        if item in ["OA", "TA", "MA"]:

            if re.search(
                rf"\b{re.escape(item)}\b",
                upper
            ):

                normalized["case_type"] = item
                break

        elif item in upper:

            normalized["case_type"] = item
            break

    # =====================================================
    # 🔥 COURT INFERENCE
    # =====================================================

    if normalized.get("_court_locked"):

        pass

    elif any(
        x in upper
        for x in [
            "SLP",
            "CIVIL APPEAL",
            "CRIMINAL APPEAL",
            "CURATIVE",
            "TRANSFER PETITION",
        ]
    ):

        normalized["court_type"] = "SUPREME COURT"

    elif any(x in upper for x in ["WP(C)", "CRM-M", "RSA", "CRL.REV"]):

        normalized["court_type"] = "HIGH COURT"

    elif re.search(
        r"\b(OA|TA|MA)\b",
        upper
    ):

        normalized["court_type"] = "TRIBUNAL"

    # =====================================================
    # 🔥 VALIDATION
    # =====================================================

    if normalized["case_number"] != "Unknown" and re.search(r"\d", raw_case):

        normalized["validation_status"] = "VALID"

    return normalized
