import re

# =========================================================
# ð¥ CASE NUMBER PATTERNS
# =========================================================


# =========================================================
# ð¥ SUPREME COURT CANONICAL PATTERNS
# =========================================================

SUPREME_COURT_CASE_PATTERNS = [

    # -----------------------------------------------------
    # APPEALS
    # -----------------------------------------------------

    r"(CIVIL\s+APPEAL\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(CRIMINAL\s+APPEAL\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    # -----------------------------------------------------
    # SLP
    # -----------------------------------------------------

    r"(SPECIAL\s+LEAVE\s+PETITION\s*\((?:CRL\.?|CIVIL|CRIMINAL|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(SLP\s*\((?:CRL\.?|CIVIL|CRIMINAL|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    # -----------------------------------------------------
    # WRITS
    # -----------------------------------------------------

    r"(WRIT\s+PETITION\s*\((?:CRL\.?|CIVIL|CRIMINAL|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(SUO\s+MOTO\s+WRIT\s*\((?:CRL\.?|CRIMINAL|CIVIL|C)\)\s*NO\.?\(?S?\)?\s*[\dA-Z\-\/ ,.&()]+)",

    # -----------------------------------------------------
    # REVIEW / CURATIVE / TRANSFER
    # -----------------------------------------------------

    r"(REVIEW\s+PETITION\s*\((?:CRL\.?|CIVIL|CRIMINAL|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(CURATIVE\s+PETITION\s*\((?:CRL\.?|CIVIL|CRIMINAL|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(TRANSFER\s+PETITION\s*\((?:CRL\.?|CIVIL|CRIMINAL|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    # -----------------------------------------------------
    # DIARY
    # -----------------------------------------------------

    r"(DIARY\s+NO\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",
]

# =========================================================
# ð¥ HIGH COURT CANONICAL PATTERNS
# =========================================================

HIGH_COURT_CASE_PATTERNS = [

    # -----------------------------------------------------
    # WRITS
    # -----------------------------------------------------

    r"(WP\s*\(C\)\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(WP\s*\(CRL\)\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(W\.?(?:P|P\(C\))\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+)",

    # -----------------------------------------------------
    # CIVIL
    # -----------------------------------------------------

    r"(CRP\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(RSA\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(FAO\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(ARB\.?P\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    # -----------------------------------------------------
    # CRIMINAL
    # -----------------------------------------------------

    r"(CRM\-M\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(BAIL\s+APPLN\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(CRL\.?\s*REV\.?\s*P\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    r"(CRIMINAL\s+REVISION\s+NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",

    # -----------------------------------------------------
    # MOTOR ACCIDENT
    # -----------------------------------------------------

    r"(MAC\s*APP\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+(?:\s+OF\s+\d{4})?)",
]


# =========================================================
# ð¥ CANONICAL CASE FORMAT NORMALIZATION
# =========================================================

CANONICAL_CASE_PATTERNS = [

    (r"\bNO\.\s*\(S\)", "NO.(S)"),

    (r"\bNOS\.\b", "NOS."),

    (r"\bNO\.\b", "NO."),

    (r"\s+", " "),

    (r"IN RE:?$", ""),

    (r"CONNECTED MATTERS?$", ""),
]

# =========================================================
# ð¥ LEGACY / HIGH COURT / TRIBUNAL
# =========================================================

# =========================================================
# ð¥ CANONICAL CONFIDENCE ENGINE
# =========================================================

CASE_TYPE_CONFIDENCE = {

    # -----------------------------------------------------
    # SUPREME COURT
    # -----------------------------------------------------

    "CIVIL APPEAL": 95,

    "CRIMINAL APPEAL": 95,

    "SPECIAL LEAVE PETITION": 92,

    "SLP": 90,

    "WRIT PETITION": 90,

    "SUO MOTO WRIT": 94,

    "REVIEW PETITION": 88,

    "CURATIVE PETITION": 88,

    "TRANSFER PETITION": 87,

    "DIARY": 84,

    # -----------------------------------------------------
    # HIGH COURT
    # -----------------------------------------------------

    "WP(C)": 85,

    "WP(CRL)": 85,

    "CRP": 82,

    "RSA": 82,

    "CRM-M": 82,

    "CRL.REV": 82,

    "MAC APP": 80,

    "ARB.P": 80,

    "BAIL APPLN": 80,
}


CASE_PATTERNS = SUPREME_COURT_CASE_PATTERNS + HIGH_COURT_CASE_PATTERNS + [


    # =====================================================
    # ð¥ SUPREME COURT
    # =====================================================


    r"(SUO\s+MOTO\s+WRIT\s*\((?:CRL\.?|CRIMINAL|CIVIL|C)\)\s*NO\.?\(?S?\)?\s*[\dA-Z\-\/ ,.&()]+)",


    r"(WRIT\s+PETITION\s*\((?:CIVIL|CRIMINAL|CRL\.?|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(SPECIAL\s+LEAVE\s+PETITION\s*\((?:CIVIL|CRIMINAL|CRL\.?|C)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(SLP\s*\((?:C|CRL\.?|CIVIL|CRIMINAL)\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(CIVIL\s+APPEAL\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(CRIMINAL\s+APPEAL\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(SPECIAL\s+LEAVE\s+PETITION\s*\(.*?\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(SLP\s*\(.*?\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(WRIT\s+PETITION\s*\(.*?\)\s*NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(WRIT\s+PETITION\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(WRIT\s+PETITION\s+NO\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(CIVIL\s+APPEAL\s+NO\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(CRIMINAL\s+APPEAL\s+NO\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(TRANSFER\s+PETITION\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(REVIEW\s+PETITION\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",


    # =====================================================
    # ð¥ COMPACT / OCR / ABBREVIATED FORMS
    # =====================================================

    r"(C\.?A\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(CR\.?A\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(W\.?P\.?\s*\((?:C|CRL|CRIMINAL|CIVIL)\)\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(ARB\.?\s*P\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(DIARY\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(B\.?A\.?\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(CRM\-M\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(FAO\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    r"(LPA\s*NO\.?\s*[\dA-Z\-\/ ,.()]+?(?:\s+OF\s+\d{4})?)",

    # =====================================================
    # ð¥ HIGH COURT
    # =====================================================

    r"(WP\s*\(C\)\s*NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    r"(WP\s*\(CRL\)\s*NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    r"(CRL\.?A\.?\s*NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    r"(C\.?R\.?P\.?\s*NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    r"(RSA\s+NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    # =====================================================
    # ð¥ TRIBUNAL
    # =====================================================

    r"(OA\s+NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    r"(TA\s+NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    r"(MA\s+NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    r"(CP\s*\(IB\)\s*NO\.?\s*[\dA-Z\-\/]+(?:\s+OF\s+\d{4})?)",

    # =====================================================
    # ð¥ COMPANY / TAX
    # =====================================================

    r"(COMPANY\s+APPEAL\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    r"(TAX\s+APPEAL\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",

    # =====================================================
    # ð¥ GENERIC
    # =====================================================

    r"((?:CIVIL|CRIMINAL|FIRST|SECOND|REGULAR|MISC(?:ELLANEOUS)?|LETTERS\s+PATENT|INTRA-COURT|COMMERCIAL|COMPANY|TAX)\s+APPEAL\s+NOS?\.?\s*[\dA-Z\-\/ ,.&()]+?\s+OF\s+\d{4})",
]

# =========================================================
# ð¥ BAD VALUES
# =========================================================

BAD_PATTERNS = [

    ".pdf",
    "judgement_",
    "judgment_",
    "uploads/",
    "download",
    "scanned",
    "document",
    "file",
    ".doc",
    ".docx"
]

# =========================================================
# ð¥ SAFE OCR NORMALIZATION
# =========================================================

def normalize_ocr(text):

    # =====================================================
    # ð¥ SAFE OCR FIXES
    # =====================================================

    text = text.replace("|", "1")

    text = text.replace("â", "-")

    text = text.replace("â", "-")

    # =====================================================
    # ð¥ FIX OCR INSIDE NUMBERS ONLY
    # =====================================================

    text = re.sub(
        r"(?<=\d)O(?=\d)",
        "0",
        text
    )

    text = re.sub(
        r"(?<=\d)I(?=\d)",
        "1",
        text
    )

    text = re.sub(
        r"(?<=\d)l(?=\d)",
        "1",
        text
    )

    return text

# =========================================================
# ð¥ CLEAN CASE NUMBER
# =========================================================

def clean_case_number(value):

    value = value.replace(
        "\n",
        " "
    )

    value = re.sub(
        r"[ 	]+",
        " ",
        value
    )

    # =====================================================
    # ð¥ REMOVE HEADER POLLUTION
    # =====================================================

    HEADER_NOISE = [

        "REPORTABLE",
        "NON-REPORTABLE",
        "IN THE SUPREME COURT OF INDIA",
        "SUPREME COURT OF INDIA",
        "HIGH COURT OF",
        "APPELLATE JURISDICTION",
        "ORIGINAL JURISDICTION",
        "CIVIL APPELLATE JURISDICTION",
        "CRIMINAL APPELLATE JURISDICTION"
    ]

    for noise in HEADER_NOISE:

        value = re.sub(
            re.escape(noise),
            "",
            value,
            flags=re.IGNORECASE
        )

    # =====================================================
    # ð¥ FIX OCR STYLE
    # =====================================================

    value = re.sub(
        r"NOS\s+\.",
        "NOS.",
        value
    )

    value = re.sub(
        r"NO\s+\.",
        "NO.",
        value
    )

    value = re.sub(
        r"\.{2,}",
        ".",
        value
    )

    # =====================================================
    # ð¥ FIX SLASH SPACING
    # =====================================================

    value = re.sub(
        r"\s*/\s*",
        "/",
        value
    )

    value = value.strip(
        " :-.," 
    )

    value = re.sub(
        r"[ 	]+",
        " ",
        value
    ).strip()

    return value

# =========================================================
# ð¥ VALIDATION
# =========================================================

def is_valid_case_number(value):

    if not value:
        return False

    value = str(value).strip()

    upper = value.upper()

    # =====================================================
    # ð¥ BASIC STRUCTURE CHECK
    # =====================================================

    if len(value) < 8:
        return False

    # =====================================================
    # ð¥ MUST CONTAIN DIGITS
    # =====================================================

    if not re.search(r"\d", value):
        return False

    # =====================================================
    # ð¥ MUST CONTAIN CASE KEYWORDS
    # =====================================================

    VALID_KEYWORDS = [

        "APPEAL",
        "PETITION",
        "WRIT",
        "SLP",
        "SPECIAL LEAVE",
        "DIARY",
        "TRANSFER",
        "REVIEW",

        # =================================================
        # 🔥 TRIBUNAL / SHORT FORMS
        # =================================================

        "OA",
        "TA",
        "MA",
        "BA",
        "WP",

        # =================================================
        # 🔥 CRIMINAL SHORT FORMS
        # =================================================

        "CRL",
        "CRL.A",
        "CRL.A.",
        "CR.A",
        "CR.A.",
        "CRL APPEAL",

        # =================================================
        # 🔥 CIVIL SHORT FORMS
        # =================================================

        "C.A",
        "C.A.",
        "CIVIL APPEAL",

        # =================================================
        # 🔥 FULL FORMS
        # =================================================

        "CIVIL",
        "CRIMINAL"
    ]

    if not any(
        keyword in upper
        for keyword in VALID_KEYWORDS
    ):
        return False

    # =====================================================
    # ð¥ REJECT FILE POLLUTION
    # =====================================================

    BAD_VALUES = [

        ".PDF",
        ".DOC",
        ".DOCX",
        "UPLOAD",
        "DOWNLOAD",
        "SCANNED",
        "DOCUMENT"
    ]

    if any(
        x in upper
        for x in BAD_VALUES
    ):
        return False

    # =====================================================
    # ð¥ MUST HAVE NUMBER STRUCTURE
    # =====================================================

    # =====================================================
    # 🔥 FLEXIBLE CASE NUMBER STRUCTURE
    # =====================================================

    flexible_patterns = [

        r"NO\.?\s*[\dA-Z/\-]+",

        r"NOS\.?\s*[\dA-Z/\-]+",

        r"NO\s+[\dA-Z/\-]+",

        r"OF\s+\d{4}",

        r"\d+\s+OF\s+\d{4}"
    ]

    if not any(
        re.search(pattern, upper)
        for pattern in flexible_patterns
    ):
        return False

    return True

# =========================================================
# ð¥ CASE CANDIDATE PRIORITIZATION ENGINE
# =========================================================

def rank_case_candidates(candidates):

    if not candidates:
        return []

    ranked = []

    for item in candidates:

        try:

            value = str(
                item.get(
                    "case_number",
                    ""
                )
            ).upper()

            confidence = int(
                item.get(
                    "confidence",
                    0
                )
            )

            score = confidence

            # =================================================
            # ð¥ PRIMARY SUPREME COURT MATTERS
            # =================================================

            if "CIVIL APPEAL" in value:
                score += 40

            if "CRIMINAL APPEAL" in value:
                score += 40

            if "WRIT PETITION" in value:
                score += 35

            if "SLP" in value:
                score += 30

            if "APPEAL (CIVIL)" in value:
                score += 45

            if "APPEAL (CRL" in value:
                score += 45

            # =================================================
            # ð¥ SECONDARY / PROCEDURAL MATTERS
            # =================================================

            secondary_penalties = [

                "IA NO",
                "INTERLOCUTORY",
                "DIARY",
                "MISC.",
                "M.A.",
                "REVIEW PETITION",
                "CONTEMPT",
                "CURATIVE",
                "CONNECTED",
                "TRANSFERRED CASE"
            ]

            for token in secondary_penalties:

                if token in value:
                    score -= 35

            # =================================================
            # ð¥ OCR CLEANLINESS BONUS
            # =================================================

            if not re.search(r"[|]{1,}", value):
                score += 5

            if len(value.split()) >= 3:
                score += 5

            ranked.append({
                **item,
                "ranking_score": score
            })

        except Exception:
            continue

    ranked.sort(
        key=lambda x: x.get(
            "ranking_score",
            0
        ),
        reverse=True
    )

    print("RANKED CASE CANDIDATES:")
    print(ranked[:5])

    return ranked

# =========================================================
# ð¥ MAIN EXTRACTION
# =========================================================
def extract_case_number(

    text,

    fallback="Unknown Case"
):

    try:

        if not text:

            return {
                "case_number": fallback,
                "confidence": 0
            }

        # =====================================================
        # =====================================================
        # ð¥ SEMANTIC FIRST-PAGE EXTRACTION
        # =====================================================

        header = text

        # =====================================================
        # ð¥ OCR NORMALIZATION FIREWALL
        # =====================================================

        OCR_NORMALIZATION_RULES = [

            (r"WR[lI]T", "WRIT"),

            (r"CR[lI]MINAL", "CRIMINAL"),

            (r"CR[lI]L", "CRL"),

            (r"N[O0]\.", "NO."),

            (r"NO\(S\)", "NO.(S)"),

            (r"S\.L\.P\.?", "SLP"),

            (r"W\.P\.\(C\)", "WP(C)"),

            (r"W\.P\.\(CRL\)", "WP(CRL)"),

            (r"APPEALN[O0]", "APPEAL NO"),

            (r"PETITIONN[O0]", "PETITION NO"),

            (r"\s{2,}", " "),
        ]

        for pattern, replacement in OCR_NORMALIZATION_RULES:

            try:

                header = re.sub(
                    pattern,
                    replacement,
                    header,
                    flags=re.I
                )

            except Exception:
                pass

        page_break_patterns = [

            r"(?i)for petition",
            r"(?i)for respondent",
            r"(?i)appearance",
            r"(?i)aor",
            r"(?i)advocate",
            r"(?i)senior advocate",
            r"(?i)video conferencing",
            r"(?i)connected matter",
            r"(?i)item no",
            r"(?i)court no",
            r"(?i)interlocutory application",
            r"(?i)applns?\.\s+for",
            r"(?i)disposed of"
        ]

        semantic_cutoffs = []

        for pattern in page_break_patterns:

            try:

                match = re.search(pattern, header)

                if match:
                    semantic_cutoffs.append(match.start())

            except Exception:
                pass

        if semantic_cutoffs:

            cutoff = min(semantic_cutoffs)

            if cutoff > 500:

                header = header[:cutoff]

        header = header[:12000]

        # normalize_ocr temporarily bypassed

        print("\nð¥ SEMANTIC HEADER ISOLATION ð¥")
        print(header[:4000])

        print("\nHEADER LINE TRACE")

        for idx, line in enumerate(
            header.splitlines()[:80],
            start=1
        ):
            print(f"{idx:03d}: {line}")
        print("ð¥ END HEADER ISOLATION ð¥\n")

        # =====================================================
        # ð¥ ADVANCED CASE HEADER RECONSTRUCTION
        # =====================================================

        header = re.sub(
              r"\bN0\b",
            "NO",
            header,
            flags=re.I
        )

        header = re.sub(
              r"\b0F\b",
            "OF",
            header,
            flags=re.I
        )

        # -----------------------------------------------------
        # ð¥ JOIN BROKEN CASE TYPE LINES
        # -----------------------------------------------------

        header = re.sub(
            r"(?i)(CRIMINAL|CIVIL|SPECIAL|WRIT|TRANSFER|REVIEW|COMPANY|TAX)\s*\s*(APPEAL|PETITION)",
            r" \1 \2",
            header
        )

        # -----------------------------------------------------
        # ð¥ JOIN BROKEN NO LINES
        # -----------------------------------------------------

        header = re.sub(
            r"(?i)(NO\.?|NOS\.?)\s*\s*(\d)",
            r" \1 \2",
            header
        )
        # ð¥ JOIN BROKEN OF YEAR LINES
        # -----------------------------------------------------

        header = re.sub(
            r"(?i)(\d)\s*\s*OF\s*\s*(\d{4})",
            r" \1 OF \2",
            header
        )

        header = re.sub(
            r"(?i)(\d)\s*\s*OF\s+(\d{4})",
            r" \1 OF \2",
            header
        )

        # -----------------------------------------------------
        # ð¥ COLLAPSE EXCESS NEWLINES
        # -----------------------------------------------------

        header = re.sub(
            r"\n+",
            "\n",
            header
        )

        # =====================================================
        # ð¥ RAW HEADER DEBUG
        # =====================================================

        print("\nRAW HEADER START")
        print(header[:5000])
        print("RAW HEADER END\n")

        header = re.sub(
            r"[ 	]+",
            " ",
            header
        )

        # =====================================================
        # ð¥ MULTILINE CASE RECONSTRUCTION
        # =====================================================


        # =====================================================
        # 🔥 SAFE NO./NOS. NORMALIZATION
        # =====================================================

        header = re.sub(
            r"(NO\.?|NOS\.?)\s+",
            r" \1 ",
            header,
            flags=re.I
        )

        header = re.sub(
            r"\s*(OF\s+\d{4})",
            r" \1",
            header,
            flags=re.I
        )

        header = re.sub(
            r"(PETITION|APPEAL|APPLICATION|CASE)\s*\s*(NO\.?|NOS\.?)",
            r" \1 \2",
            header,
            flags=re.I
        )

        # =====================================================
        # ð¥ OCR-AWARE CASE TOKEN COLLAPSE
        # =====================================================

        OCR_CASE_FIXES = {

            r"APPEA\s+L":
                "APPEAL",

            r"CRIMINA\s+L":
                "CRIMINAL",

            r"CIVI\s+L":
                "CIVIL",

            r"PETITIO\s+N":
                "PETITION",

            r"APPLICATIO\s+N":
                "APPLICATION",

            r"SPECIA\s+L":
                "SPECIAL",

            r"LEAV\s+E":
                "LEAVE",

            r"N\s+O\s*\.":
                "NO.",

            r"N\s+O\s*S\s*\.":
                "NOS.",

            r"WRI\s+T":
                "WRIT",

            r"CAS\s+E":
                "CASE",

            r"SUI\s+T":
                "SUIT"
        }

        for wrong, correct in OCR_CASE_FIXES.items():

            header = re.sub(
                wrong,
                correct,
                header,
                flags=re.I
            )

          # whitespace collapse temporarily disabled
        # =====================================================
        # =====================================================
        # ð¥ AGGRESSIVE CASE HEADER RECONSTRUCTION
        # =====================================================

        AGGRESSIVE_CASE_FIXES = {

            r"CRIMI\s+NAL":
                "CRIMINAL",

            r"CIVI\s+L":
                "CIVIL",

            r"APPEA\s+L":
                "APPEAL",

            r"PETITI\s+ON":
                "PETITION",

            r"APPLICATI\s+ON":
                "APPLICATION",

            r"SPECIA\s+L":
                "SPECIAL",

            r"LEAV\s+E":
                "LEAVE",

            r"WRI\s+T":
                "WRIT",

            r"CAS\s+E":
                "CASE",

            r"N\s+O\s*\.":
                "NO.",

            r"N\s+O\s*S\s*\.":
                "NOS.",

            r"O\s+F\s+(\d{4})":
                r"OF "
        }

        for wrong, correct in AGGRESSIVE_CASE_FIXES.items():

            try:

                header = re.sub(
                    wrong,
                    correct,
                    header,
                    flags=re.I
                )

            except Exception as aggressive_error:

                print("❌ AGGRESSIVE FIX ERROR:")
                print(wrong)
                print(correct)
                print(str(aggressive_error))

                continue


        # =====================================================
        # ð¥ CANONICAL CASE FORMAT NORMALIZATION ENGINE
        # =====================================================


        for pattern, replacement in CANONICAL_CASE_PATTERNS:

            try:

                header = re.sub(
                    pattern,
                    replacement,
                    header,
                    flags=re.I
                )

            except Exception as canonical_error:

                print("❌ CANONICAL NORMALIZATION ERROR:")
                print(pattern)
                print(replacement)
                print(str(canonical_error))

                continue

        print("\nð¥ CANONICAL CASE HEADER ð¥")
        print(header[:5000])
        print("ð¥ END CANONICAL HEADER ð¥\n")

        # =====================================================

        # =====================================================
        # ð¥ CANDIDATE COLLECTION ENGINE
        # =====================================================

                # =====================================================
        # 🔥 LOCKED INDIAN JUDICIARY CASE EXTRACTION ENGINE
        # =====================================================

        normalized_header = re.sub(
            r"\s+",
            " ",
            header
        )

        COURT_CASE_PATTERNS = [

            # =================================================
            # 🔥 SUPREME COURT OF INDIA
            # =================================================

            r"((?:CRIMINAL|CIVIL)\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d{4})",

            r"((?:SPECIAL\s+LEAVE\s+PETITION|SLP).*?\d+\s+OF\s+\d{4})",

            r"((?:WRIT\s+PETITION|W\.?P\.?).*?\d+\s+OF\s+\d{4})",

            r"((?:TRANSFER\s+PETITION|TRANSFER\s+CASE).*?\d+\s+OF\s+\d{4})",

            r"((?:REVIEW\s+PETITION|CURATIVE\s+PETITION).*?\d+\s+OF\s+\d{4})",

            r"((?:CONTEMPT\s+PETITION).*?\d+\s+OF\s+\d{4})",

            # =================================================
            # 🔥 HIGH COURTS
            # =================================================

            r"((?:CRL\.?|CRM|CRA|CRA-D|CRR|BA|ARB)\s*[-A-Z()\/]*\s*\d+[-\/]\d{4})",

            r"((?:CWP|CWJC|LPA|RSA|RFA|FAO|MACA)\s+NO\.?\s*\d+\s+OF\s+\d{4})",

            r"((?:W\.?P\.?\(?C?\)?).*?\d+\/\d{4})",

            r"((?:CRIMINAL|CIVIL)\s+REVISION\s+NO\.?\s*\d+\s+OF\s+\d{4})",

            # =================================================
            # 🔥 TRIBUNALS
            # =================================================

            r"((?:OA|TA)\s+NO\.?\s*\d+\/\d{4})",

            r"((?:CP\s*\(IB\)|IA\s*\(IB\)).*?\d+\/[A-Z]+\/\d{4})",

            r"((?:COMPANY\s+PETITION).*?\d+\s+OF\s+\d{4})",

            r"((?:ITA|ITA\s+NO\.?).*?\d+\/[A-Z]+\/\d{4})",

            r"((?:GST\s+APPEAL).*?\d+\s+OF\s+\d{4})"
        ]

        # =====================================================
        # 🔥 AUTHORITATIVE LOCKED EXTRACTION ENGINE
        # =====================================================

        for locked_pattern in COURT_CASE_PATTERNS:

            try:

                locked_match = re.search(
                    locked_pattern,
                    normalized_header,
                    flags=re.I
                )

                if locked_match:

                    direct_case = clean_case_number(
                        locked_match.group(1)
                    )

                    print("🔥 LOCKED COURT MATCH:")
                    print(direct_case)

                    return {
                        "case_number": direct_case,
                        "canonical_case_number": direct_case,
                        "normalized_case_number": direct_case,
                        "case_type": "LOCKED_CASE_PATTERN",
                        "source": "LOCKED_JUDICIARY_ENGINE",
                        "court": "INDIAN COURT SYSTEM",
                        "confidence": 99,
                        "validation_passed": True
                    }

            except Exception as locked_error:

                print("❌ LOCKED PATTERN ERROR:")
                print(locked_pattern)
                print(str(locked_error))

        # =====================================================
        # 🔒 PERMANENT INDIAN JUDICIARY LOCK ENGINE
        # =====================================================

        LOCKED_CASE_PATTERNS = [

            r"(CRIMINAL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(CIVIL\s+APPEAL\s+NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(SPECIAL\s+LEAVE\s+PETITION\s*\(?[A-Z]*\)?\s*NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(WRIT\s+PETITION\s*\(?[A-Z]*\)?\s*NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(TRANSFER\s+PETITION\s*\(?[A-Z]*\)?\s*NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(REVIEW\s+PETITION\s*\(?[A-Z]*\)?\s*NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(CONTEMPT\s+PETITION\s*\(?[A-Z]*\)?\s*NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(CRL\.?A\.?\s*\d+/?\d{4})",

            r"(W\.P\.\(C\)\s*NO\.?\s*\d+\s+OF\s+\d{4})",

            r"(W\.P\.\(CRL\.?\)\s*NO\.?\s*\d+\s+OF\s+\d{4})"
        ]

        for locked_pattern in LOCKED_CASE_PATTERNS:

            try:

                locked_match = re.search(
                    locked_pattern,
                    header,
                    flags=re.I
                )

                if locked_match:

                    direct_case = clean_case_number(
                        locked_match.group(1)
                    )

                    print("🔥 LOCKED COURT MATCH:")
                    print(direct_case)

                    return {
                        "case_number": direct_case,
                        "canonical_case_number": direct_case,
                        "normalized_case_number": direct_case,
                        "case_type": "LOCKED_CASE_PATTERN",
                        "source": "LOCKED_JUDICIARY_ENGINE",
                        "court": "INDIAN COURT SYSTEM",
                        "confidence": 100,
                        "validation_passed": True
                    }

            except Exception as locked_error:

                print("❌ LOCKED PATTERN ERROR:")
                print(locked_pattern)
                print(str(locked_error))

        candidate_results = []

        for pattern in CASE_PATTERNS:

            try:

                matches = re.findall(
                    pattern,
                    header,
                    flags=re.I
                )

            except Exception as regex_error:

                print("â CASE REGEX ERROR:")
                print(pattern)
                print(str(regex_error))

                continue

            for match in matches:

                # ============================================
                # ð¥ TUPLE NORMALIZATION
                # ============================================

                if isinstance(match, tuple):

                    match = " ".join(
                        str(x).strip()
                        for x in match
                        if x and str(x).strip()
                    )

                value = clean_case_number(
                    str(match)
                )

                # ============================================
                # ð¥ PROCEDURAL SUFFIX FIREWALL
                # ============================================

                PROCEDURAL_SUFFIXES = [

                    " IN RE",
                    " PETITIONER",
                    " PETITIONERS",
                    " RESPONDENT",
                    " RESPONDENTS",
                    " APPELLANT",
                    " APPELLANTS",
                    " ORDER",
                    " JUDGMENT",
                    " CONNECTED MATTERS",
                    " CONNECTED CASES",
                    " WITH CONNECTED",
                ]

                upper_value_cleanup = value.upper()

                for suffix in PROCEDURAL_SUFFIXES:

                    if upper_value_cleanup.endswith(suffix):

                        value = value[
                            : -len(suffix)
                        ].strip()

                        upper_value_cleanup = value.upper()


                print("ð¥ CANDIDATE BEFORE VALIDATION:")
                print(value)

                print("ð¥ VALIDATION RESULT:")
                print(is_valid_case_number(value))

                if not is_valid_case_number(value):
                    continue

                confidence = 50

                upper_value = value.upper()


                
                # -------------------------------------------------
                # ð¥ CANONICAL CONFIDENCE ENGINE
                # -------------------------------------------------

                for case_key, score in CASE_TYPE_CONFIDENCE.items():

                    if case_key in upper_value:

                        confidence = max(
                            confidence,
                            score
                        )



                # -------------------------------------------------
                # ð¥ OCR PENALTIES
                # -------------------------------------------------

                if re.search(r"[|]{1,}", value):
                    confidence -= 20

                if len(value.split()) < 2:
                    confidence -= 25

                # -------------------------------------------------
                # ð¥ HEADER CONTEXT BOOST
                # -------------------------------------------------

                if "SUPREME COURT" in header.upper():
                    confidence += 5

                candidate_results.append({

                    "case_number": value,

                    "confidence": max(
                        0,
                        min(100, confidence)
                    )
                })

        # =====================================================
        # ð¥ GENERIC SEMANTIC FALLBACK
        # =====================================================

        generic_patterns = [

            r"CASE\s+NO\.?\s*[:\-]?\s*(Appeal\s*\((?:civil|crl\.?|criminal)\)\s*\d+\s*of\s*\d{4})",

            r"Appeal\s*\((?:civil|crl\.?|criminal)\)\s*\d+\s*of\s*\d{4}",

            r"Petition\s*\((?:civil|crl\.?|criminal)\)\s*\d+\s*of\s*\d{4}",

            r"Transfer\s+(?:Case|Petition)\s*\(?[A-Z]*\)?\s*\d+\s*of\s*\d{4}",

            r"(?:CRIMINAL|CIVIL)\s+APPEAL\s+NO\.?\s*[\d\/\-]+\s+OF\s+\d{4}",

            r"WRIT\s+PETITION.*?NO\.?\s*[\d\/\-]+\s+OF\s+\d{4}",

            r"SLP.*?NO\.?\s*[\d\/\-]+\s+OF\s+\d{4}",

            r"[A-Z .()\/-]+NO\.?\s*[\d\/\-]+\s+OF\s+\d{4}"
        ]

        for pattern in generic_patterns:

            try:

                fallback_matches = re.findall(
                    pattern,
                    header,
                    flags=re.I
                )

            except Exception:
                continue

            for match in fallback_matches:

                value = clean_case_number(match)


                print("ð¥ CANDIDATE BEFORE VALIDATION:")
                print(value)
                print(repr(value))


                print("ð¥ VALIDATION RESULT:")
                print(is_valid_case_number(value))

                if not is_valid_case_number(value):
                    continue

                candidate_results.append({

                    "case_number": value,

                    "confidence": 60
                })

        # =====================================================
        # ð¥ FINAL BEST CANDIDATE
        # =====================================================

        if candidate_results:

            candidate_results = rank_case_candidates(
                candidate_results
            )

            best = candidate_results[0]

            print("BEST CASE NUMBER:")
            print(best)

            return best

        # =====================================================
        # ð¥ FINAL FAILURE
        # =====================================================


        # =====================================================
        # ð¥ PARTY TITLE FALLBACK
        # =====================================================

        petitioner_match = re.search(
            r"PETITIONER\s*:?\s*([A-Z0-9][A-Z0-9\s\.\&\,\-\(\)\/\']+?)(?=RESPONDENT|DATE OF JUDGMENT|BENCH|JUDGMENT|$)",
            header,
            flags=re.I
        )

        respondent_match = re.search(
            r"RESPONDENT\s*:?\s*([A-Z0-9][A-Z0-9\s\.\&\,\-\(\)\/\']+?)(?=DATE OF JUDGMENT|BENCH|JUDGMENT|$)",
            header,
            flags=re.I
        )

        if petitioner_match and respondent_match:

            petitioner = petitioner_match.group(1).strip()
            respondent = respondent_match.group(1).strip()

            respondent = re.sub(
                r"(?i)^\s*(V|VS|VS\.|VERSUS)\s+",
                "",
                respondent
            ).strip()

            title_case = (
                f"{petitioner} Vs. {respondent}"
            )

            title_case = re.sub(
                r"Vs\.\s+Vs\.",
                "Vs.",
                title_case,
                flags=re.I
            )

            title_case = re.sub(
                r"\s+",
                " ",
                title_case
            ).strip()

            print("🔥 AUTHORITATIVE PARTY TITLE FALLBACK:")
            print(title_case)

            return {
                "case_number": title_case,
                "canonical_case_number": title_case,
                "normalized_case_number": title_case,
                "case_type": "PARTY_TITLE_FALLBACK",
                "source": "PETITIONER_RESPONDENT_CAPTION",
                "court": "SUPREME COURT OF INDIA",
                "confidence": 82,
                "validation_passed": True
            }

        print("â CASE NUMBER NOT FOUND")

        return {
            "case_number": fallback,
            "confidence": 0
        }

    except Exception as e:

        print("â CASE NUMBER EXTRACTION ERROR:")
        print(str(e))

        import traceback

        print("❌ FULL TRACEBACK:")
        traceback.print_exc()

        return {
            "case_number": fallback,
            "confidence": 0
        }
