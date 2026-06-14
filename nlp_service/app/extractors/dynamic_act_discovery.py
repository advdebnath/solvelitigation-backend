import re



ACT_PATTERNS = [

    r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,10}\s+Act[, ]*\d{4})\b',

    r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,10}\s+Rules[, ]*\d{4})\b',

    r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,10}\s+Regulations[, ]*\d{4})\b',

    r'\b(Constitution Of India)\b',

]


def discover_dynamic_acts(text=""):

    if not text:
        return []

    acts = []

    for pattern in ACT_PATTERNS:

        matches = re.findall(
            pattern,
            text,
            flags=re.I
        )

        for m in matches:

            value = str(m).strip()

            value = re.sub(
                r'^(under|of|and|the|schedule to|as per|provisions of)\s+',
                '',
                value,
                flags=re.I
            )

            value = re.sub(
                r'\s+',
                ' ',
                value
            )

            value = value.strip(' ,.;:')
            # ==========================================
            # 🔥 ACT TITLE NORMALIZATION
            # ==========================================

            value = re.sub(
                r'\s*,\s*',
                ', ',
                value
            )

            value = value.title()

            value = re.sub(
                r'\bAct\b',
                'Act',
                value
            )

            value = re.sub(
                r'\bRules\b',
                'Rules',
                value
            )

            value = re.sub(
                r'\bRegulations\b',
                'Regulations',
                value
            )




            if value.lower().startswith(
                (
                    "the ",
                    "of ",
                    "under ",
                    "and ",
                    "had ",
                    "as per ",
                    "schedule to "
                )
            ):
                continue

            if len(value.split()) > 12:
                continue


            value = re.sub(
                r"\s+",
                " ",
                value
            )

            if len(value) < 5:
                continue

            acts.append(value)

    acts = sorted(
        list(
            dict.fromkeys(acts)
        )
    )

    print("🔥 DYNAMIC ACT DISCOVERY 🔥")
    print(acts)

    return acts
