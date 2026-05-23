import re

from collections import defaultdict

from app.legal_ontology.canonical_legal_object_engine import (
    canonicalize_act_name,
    build_canonical_legal_object
)

# =========================================================
# 🔥 ACT ONTOLOGY
# =========================================================

ACT_PATTERNS = {

    "Constitution Of India": {

        "type": "Article",

        "patterns": [

            r'Article\s+(\d+[A-Z\-]*)'
        ],

        "signals": [

            "writ petition",
            "constitutional",
            "fundamental rights",
            "judicial review",
            "high court"
        ]
    },

    "Code Of Criminal Procedure, 1973": {

        "type": "Section",

        "patterns": [

            r'Section\s+(\d+[A-Z\-]*)',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+of\s+IPC',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+IPC',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+CrPC',

            r'under\s+section\s+(\d+[A-Z\-\(\)]*)'
        ],

        "signals": [

            "fir",
            "bail",
            "accused",
            "criminal",
            "charge sheet",
            "investigation",
            "trial"
        ]
    },

    "Indian Penal Code, 1860": {

        "type": "Section",

        "patterns": [

            r'Section\s+(\d+[A-Z\-]*)',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+of\s+IPC',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+IPC',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+CrPC',

            r'under\s+section\s+(\d+[A-Z\-\(\)]*)'
        ],

        "signals": [

            "murder",
            "assault",
            "offence",
            "conviction",
            "sentence",
            "homicide"
        ]
    },

    "Wakf Act, 1995": {

        "type": "Section",

        "patterns": [

            r'Section\s+(\d+[A-Z\-]*)',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+of\s+IPC',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+IPC',

            r'u/s\.?\s*(\d+[A-Z\-\(\)]*)\s+CrPC',

            r'under\s+section\s+(\d+[A-Z\-\(\)]*)',

            r'Section[s]?\s+85A?\s+of\s+the\s+Wakf\s+Act[, ]*1995',

            r'Section[s]?\s+85A?\s+of\s+Wakf\s+Act',

            r'Wakf\s+Act[, ]*1995',

            r'Wakf\s+Tribunal',
        ],

        "signals": [

            "wakf",
            "wakf board",
            "mutawalli",
            "wakf property",
            "tribunal",
            "tenant"
        ]
    }
}

# =========================================================
# 🔥 WINDOW CONFIG
# =========================================================

WINDOW_SIZE = 350

# =========================================================
# 🔥 CONTEXT SCORE
# =========================================================

def calculate_context_score(
    context,
    signals
):

    score = 0

    context = context.lower()

    for signal in signals:

        if signal.lower() in context:

            score += 10

    return score

# =========================================================
# 🔒 OCR-SAFE SECTION NORMALIZATION LOCK
# =========================================================

def normalize_section_text(text):

    if not text:
        return ""

    text = str(text)

    # -----------------------------------------------------
    # 🔥 OCR RECONSTRUCTION
    # -----------------------------------------------------

    text = re.sub(
        r"u\s*/\s*s\.?",
        "u/s",
        text,
        flags=re.I
    )

    text = re.sub(
        r"S\s*E\s*C\s*T\s*I\s*O\s*N",
        "Section",
        text,
        flags=re.I
    )

    text = re.sub(
        r"A\s*R\s*T\s*I\s*C\s*L\s*E",
        "Article",
        text,
        flags=re.I
    )

    text = re.sub(
        r"Cr\s*P\s*C",
        "CrPC",
        text,
        flags=re.I
    )

    text = re.sub(
        r"I\s*P\s*C",
        "IPC",
        text,
        flags=re.I
    )

    text = re.sub(
        r"\s{2,}",
        " ",
        text
    )

    return text.strip()


# =========================================================
# 🔥 MAIN EXTRACTOR
# =========================================================

def extract_sections(
    full_text=""
):

    if not full_text:

        return {

            "sections": [],

            # backward compatibility
            "matched_sections": [],

            "confidence": 0
        }

    text = normalize_section_text(full_text)

    extracted = []

    seen = set()

    # -----------------------------------------------------
    # 🔥 ACT LOOP
    # -----------------------------------------------------

    for act_name, config in ACT_PATTERNS.items():

        section_type = config.get(
            "type"
        )

        patterns = config.get(
            "patterns",
            []
        )

        signals = config.get(
            "signals",
            []
        )

        # -------------------------------------------------
        # 🔥 PATTERN LOOP
        # -------------------------------------------------

        for pattern in patterns:

            for match in re.finditer(

                pattern,
                text,
                flags=re.I
            ):

                try:

                    section_number = match.group(1)

                except Exception:
                    continue

                # =========================================
                # 🔥 OCR / MALFORMED SECTION NORMALIZATION
                # =========================================

                if not section_number:
                    continue

                section_number = (
                    str(section_number)
                    .strip()
                    .upper()
                )

                section_number = (
                    section_number
                    .replace("O", "0")
                    .replace("I", "1")
                )

                section_number = section_number.strip(
                    ".,:;()[]{}"
                )

                if len(section_number) > 15:
                    continue

                if section_number.startswith("-"):
                    continue

                if section_number.endswith("-"):
                    continue

                if not re.fullmatch(
                    r"[0-9A-Z/-]+",
                    section_number
                ):
                    continue

                # -----------------------------------------
                # 🔥 LOCAL CONTEXT WINDOW
                # -----------------------------------------

                start = max(

                    0,

                    match.start() - WINDOW_SIZE
                )

                end = min(

                    len(text),

                    match.end() + WINDOW_SIZE
                )

                context = text[start:end]

                # -----------------------------------------
                # 🔥 CONTEXT SCORE
                # -----------------------------------------

                context_score = calculate_context_score(

                    context,
                    signals
                )

                # -----------------------------------------
                # 🔥 CONTEXT FILTER
                # -----------------------------------------

                if context_score < 10:
                    continue

                # -----------------------------------------
                # 🔥 CONSTITUTION FILTER
                # -----------------------------------------

                if (
                    act_name == "Constitution Of India"
                    and section_type != "Article"
                ):
                    continue

                key = (

                    section_type,
                    section_number,
                    act_name
                )

                if key in seen:
                    continue

                seen.add(key)

                extracted.append({

                    "type":
                        section_type,

                    "section":
                        section_number,

                    # -----------------------------------------
                    # 🔒 CANONICAL ACT NORMALIZATION
                    # -----------------------------------------

                    "act":
                        canonicalize_act_name(
                            act_name
                        ),

                    "canonical_act_object":
                        build_canonical_legal_object(
                            canonicalize_act_name(
                                act_name
                            ),
                            "ACT"
                        ),

                    "context_score":
                        context_score
                })

    # =====================================================
    # 🔒 CONTEXTUAL CRIMINAL LAW ENRICHMENT LOCK
    # =====================================================

    lower_text = text.lower()

    if not extracted:

        # -------------------------------------------------
        # 🔥 CrPC CONTEXT
        # -------------------------------------------------

        if any(
            token in lower_text
            for token in [
                "fir",
                "charge sheet",
                "criminal appeal",
                "bail",
                "trial court",
                "accused",
                "investigation",
                "conviction",
                "sentence"
            ]
        ):

            extracted.append({

                "type":
                    "Contextual",

                "section":
                    "Procedural",

                "act":
                    "Code Of Criminal Procedure, 1973",

                "canonical_act_object":
                    build_canonical_legal_object(
                        "Code Of Criminal Procedure, 1973",
                        "ACT"
                    ),

                "context_score":
                    40
            })

        # -------------------------------------------------
        # 🔥 IPC CONTEXT
        # -------------------------------------------------

        if any(
            token in lower_text
            for token in [
                "murder",
                "assault",
                "homicide",
                "weapon",
                "offence",
                "crime"
            ]
        ):

            extracted.append({

                "type":
                    "Contextual",

                "section":
                    "Substantive",

                "act":
                    "Indian Penal Code, 1860",

                "canonical_act_object":
                    build_canonical_legal_object(
                        "Indian Penal Code, 1860",
                        "ACT"
                    ),

                "context_score":
                    40
            })

    # -----------------------------------------------------
    # 🔥 SORTING
    # -----------------------------------------------------

    extracted = sorted(

        extracted,

        key=lambda x: x.get(
            "context_score",
            0
        ),

        reverse=True
    )

    return {

        "sections":
            extracted,

        # backward compatibility
        "matched_sections": [

            item.get("section")

            for item in extracted

            if item.get("section")
        ],

        "confidence":
            min(
                95,
                60 + len(extracted) * 5
            )
    }
