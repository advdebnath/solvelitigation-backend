import re
from typing import List


def clean_single_judge_name(name: str) -> str:
    name = re.sub(r"J\s+U\s+D\s+G\s+M\s+E\s+N\s+T", "", name, flags=re.IGNORECASE)
    name = re.sub(r"Hon'?ble", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\bHon\b", "", name, flags=re.IGNORECASE)

    name = name.replace("\n", " ").strip()
    name = re.sub(r"\s+", " ", name)
    name = name.strip(" ,.;:")

    name = re.sub(r"\b([A-Z])\s+([A-Z])\b", r"\1. \2.", name)
    name = re.sub(r"\b([A-Z])\b(?!\.)", r"\1.", name)
    name = re.sub(r"\.\.", ".", name)

    return name.strip()


def normalize_judges(judges: List[str]) -> List[str]:
    cleaned = []

    for judge in judges:
        cleaned_name = clean_single_judge_name(judge)

        if cleaned_name and len(cleaned_name) > 3:
            cleaned.append(cleaned_name)

    seen = set()
    unique = []
    for j in cleaned:
        key = j.lower()
        if key not in seen:
            seen.add(key)
            unique.append(j)

    return unique
