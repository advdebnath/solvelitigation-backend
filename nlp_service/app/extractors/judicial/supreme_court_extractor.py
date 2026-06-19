# =========================================================
# 🔥 SUPREME COURT EXTRACTOR
# =========================================================

import re

from app.extractors.judicial.shared_utils import (build_case_object,
                                                  clean_case_number,
                                                  normalize_ocr)


SC_PATTERNS = [

    (
        r"(CIVIL\s+APPEAL\s+NOS?\.?\s*[\d\-\/]+(?:\s+OF\s+\d{4}|/\d{4}))",
        "CIVIL"
    ),

    (
        r"(CRIMINAL\s+APPEAL\s+NOS?\.?\s*[\d\-\/]+(?:\s+OF\s+\d{4}|/\d{4}))",
        "CRIMINAL"
    ),


    # =====================================================
    # 🔥 MODERN SUPREME COURT APPEALS
    # =====================================================

    (
        r"(CIVIL\s+APPEAL\s+NOS?\.?\s*[\d\-\/]+(?:\s+OF\s+\d{4}|/\d{4}))",
        "CIVIL"
    ),

    (
        r"(CRIMINAL\s+APPEAL\s+NOS?\.?\s*[\d\-\/]+(?:\s+OF\s+\d{4}|/\d{4}))",
        "CRIMINAL"
    ),

    (
        r"(CIVIL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d{4})",
        "CIVIL"
    ),

    (
        r"(CRIMINAL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d{4})",
        "CRIMINAL"
    ),
    (
        r"(SPECIAL\s+LEAVE\s+PETITION\s*\(?[A-Z]*\)?\s*NO\.?\(?S\)?\.?\s*[\d\-\/]+\s*(?:OF\s+\d{4})?)",
        "SPECIAL_LEAVE"
    ),

    (
        r"(PETITION\s+FOR\s+SPECIAL\s+LEAVE\s+TO\s+APPEAL\s*"
        r"\([A-Z\.]+\)\s*"
        r"NO\.?\s*[\d\-\/]+\s*"
        r"(?:OF\s*\n*\s*\d{4})?)",
        "SPECIAL_LEAVE"
    ),
    (r"(WRIT\s+PETITION.*?NO\.?\s*\d+\s+OF\s+\d{4})", "WRIT"),
    (r"(REVIEW\s+PETITION\s*\((?:CRL\.?|C|CIVIL|CRIMINAL)\)\s*NO\.?\s*\d+(?:[-/,]\d+)*\s+OF\s+\d{4})", "REVIEW"),
]


def extract_sc_case_number(text):

    text = normalize_ocr(text)

    upper = text.upper()

    upper = upper.replace("\\N", " ")

    upper = re.sub(
        r"\s+",
        " ",
        upper
    )

    print("🔥 SC HEADER START 🔥")
    print(upper[:4000])
    print("🔥 SC HEADER END 🔥")

    candidates = []

    for pattern, case_type in SC_PATTERNS:

        try:

            matches = re.findall(pattern, upper, flags=re.I)

        except Exception as e:

            print("❌ SC REGEX ERROR:")
            print(str(e))

            continue

        for match in matches:

            value = clean_case_number(match)

            print("🔥 SC MATCH:")
            print(value)

            print("🔥 SC MATCH RAW:")
            print(repr(match))

            print("🔥 SC MATCH CLEAN:")
            print(repr(value))

            if re.search(r"\d{2,}", value):

                return build_case_object(
                    case_number=value,
                    court_type="SUPREME COURT",
                    case_type=case_type,
                    confidence=100,
                    source="SC_EXTRACTOR_V2",
                )


    if candidates:

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        best = candidates[0]

        print("🔥 SC BEST CANDIDATE:")
        print(best)

        return build_case_object(
            case_number=best["value"],
            court_type="SUPREME COURT",
            case_type=best["case_type"],
            confidence=100,
            source="SC_EXTRACTOR_V3"
        )


    # =====================================================
    # 🔥 HISTORICAL JUDIS FALLBACK
    # =====================================================

    header_for_party = upper

    header_for_party = re.sub(
        r"\\N",
        " ",
        header_for_party
    )

    header_for_party = re.sub(
        r"\s+",
        " ",
        header_for_party
    )

    print("🔥 PARTY HEADER NORMALIZED 🔥")
    print(header_for_party[:1000])

    vs_pos = header_for_party.find("VS.")

    if vs_pos != -1:

        search_window = header_for_party[
            max(0, vs_pos - 200):
            vs_pos + 250
        ]

    else:

        search_window = header_for_party

    print("🔥 PARTY SEARCH WINDOW 🔥")
    print(search_window)

    party_match = re.search(
        r"""
        ([A-Z][A-Z0-9\s\.\,&'()/\-]{3,300}?)
        \s+
        (?:VS\.?|VERSUS|V\.)
        \s+
        ([A-Z][A-Z0-9\s\.\,&'()/\-]{3,300}?)
        \s+
        DATE\s+OF
        """,
        search_window,
        re.I | re.S | re.X
    )

    print("🔥 PARTY_MATCH:")
    print(bool(party_match))

    if party_match:

        petitioner = re.sub(
            r"\s+",
            " ",
            party_match.group(1)
        ).strip()

        petitioner = re.sub(
            r"^.*?SUPREME\s+COURT+T*\s+OF\s+INDIA\s+",
            "",
            petitioner,
            flags=re.I
        )

        respondent = re.sub(
            r"\s+",
            " ",
            party_match.group(2)
        ).strip()

        synthetic_case = (
            f"{petitioner} VS. {respondent}"
        )

        print("🔥 SC HISTORICAL FALLBACK:")
        print(synthetic_case)

        return build_case_object(
            case_number=synthetic_case,
            court_type="SUPREME COURT",
            case_type="HISTORICAL",
            confidence=85,
            source="SC_HISTORICAL_FALLBACK"
        )

    # =====================================================
    # 🔥 PETITION TITLE FALLBACK
    # =====================================================

    title_match = re.search(
        r"(?:TRANSFER\s+PETITION|WRIT\s+PETITION|SPECIAL\s+LEAVE\s+PETITION)[^\n]{0,100}?NO\.?\s*[\d\/\-]+\s*\n?\s*([A-Z][A-Z \.]{3,80}?)\s*(?:VERSUS|VS\.?|O\s+R\s+D\s+E\s+R|ORDER)",
        header_for_party,
        re.I
    )

    print("🔥 TITLE_MATCH:")
    print(bool(title_match))

    if title_match:

        numbered_case = re.search(
            r"(WRIT\s+PETITION.*?NO\.?\s*[\d/\-]+|"
            r"SPECIAL\s+LEAVE\s+PETITION.*?NO\.?\s*[\d/\-]+|"
            r"PETITION\s+FOR\s+SPECIAL\s+LEAVE\s+TO\s+APPEAL.*?NO\.?\s*[\d/\-]+(?:\s*OF\s+\d{4})?|"
            r"TRANSFER\s+PETITION.*?NO\.?\s*[\d/\-]+)",
            header_for_party,
            re.I | re.S
        )

        if numbered_case:

            extracted_case = re.sub(
                r"\s+",
                " ",
                numbered_case.group(1)
            ).strip().upper()

            print(
                "🔒 NUMBERED CASE OVERRIDE"
            )
            print(extracted_case)

            return build_case_object(
                case_number=extracted_case,
                court_type="SUPREME COURT",
                case_type="PETITION",
                confidence=100,
                source="SC_NUMBERED_CASE_OVERRIDE"
            )

        petitioner = re.sub(
            r"\s+",
            " ",
            title_match.group(1)
        ).strip()

        print("🔥 PETITION TITLE FALLBACK:")
        print(petitioner)

    # =====================================================
    # 🔥 WRIT PETITION NAME FALLBACK
    # =====================================================

    writ_match = re.search(
        r"WRIT\s+PETITION.*?NO\.?\s*[\d\/\-]+\s+([A-Z][A-Z\s\.]{5,80})\s+J\s*U\s*D\s*G\s*M\s*E\s*N\s*T",
        header_for_party,
        re.I | re.S
    )

    print("🔥 WRIT_MATCH:")
    print(bool(writ_match))

    if writ_match:

        petitioner = re.sub(
            r"\s+",
            " ",
            writ_match.group(1)
        ).strip()

        print("🔥 WRIT FALLBACK:")
        print(petitioner)

        return build_case_object(
            case_number=petitioner,
            court_type="SUPREME COURT",
            case_type="WRIT PETITION",
            confidence=80,
            source="SC_WRIT_FALLBACK"
        )


    # =====================================================
    # 🔥 DERIVED CASE RECOVERY ENGINE
    # =====================================================

    derived_match = re.search(
        r"(S\.?L\.?P\.?\s*\([A-Z]+\)\s*NO\.?\s*\d+\s*OF\s*\d{4})",
        header_for_party,
        re.I
    )

    if derived_match:

        recovered = re.sub(
            r"\s+",
            " ",
            derived_match.group(1)
        ).strip().upper()

        print("🔥 DERIVED SLP RECOVERY 🔥")
        print(recovered)

        return build_case_object(
            case_number=recovered,
            court_type="SUPREME COURT",
            case_type="SPECIAL_LEAVE",
            confidence=95,
            source="SC_DERIVED_CASE_RECOVERY"
        )

    derived_match = re.search(
        r"(SPECIAL\s+LEAVE\s+PETITION\s*\([A-Z\.]+\)\s*NO\.?\s*\d+\s*OF\s*\d{4})",
        header_for_party,
        re.I
    )

    if derived_match:

        recovered = re.sub(
            r"\s+",
            " ",
            derived_match.group(1)
        ).strip().upper()

        print("🔥 DERIVED SPECIAL LEAVE RECOVERY 🔥")
        print(recovered)

        return build_case_object(
            case_number=recovered,
            court_type="SUPREME COURT",
            case_type="SPECIAL_LEAVE",
            confidence=95,
            source="SC_DERIVED_CASE_RECOVERY"
        )

    derived_match = re.search(
        r"(DIARY\s+NO\.?\s*\d+\s*(?:OF|\/)\s*\d{4})",
        header_for_party,
        re.I
    )

    if derived_match:

        recovered = re.sub(
            r"\s+",
            " ",
            derived_match.group(1)
        ).strip().upper()

        print("🔥 DERIVED DIARY RECOVERY 🔥")
        print(recovered)

        return build_case_object(
            case_number=recovered,
            court_type="SUPREME COURT",
            case_type="DIARY",
            confidence=95,
            source="SC_DERIVED_CASE_RECOVERY"
        )


    if title_match:

        return build_case_object(
            case_number="Unknown Case",
            court_type="SUPREME COURT",
            case_type="PETITION",
            confidence=20,
            source="SC_PETITION_TITLE_FALLBACK"
        )


    return None

