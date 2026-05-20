import re

# =========================================================
# 🔥 RELATIONSHIP KEYWORDS
# =========================================================

RELATIONSHIP_PATTERNS = {

    "followed": [
        "followed",
        "relied upon",
        "applied",
        "approved"
    ],

    "distinguished": [
        "distinguished",
        "distinguishable"
    ],

    "overruled": [
        "overruled"
    ],

    "reversed": [
        "reversed",
        "set aside"
    ],

    "affirmed": [
        "affirmed",
        "upheld"
    ],

    "referred": [
        "referred to",
        "cited",
        "considered"
    ]
}

# =========================================================
# 🔥 CITATION PATTERN
# =========================================================

CITATION_PATTERN = re.compile(

    r'(\(\d{4}\)\s*\d+\s*SCC\s*\d+|'
    r'AIR\s*\d{4}\s*SC\s*\d+|'
    r'\d{4}\s*SCC\s*OnLine\s*SC\s*\d+|'
    r'\d{4}\s*INSC\s*\d+)',

    flags=re.IGNORECASE
)

# =========================================================
# 🔥 CASE NAME PATTERN
# =========================================================

CASE_PATTERN = re.compile(

    r'([A-Z][A-Za-z\.\s&]+v(?:s\.?|ersus)\s*[A-Z][A-Za-z\.\s&]+)',

    flags=re.IGNORECASE
)

# =========================================================
# 🔥 RELATIONSHIP DETECTOR
# =========================================================

def detect_relationship(text=""):

    lowered = text.lower()

    for relation, keywords in RELATIONSHIP_PATTERNS.items():

        for keyword in keywords:

            if keyword in lowered:

                return relation

    return "referred"

# =========================================================
# 🔥 MAIN ENGINE
# =========================================================

def build_citation_graph(full_text=""):

    try:

        if not isinstance(full_text, str):

            full_text = str(full_text)

        graph_edges = []

        seen = set()

        lines = full_text.splitlines()

        for line in lines:

            case_match = CASE_PATTERN.search(line)

            citation_match = CITATION_PATTERN.search(line)

            if not case_match:
                continue

            case_name = re.sub(
                r'\s+',
                ' ',
                case_match.group(1)
            ).strip()

            citation = None

            if citation_match:

                citation = re.sub(
                    r'\s+',
                    ' ',
                    citation_match.group(1)
                ).strip()

            relationship = detect_relationship(line)

            key = f"{case_name}_{citation}_{relationship}"

            if key in seen:
                continue

            seen.add(key)

            graph_edges.append({

                "source":
                    "current_case",

                "target":
                    case_name,

                "citation":
                    citation,

                "relationship":
                    relationship,

                "weight":
                    1
            })

        print("✅ Citation Graph Built:")
        print(graph_edges)

        return {

            "edges":
                graph_edges,

            "count":
                len(graph_edges),

            "confidence":
                90
        }

    except Exception as e:

        print("❌ Citation Graph Error:")
        print(str(e))

        return {

            "edges": [],
            "count": 0,
            "confidence": 0
        }

