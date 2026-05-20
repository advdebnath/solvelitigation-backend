import re

# =========================================================
# 🔥 OCR SAFE NORMALIZATION
# =========================================================

def normalize_ocr_text(text):

    if not isinstance(text, str):
        text = str(text)

    replacements = {

        "S C C": "SCC",
        "S. C. C.": "SCC",

        "A I R": "AIR",
        "S C": "SC",

        "On Line": "OnLine",

        "IN S C": "INSC",

        "0nLine": "OnLine",

        "( ": "(",
        " )": ")"
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    # ---------------------------------------------
    # MULTISPACE COLLAPSE
    # ---------------------------------------------

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text


# =========================================================
# 🔥 CITATION RECONSTRUCTION
# =========================================================

def reconstruct_citation_windows(text):

    lines = text.splitlines()

    reconstructed = []

    buffer = ""

    for line in lines:

        cleaned = line.strip()

        if not cleaned:
            continue

        # -----------------------------------------
        # JOIN SMALL OCR-BROKEN LINES
        # -----------------------------------------

        if len(cleaned) < 80:

            buffer += " " + cleaned

        else:

            if buffer:

                reconstructed.append(buffer.strip())

            reconstructed.append(cleaned)

            buffer = ""

    if buffer:
        reconstructed.append(buffer.strip())

    reconstructed_text = "\n".join(reconstructed)

    reconstructed_text = normalize_ocr_text(
        reconstructed_text
    )

    print("✅ Citation Reconstruction Complete")

    return reconstructed_text


# =========================================================
# 🔥 CANONICAL CITATION PATTERNS
# =========================================================

CITATION_PATTERNS = {

    "SCC": [

        r'\(\s*\d{4}\s*\)\s*\d+\s*SCC\s*\d+',

        r'\(\d{4}\)\d+SCC\d+'
    ],

    "SCC_ONLINE": [

        r'\d{4}\s*SCC\s*OnLine\s*SC\s*\d+'
    ],

    "AIR": [

        r'AIR\s*\d{4}\s*SC\s*\d+'
    ],

    "SCR": [

        r'\[\s*\d{4}\s*\]\s*\d+\s*SCR\s*\d+'
    ],

    "INSC": [

        r'\d{4}\s*INSC\s*\d+'
    ],

    "SLP": [

        r'SLP\s*\(.*?\)\s*No\.?\s*\d+\s*of\s*\d{4}'
    ],

    "ARTICLE": [

        r'Article\s+\d+[A-Z\-]*',

        r'Art\.?\s*\d+[A-Z\-]*'
    ],

    "SECTION": [

        r'Section\s+\d+[A-Z\-\(\)]*\s*(?:of\s+the\s+[A-Za-z\s]+)?',

        r'Sec\.?\s*\d+[A-Z\-\(\)]*',

        r'u/s\.?\s*\d+[A-Z\-\(\)]*'
    ],

    "RULE": [

        r'Rule\s+\d+[A-Z\-]*',

        r'Order\s+\d+\s+Rule\s+\d+'
    ]
}

# =========================================================
# 🔥 TREATMENT WORDS
# =========================================================

TREATMENT_PATTERNS = {

    "followed": [
        "followed",
        "relied upon",
        "applied"
    ],

    "distinguished": [
        "distinguished"
    ],

    "overruled": [
        "overruled"
    ],

    "affirmed": [
        "affirmed"
    ],

    "reversed": [
        "reversed",
        "set aside"
    ],

    "referred": [
        "referred to",
        "cited"
    ]
}

# =========================================================
# 🔥 NORMALIZER
# =========================================================

def normalize_citation(citation):

    citation = re.sub(
        r'\s+',
        ' ',
        citation
    ).strip()

    return citation


# =========================================================
# 🔥 TREATMENT DETECTION
# =========================================================

def detect_treatment(context):

    lowered = context.lower()

    for treatment, keywords in TREATMENT_PATTERNS.items():

        for keyword in keywords:

            if keyword in lowered:
                return treatment

    return "referred"


# =========================================================
# 🔥 MAIN ENGINE
# =========================================================

def extract_citations(full_text=""):

    try:

        if not isinstance(full_text, str):
            full_text = str(full_text)

        # ---------------------------------------------
        # OCR RECONSTRUCTION
        # ---------------------------------------------

        full_text = reconstruct_citation_windows(
            full_text
        )

        citations = []

        print("🔥 CITATION TEXT SAMPLE:")
        print(full_text[:5000])

        seen = set()

        for citation_type, patterns in CITATION_PATTERNS.items():

            for pattern in patterns:

                matches = re.findall(
                    pattern,
                    full_text,
                    flags=re.IGNORECASE
                )

                for match in matches:

                    normalized = normalize_citation(
                        match
                    )

                    if normalized in seen:
                        continue

                    seen.add(normalized)

                    year_match = re.search(
                        r'\d{4}',
                        normalized
                    )

                    citations.append({

                        "citation":
                            normalized,

                        "type":
                            citation_type,

                        "court":
                            "Supreme Court",

                        "year":
                            year_match.group(0)
                            if year_match
                            else None,

                        "treatment":
                            detect_treatment(
                                full_text
                            ),

                        "canonical":
                            True
                    })

        print("✅ Citations Extracted:")
        print(citations)

        return {

            "citations":
                citations,

            "count":
                len(citations),

            "confidence":
                95
        }

    except Exception as e:

        print("❌ Citation Extraction Error:")
        print(str(e))

        return {

            "citations": [],
            "count": 0,
            "confidence": 0
        }
