import re

# 🔥 KEY LEGAL SIGNAL WORDS
REASONING_WORDS = ["because", "held", "observed", "considered", "therefore"]
RATIO_WORDS = ["it is held", "ratio", "principle", "law laid down"]
OUTCOME_WORDS = ["appeal dismissed", "appeal allowed", "conviction", "acquitted"]

def detect_reasoning(text):
    t = text.lower()
    return any(word in t for word in REASONING_WORDS)

def detect_ratio(text):
    t = text.lower()
    return any(word in t for word in RATIO_WORDS)

def detect_outcome(text):
    t = text.lower()
    for word in OUTCOME_WORDS:
        if word in t:
            return word
    return "decision"

def extract_highlights_v2(full_text, sections):
    paragraphs = re.split(r"\n{2,}", full_text)

    results = []

    for para in paragraphs:
        para_lower = para.lower()

        for sec in sections:
            sec_num = sec.replace("Section", "").strip()

            patterns = [
                f"section {sec_num}",
                f"sec. {sec_num}",
                f"u/s {sec_num}"
            ]

            if any(p in para_lower for p in patterns):
                results.append({
                    "section": sec,
                    "text": para.strip(),
                    "isReasoning": detect_reasoning(para),
                    "isRatio": detect_ratio(para),
                    "outcome": detect_outcome(para)
                })
                break

    return results[:30]
