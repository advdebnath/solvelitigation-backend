import re


def clean_name(name):
    name = re.sub(
        r"\b(Appellant|Petitioner|Respondent|Versus|Vs\.?)\b",
        "",
        name,
        flags=re.IGNORECASE,
    )
    name = re.sub(r"[^A-Za-z0-9\s\.\&]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()


def extract_parties(text):
    clean = re.sub(r"\s+", " ", text)

    patterns = [
        r"(.*?)\s+v(?:s\.?|ersus)\s+(.*?)(?:\n|$)",
        r"(.*?)\s+V(?:S\.?|ERSUS)\s+(.*?)(?:\n|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, clean, re.IGNORECASE)
        if match:
            petitioner = match.group(1).strip()
            respondent = match.group(2).strip()
            return clean_name(petitioner), clean_name(respondent)

    return "Unknown", "Unknown"
