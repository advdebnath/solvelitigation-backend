import re
from collections import defaultdict


ENTITY_PATTERNS = {
    "acts": [
        r'([A-Z][A-Za-z0-9()\-]{2,40}(?:\s+[A-Z][A-Za-z0-9()\-]{2,40}){0,8}\s+Act(?:,\s*\d{4})?)',
    ],
    "codes": [
        r'([A-Z][A-Za-z0-9 ,()\-]{3,200}\s+Code(?:,\s*\d{4})?)',
    ],
    "rules": [
        r'([A-Z][A-Za-z0-9 ,()\-]{3,200}\s+Rules(?:,\s*\d{4})?)',
    ],
    "regulations": [
        r'([A-Z][A-Za-z0-9 ,()\-]{3,200}\s+Regulations(?:,\s*\d{4})?)',
    ],
    "tribunals": [
        r'([A-Z][A-Za-z0-9 ,()\-]{3,200}\s+Tribunal)',
    ],
    "authorities": [
        r'([A-Z][A-Za-z0-9 ,()\-]{3,200}\s+Authority)',
        r'([A-Z][A-Za-z0-9 ,()\-]{3,200}\s+Commission)',
        r'([A-Z][A-Za-z0-9 ,()\-]{3,200}\s+Board)',
    ],
}



def normalize_entity_name(name):

    name = re.sub(
        r',\s*\d{4}$',
        '',
        name.strip(),
        flags=re.I
    )

    name = re.sub(
        r'\s+',
        ' ',
        name
    )

    return name.strip()


SECTION_ACT_PATTERN = re.compile(
    r'Section[s]?\s+([0-9A-Za-z()./\-]+).*?of\s+the\s+([A-Z][A-Za-z0-9 ,()\-]{3,200}(?:Act|Code|Rules|Regulations))',
    re.I | re.S
)


def discover_legal_entities(text):

    result = {
        "acts": [],
        "codes": [],
        "rules": [],
        "regulations": [],
        "tribunals": [],
        "authorities": [],
        "sections": [],
        "section_act_map": [],
        "frequency": {},
        "dominant_entity": None,
    }

    if not text:
        return result

    frequency = defaultdict(int)

    for entity_type, patterns in ENTITY_PATTERNS.items():

        for pattern in patterns:

            for match in re.findall(pattern, text):

                value = normalize_entity_name(
    str(match)
)

                words = value.split()

                if len(words) > 15:
                    continue

                invalid_terms = [
                    "court was",
                    "this court",
                    "it is",
                    "however",
                    "therefore",
                    "contended",
                    "argued",
                    "held that"
                ]

                if any(t in value.lower() for t in invalid_terms):
                    continue

                if ";" in value or ":" in value:
                    continue


                if len(value) < 5:
                    continue

                result[entity_type].append(value)

                frequency[value] += 1

    for section, act in SECTION_ACT_PATTERN.findall(text):

        result["section_act_map"].append({
            "section": section.strip(),
            "act": act.strip()
        })

        result["sections"].append(section.strip())

        
        canonical_act = normalize_entity_name(
            act.strip()
        )

        frequency[canonical_act] += 1


    for key in [
        "acts",
        "codes",
        "rules",
        "regulations",
        "tribunals",
        "authorities",
        "sections",
    ]:
        result[key] = sorted(list(set(result[key])))

    result["frequency"] = dict(
        sorted(
            frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    if frequency:
        result["dominant_entity"] = max(
            frequency,
            key=frequency.get
        )

    return result
