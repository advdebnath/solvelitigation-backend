import re

def normalize_text(text):
    return re.sub(r"\s+", " ", text).strip()
