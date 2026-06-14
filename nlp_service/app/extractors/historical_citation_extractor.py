import re


SCC_PATTERNS = [
    r"\(\d{4}\)\s*\d+\s*SCC\s*\d+",
    r"\d{4}\s*\(\d+\)\s*SCC\s*\d+",
]

AIR_PATTERNS = [
    r"AIR\s+\d{4}\s+SC\s+\d+",
    r"AIR\s+\d{4}\s+S\.C\.\s+\d+",
]

SCR_PATTERNS = [
    r"\[\d{4}\]\s*\d+\s*SCR\s*\d+",
    r"\d{4}\s+Supp\s*\(\d+\)\s*SCR\s*\d+",
]

JT_PATTERNS = [
    r"JT\s+\d{4}\s*\(\d+\)\s*SC\s*\d+",
    r"JT\s+\d{4}\s*\(\d+\)\s*S\.C\.\s*\d+",
]

SCALE_PATTERNS = [
    r"\(\d{4}\)\s*\d+\s*SCALE\s*\d+",
]



def extract_historical_citations(text=""):

    citations = []

    for patterns in [
        SCC_PATTERNS,
        AIR_PATTERNS,
        SCR_PATTERNS,
        JT_PATTERNS,
        SCALE_PATTERNS,
    ]:

        for pattern in patterns:

            matches = re.findall(
                pattern,
                text,
                flags=re.I
            )

            citations.extend(matches)

    citations = list(
        dict.fromkeys(
            [c.strip() for c in citations]
        )
    )

    preferred = ""

    for c in citations:
        if "SCC" in c.upper():
            preferred = c
            break

    if not preferred and citations:
        preferred = citations[0]

    return {
        "preferredCitation": preferred,
        "citations": citations,
    }
