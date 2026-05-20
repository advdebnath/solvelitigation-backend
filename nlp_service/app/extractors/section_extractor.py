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

    text = str(full_text)

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
