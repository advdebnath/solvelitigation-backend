import re

# 🔥 Known Act normalization
ACT_NORMALIZATION = {
    "Major Port Trust Act, 1963": "Major Port Trusts Act, 1963",
    "Major Port Trusts Act, 1963": "Major Port Trusts Act, 1963",
    "Indian Contract Act, 1872": "Indian Contract Act, 1872",
    "Industrial Disputes Act, 1947": "Industrial Disputes Act, 1947",
}

ACT_ABBREVIATIONS = {
    "IPC": "Indian Penal Code, 1860",
    "CRPC": "Code of Criminal Procedure, 1973",
    "CPC": "Code of Civil Procedure, 1908",
}

def extract_acts(text):
    acts = set()

    # 🔹 STRICT regex (no long sentences)
    pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+Act[s]?,?\s*\d{4})\b'
    matches = re.findall(pattern, text)

    for m in matches:
        act = m.strip()

        # remove prefixes
        act = re.sub(r'^(Of The|Under The|Under|Of)\s+', '', act, flags=re.IGNORECASE)

        # fix comma
        act = re.sub(r'Act\s+(\d{4})', r'Act, \1', act)

        # normalize spaces
        act = re.sub(r'\s+', ' ', act)

        # normalize known acts
        act = ACT_NORMALIZATION.get(act, act)

        # filter garbage (very important)
        if len(act.split()) > 8:
            continue

        acts.add(act)

    # 🔹 abbreviation detection
    upper_text = text.upper()
    for abbr, full in ACT_ABBREVIATIONS.items():
        if abbr in upper_text:
            acts.add(full)

    return list(acts)
