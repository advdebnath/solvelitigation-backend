import json
import os
import re

from rapidfuzz import process

LEGAL_DICTIONARY = set()

LEGAL_CORRECTIONS = {}

CORRECTION_FILE = (
    "/var/www/solvelitigation/nlp_service/app/data/legal_corrections.json"
)

if os.path.exists(CORRECTION_FILE):
    try:
        with open(
            CORRECTION_FILE,
            "r",
            encoding="utf-8"
        ) as fp:
            LEGAL_CORRECTIONS = json.load(fp)

    except Exception as e:
        print("❌ CORRECTION MAP LOAD ERROR:", e)


DICT_FILES = [
    "/var/www/solvelitigation/nlp_service/app/data/legal_dictionary.json",
    "/var/www/solvelitigation/nlp_service/app/data/generated_legal_dictionary.json",
]

for dict_file in DICT_FILES:

    if not os.path.exists(dict_file):
        continue

    try:

        with open(
            dict_file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, dict):

                LEGAL_DICTIONARY.update(
                    {
                        str(k).lower()
                        for k in data.keys()
                    }
                )

            elif isinstance(data, list):

                LEGAL_DICTIONARY.update(
                    {
                        str(x).lower()
                        for x in data
                    }
                )

    except Exception as e:

        print(
            f"❌ DICTIONARY LOAD ERROR: {dict_file}",
            e,
            flush=True
        )

print(
    f"✅ OCR DICTIONARY LOADED: {len(LEGAL_DICTIONARY)} words",
    flush=True
)


def fuzzy_fix(token):

    token_lower = token.lower()

    if token_lower in LEGAL_CORRECTIONS:
        return LEGAL_CORRECTIONS[token_lower]

    if (
        not token
        or len(token) < 5
        or token_lower in LEGAL_DICTIONARY
    ):
        return token

    try:

        result = process.extractOne(
            token.lower(),
            LEGAL_DICTIONARY,
            score_cutoff=92
        )

        if result:

            candidate = result[0]

            return candidate

    except Exception:
        pass

    return token


def dynamic_ocr_reconstruct(text):

    if not text:
        return ""

    repaired = str(text)

    print(
        f"🔥 OCR ENGINE ACTIVE | Dictionary={len(LEGAL_DICTIONARY)}",
        flush=True
    )

    repair_count = 0


    patterns = [

        r"\b([A-Za-z]{4,})\s+(ion)\b",
        r"\b([A-Za-z]{4,})\s+(ive)\b",
        r"\b([A-Za-z]{4,})\s+(ment)\b",
        r"\b([A-Za-z]{4,})\s+(tion)\b",
        r"\b([A-Za-z]{4,})\s+(ence)\b",
        r"\b([A-Za-z]{4,})\s+(ent)\b",

    ]

    for pattern in patterns:

        matches = list(
            re.finditer(
                pattern,
                repaired,
                flags=re.I
            )
        )

        for match in reversed(matches):

            left = match.group(1)
            right = match.group(2)

            candidate = (
                left + right
            ).lower()

            if candidate in LEGAL_DICTIONARY:

                repaired = (
                    repaired[:match.start()]
                    + candidate
                    + repaired[match.end():]
                )

                repair_count += 1

                print(
                    f"🔧 OCR FIX: {left} {right} -> {candidate}",
                    flush=True
                )

    # =====================================================
    # 🔥 FRAGMENT STITCHER V2
    # =====================================================

    fragment_patterns = [

        (
            r"\b([A-Za-z]{2,})\s+i\s+o\s+n\b",
            lambda m: (
                m.group(1) + "ition"
            ).lower()
        ),

        (
            r"\b([A-Za-z]{3,})\s+i\s+v\s+e\b",
            lambda m: (
                m.group(1) + "ive"
            ).lower()
        ),

        (
            r"\b([A-Za-z]{3,})\s+m\s+e\s+n\s+t\b",
            lambda m: (
                m.group(1) + "ment"
            ).lower()
        ),

        (
            r"\b([A-Za-z]{3,})\s+t\s+i\s+o\s+n\b",
            lambda m: (
                m.group(1) + "tion"
            ).lower()
        ),

    ]

    for pattern, builder in fragment_patterns:

        matches = list(
            re.finditer(
                pattern,
                repaired,
                flags=re.I
            )
        )

        for match in reversed(matches):

            candidate = builder(match)

            if candidate in LEGAL_DICTIONARY:

                repaired = (
                    repaired[:match.start()]
                    + candidate
                    + repaired[match.end():]
                )

                repair_count += 1

                print(
                    f"🔥 FRAGMENT FIX -> {candidate}",
                    flush=True
                )


    token_pattern = re.compile(
        r"\b[A-Za-z]{5,}\b"
    )

    def replace_token(m):

        nonlocal repair_count

        token = m.group(0)

        fixed = token

        if token.lower() in LEGAL_CORRECTIONS:
            fixed = LEGAL_CORRECTIONS[token.lower()]

        if fixed != token.lower():

            repair_count += 1

            print(
                f"🔧 CORRECTION MAP: {token} -> {fixed}",
                flush=True
            )

            return fixed

        return token

    repaired = token_pattern.sub(
        replace_token,
        repaired
    )

    # =====================================================
    # GLOBAL WHOLE-WORD CORRECTIONS
    # =====================================================

    for bad, good in LEGAL_CORRECTIONS.items():

        repaired = re.sub(
            rf"\b{re.escape(bad)}\b",
            good,
            repaired,
            flags=re.I
        )


    print(
        f"🔧 OCR FIXES APPLIED: {repair_count}",
        flush=True
    )

    return repaired
