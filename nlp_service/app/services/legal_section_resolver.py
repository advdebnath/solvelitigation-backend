# =====================================================
# 🔥 SOLVELITIGATION
# DYNAMIC LEGAL SECTION RESOLVER ENGINE
# =====================================================

from pymongo import MongoClient
import os

# =====================================================
# 🔥 MONGO CONNECTION
# =====================================================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://127.0.0.1:27017/solvelitigation"
)

mongo_client = MongoClient(MONGO_URI)

db = mongo_client["solvelitigation"]

# =====================================================
# 🔥 STATIC SEED MAP
# =====================================================

SECTION_ACT_MAP = {

    # ==========================================
    # IPC
    # ==========================================

    "302": "Indian Penal Code, 1860",
    "304B": "Indian Penal Code, 1860",
    "376": "Indian Penal Code, 1860",
    "420": "Indian Penal Code, 1860",
    "498A": "Indian Penal Code, 1860",
    "406": "Indian Penal Code, 1860",
    "307": "Indian Penal Code, 1860",
    "34": "Indian Penal Code, 1860",
    "120B": "Indian Penal Code, 1860",

    # ==========================================
    # CRPC
    # ==========================================

    "125": "Code Of Criminal Procedure, 1973",
    "161": "Code Of Criminal Procedure, 1973",
    "164": "Code Of Criminal Procedure, 1973",
    "173": "Code Of Criminal Procedure, 1973",
    "438": "Code Of Criminal Procedure, 1973",
    "439": "Code Of Criminal Procedure, 1973",

    # ==========================================
    # EVIDENCE ACT
    # ==========================================

    "27": "Indian Evidence Act, 1872",
    "32": "Indian Evidence Act, 1872",
    "65B": "Indian Evidence Act, 1872",

    # ==========================================
    # NI ACT
    # ==========================================

    "138":
        "Negotiable Instruments Act, 1881",
}

# =====================================================
# 🔥 DYNAMIC ONTOLOGY LOOKUP
# =====================================================

def dynamic_ontology_lookup(

    section,

    context="",

    category=""
):

    try:

        sec = str(section).upper().strip()

        ctx = str(context).lower()

        ontology_records = list(

            db.legalontologies.find(

                {
                    "section": sec
                }
            )
        )

        if not ontology_records:

            return None

        # ==========================================
        # BEST MATCH ENGINE
        # ==========================================

        best_match = None

        best_score = 0

        for record in ontology_records:

            score = 0

            # --------------------------------------
            # CATEGORY BOOST
            # --------------------------------------

            if (
                record.get("category")
                == category
            ):

                score += 5

            # --------------------------------------
            # CONTEXT BOOST
            # --------------------------------------

            for word in record.get(

                "contexts",
                []
            ):

                if word.lower() in ctx:

                    score += 10

            # --------------------------------------
            # CONFIDENCE BOOST
            # --------------------------------------

            score += int(

                record.get(
                    "confidence",
                    50
                ) / 10
            )

            # --------------------------------------
            # BEST MATCH
            # --------------------------------------

            if score > best_score:

                best_score = score

                best_match = record

        if best_match:

            print(
                "✅ Dynamic ontology match:",
                {
                    "section": sec,
                    "act":
                        best_match.get("act"),
                    "score":
                        best_score
                }
            )

            return best_match.get("act")

    except Exception as e:

        print(
            "❌ Dynamic ontology lookup failed:",
            e
        )

    return None

# =====================================================
# 🔥 CONTEXTUAL SECTION RESOLUTION
# =====================================================

def resolve_section_act(

    section,

    category="",

    context=""
):

    sec = str(section).upper().strip()

    ctx = str(context).lower()

    # =================================================
    # 🔥 DYNAMIC ONTOLOGY FIRST
    # =================================================

    dynamic_match = dynamic_ontology_lookup(

        section=sec,

        context=ctx,

        category=category
    )

    if dynamic_match:

        return dynamic_match

    # =================================================
    # 🔥 SPECIAL CONTEXTUAL RULES
    # =================================================

    if sec == "25":

        if "arms" in ctx:

            return "Arms Act, 1959"

        return "Indian Penal Code, 1860"

    if sec == "27":

        if (

            "recovery" in ctx

            or

            "evidence" in ctx
        ):

            return "Indian Evidence Act, 1872"

    if sec == "13":

        if (

            "corruption" in ctx

            or

            "public servant" in ctx
        ):

            return (
                "Prevention Of Corruption Act, 1988"
            )

    if sec == "7":

        if (

            "corruption" in ctx

            or

            "bribe" in ctx
        ):

            return (
                "Prevention Of Corruption Act, 1988"
            )

    # =================================================
    # 🔥 STATIC LOOKUP
    # =================================================

    if sec in SECTION_ACT_MAP:

        return SECTION_ACT_MAP[sec]

    # =================================================
    # 🔥 CATEGORY FALLBACKS
    # =================================================

    if category == "Criminal":

        return "Indian Penal Code, 1860"

    if category == "Civil":

        return "Code Of Civil Procedure, 1908"

    if category == "Service Law":

        return "Service Law"

    if category == "Taxation & Corporate":

        return "Taxation Law"

    # =================================================
    # 🔥 FINAL FALLBACK
    # =================================================

    return "Unknown Act"
