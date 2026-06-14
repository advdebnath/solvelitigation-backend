# =========================================================
# 🔥 SUPREME COURT IDENTITY ENGINE
# =========================================================
#
# PURPOSE:
# Permanent identity resolution for Supreme Court judgments
# from 1950 onwards.
#
# ERA SUPPORT:
# ERA1 = 1950-1969
# ERA2 = 1970-1994
# ERA3 = 1995-2004
# ERA4 = 2005-2014
# ERA5 = 2015-Present
#
# =========================================================

import re
from datetime import datetime

from app.extractors.historical_citation_extractor import (
    extract_historical_citations
)


# =========================================================
# ERA DETECTION
# =========================================================

def detect_supreme_court_era(judgment_date=None):

    try:

        if isinstance(judgment_date, dict):
            judgment_date = judgment_date.get("date")

        if not judgment_date:
            return "UNKNOWN"

        year = int(str(judgment_date)[:4])

        if year < 1970:
            return "ERA1"

        elif year < 1995:
            return "ERA2"

        elif year < 2005:
            return "ERA3"

        elif year < 2015:
            return "ERA4"

        return "ERA5"

    except Exception:
        return "UNKNOWN"


# =========================================================
# CITATION EXTRACTION
# =========================================================

def extract_identity_citation(full_text=""):

    if not full_text:
        return None

    patterns = [

        r"\(\d{4}\)\s*\d+\s*SCC\s*\d+",

        r"AIR\s*\d{4}\s*SC\s*\d+",

        r"JT\s*\d{4}\s*\(\d+\)\s*SC\s*\d+",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            full_text,
            re.I
        )

        if match:
            return match.group(0).strip()

    return None


# =========================================================
# IDENTITY BUILDER
# =========================================================

def build_supreme_identity(
    case_number="",
    petitioner="",
    respondent="",
    judgment_date=None,
    judges=None,
    full_text=""
):

    judges = judges or []

    era = detect_supreme_court_era(
        judgment_date
    )

    identity = {
        "courtEra": era,
        "canonicalCaseId": None,
        "identitySource": None,
        "identityConfidence": 0,
        "citationIdentity": None,
    }

    # =====================================================
    # PRIORITY 1
    # CASE NUMBER
    # =====================================================

    if case_number and str(case_number).upper() not in [
        "UNKNOWN CASE",
        "UNKNOWN",
        "",
        None,
    ]:

        canonical = (
            str(case_number)
            .upper()
            .replace(" ", "-")
            .replace("/", "-")
        )

        identity.update({
            "canonicalCaseId": canonical,
            "identitySource": "CASE_NUMBER",
            "identityConfidence": 100,
        })

        return identity

    # =====================================================
    # PRIORITY 2
    # CITATION
    # =====================================================

    historical = extract_historical_citations(
        full_text
    )

    print("🔥 SUPREME HISTORICAL CITATIONS 🔥")
    print(historical)

    citation = historical.get(
        "preferredCitation",
        ""
    )

    if citation:

        identity.update({
            "citationIdentity": citation,
            "canonicalCaseId": citation,
            "identitySource": "CITATION",
            "identityConfidence": 95,
        })

        return identity

    # =====================================================
    # PRIORITY 3
    # PARTY + DATE
    # =====================================================

    if (
        petitioner
        and respondent
        and judgment_date
    ):

        canonical = (
            f"SC-"
            f"{str(judgment_date)[:10]}-"
            f"{petitioner[:40]}-"
            f"{respondent[:40]}"
        )

        canonical = re.sub(
            r"[^A-Z0-9\-]",
            "-",
            canonical.upper()
        )

        identity.update({
            "canonicalCaseId": canonical,
            "identitySource": "PARTY_DATE",
            "identityConfidence": 80,
        })

        return identity

    # =====================================================
    # PRIORITY 4
    # BENCH + DATE
    # =====================================================

    if judges and judgment_date:

        judge_key = "-".join(
            [
                str(x)
                for x in judges[:2]
            ]
        )

        canonical = (
            f"SC-"
            f"{str(judgment_date)[:10]}-"
            f"{judge_key}"
        )

        canonical = re.sub(
            r"[^A-Z0-9\-]",
            "-",
            canonical.upper()
        )

        identity.update({
            "canonicalCaseId": canonical,
            "identitySource": "BENCH_DATE",
            "identityConfidence": 60,
        })

        return identity

    # =====================================================
    # FALLBACK
    # =====================================================

    identity.update({
        "canonicalCaseId": None,
        "identitySource": "UNRESOLVED",
        "identityConfidence": 0,
    })

    return identity
